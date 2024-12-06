#!/usr/bin/env python3

## Copyright 2024 David Miguel Susano Pinto <pinto@robots.ox.ac.uk>
##
## Licensed under the Apache License, Version 2.0 (the "License"); you
## may not use this file except in compliance with the License.  You
## may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
## implied.  See the License for the specific language governing
## permissions and limitations under the License.

"""Tools to handle COCO data files.

COCO is not a VIA format but it is very widespread.  See
https://cocodataset.org/#format-data for COCO data format and
https://cocodataset.org/#format-results for COCO results format.

"""


import argparse
import contextlib
import datetime
import json
import logging
import os
import sys
from typing import Dict, List, Optional

import PIL.Image
import pycocotools.coco
import pycocotools.mask

import via.lisa
from via.via3 import (
    VIA3AttributeType,
    VIA3FileLoc,
    VIA3FileType,
    VIA3RegionShape,
)


_logger = logging.getLogger(__name__)


def empty_coco():
    return {
        "info": {
            "year": datetime.datetime.now().year,
            "version": "",
            "description": "",
            "contributor": "",
            "url": "",
            "date_created": datetime.datetime.now().isoformat(),
        },
        "images": [],
        "annotations": [],
        "categories": [],
        "licenses": [],
    }


def coco_bbox_from_via3_polygon(via3_xy):
    assert via3_xy[0] == VIA3RegionShape.POLYGON
    x = min(via3_xy[1::2])
    y = min(via3_xy[2::2])
    x_max = max(via3_xy[1::2])
    y_max = max(via3_xy[2::2])
    bbox_f = [x, y, x_max - x, y_max - y]
    return [round(x) for x in bbox_f]


def coco_bbox_from_via3_rectangle(via3_xy):
    assert via3_xy[0] == VIA3RegionShape.RECTANGLE
    return [round(x) for x in via3_xy[1:]]


def coco_segm_from_via3_polygon(via3_xy):
    assert via3_xy[0] == VIA3RegionShape.POLYGON
    return [
        [round(x) for x in via3_xy[1:]],
    ]


def coco_segm_from_via3_rectangle(via3_xy):
    assert via3_xy[0] == VIA3RegionShape.RECTANGLE
    segm_f = [
        via3_xy[1],
        via3_xy[2],
        via3_xy[1] + via3_xy[3],
        via3_xy[2],
        via3_xy[1] + via3_xy[3],
        via3_xy[2] + via3_xy[4],
        via3_xy[1],
        via3_xy[2] + via3_xy[4],
    ]
    return [
        [round(x) for x in segm_f],
    ]


def coco_area_from_segmentation(segmentation, coco_img):
    rle_mask = pycocotools.mask.frPyObjects(
        segmentation, coco_img["height"], coco_img["width"]
    )
    return round(pycocotools.mask.area(rle_mask)[0])


## TODO: a via3 module to handle this for us.
def coco_dict_from_via3_dict(
    via3_dict: str,
    image_basedir: str,
    category_attribute: str,
) -> Dict:
    if any([len(x["fid_list"]) != 1 for x in via3_dict["view"].values()]):
        raise Exception("VIA3 multi-file views are incompatible with COCO")

    if any([k != v["fid"] for k, v in via3_dict["file"].items()]):
        raise Exception("VIA3 file key differs from its fid")

    if category_attribute not in via3_dict["attribute"]:
        raise Exception(f"Attribute '{category_attribute}' not present")

    via3_attr = via3_dict["attribute"][category_attribute]
    if via3_attr["anchor_id"] != "FILE1_Z0_XY1":
        raise Exception(
            f"'{category_attribute}' is not an image region attribute"
        )
    if via3_attr["type"] not in [
        VIA3AttributeType.RADIO,
        VIA3AttributeType.SELECT,
    ]:
        raise Exception(
            f"'{category_attribute}' is not of 'radio' or 'select' type "
        )
    via3_attr_options = via3_attr["options"]

    coco = empty_coco()
    coco["info"]["description"] = via3_dict["project"]["pname"]

    via3_attr_key_to_coco_cat_id: Dict[str, int] = {}
    for cat_id, (via3_key, cat_name) in enumerate(via3_attr_options.items()):
        coco["categories"].append(
            {
                "id": cat_id,
                "name": cat_name,
                "supercategory": cat_name,  # it is its own supercategory
            }
        )
        via3_attr_key_to_coco_cat_id[via3_key] = cat_id

    ## We checked that all views are single-file views, but we don't
    ## know the view-to-file map and we don't know if all files have a
    ## view (files without a view are not displayed).
    via3_vid_to_coco_img_id: Dict[str, int] = {}
    for img_id, via3_vid in enumerate(via3_dict["project"]["vid_list"]):
        via3_view = via3_dict["view"][via3_vid]
        via3_fid = via3_view["fid_list"][0]
        via3_file = via3_dict["file"][via3_fid]
        if via3_file["type"] != VIA3FileType.IMAGE:
            raise Exception(
                f"File '{via3_file['fname']}' (fid {via3_file['fid']})"
                f" is of type {via3_file['type']} (not an image)"
            )
        if via3_file["loc"] == VIA3FileLoc.INLINE:
            raise Exception(
                f"File '{via3_file['fname']}' (fid {via3_file['fid']})"
                f" is an inline image (not COCO compatible)"
            )

        ## TODO: support images available online
        fpath = (
            via3_dict["config"]["file"]["loc_prefix"][str(via3_file["loc"])]
            + via3_file["src"]
        )  # apply location prefix, if any, first
        img_fpath = os.path.join(image_basedir, fpath)

        pil_img = PIL.Image.open(img_fpath)
        coco["images"].append(
            {
                "id": img_id,
                "width": pil_img.width,
                "height": pil_img.height,
                "file_name": fpath,  # do not include image_basedir
            }
        )
        via3_vid_to_coco_img_id[via3_vid] = img_id

    for ann_id, via3_ann in enumerate(via3_dict["metadata"].values()):
        try:
            coco_img_id = via3_vid_to_coco_img_id[via3_ann["vid"]]
        except KeyError:
            _logger.warning(
                "Skipping annotation referring unknown view: %s", via3_ann
            )
            continue
        try:
            via3_xy = via3_ann["xy"]
        except KeyError:
            _logger.warning(
                "Skipping annotation without 'xy' field: %s", via3_ann
            )
            continue
        try:
            via3_class_attr = via3_ann["av"][category_attribute]
        except KeyError:
            _logger.warning(
                "Skipping annotation without value for attribute '%s': %s",
                category_attribute,
                via3_ann,
            )
            continue
        try:
            coco_ann_id = via3_attr_key_to_coco_cat_id[via3_class_attr]
        except KeyError:
            _logger.warning(
                "Skipping annotation referring invalid attribute option: %s",
                via3_ann,
            )
            continue

        via3_shape_type = int(via3_xy[0])
        if via3_shape_type == VIA3RegionShape.POLYGON:
            coco_segm = coco_segm_from_via3_polygon(via3_xy)
            coco_bbox = coco_bbox_from_via3_polygon(via3_xy)
            coco_area = coco_area_from_segmentation(
                coco_segm, coco["images"][coco_img_id]
            )
        elif via3_shape_type == VIA3RegionShape.RECTANGLE:
            coco_segm = coco_segm_from_via3_rectangle(via3_xy)
            coco_bbox = coco_bbox_from_via3_rectangle(via3_xy)
            coco_area = coco_bbox[2] * coco_bbox[3]
        else:
            _logger.warning(
                "Skipping annotation with xy type %d (no rect or polygon)",
                via3_shape_type,
            )
            continue

        coco["annotations"].append(
            {
                "id": ann_id,
                "image_id": coco_img_id,
                "segmentation": coco_segm,
                "area": coco_area,
                "bbox": coco_bbox,
                "iscrowd": 0,
                "category_id": coco_ann_id,
            }
        )

    return coco


def main_from_via3(
    via3_project_fpath: str,
    image_basedir: str,
    category_attribute: str,
) -> int:
    """Entry point for the "via.coco from-via3 program.

    Refer to `python3 -m via.coco from-via3 -h` for description of this
    function arguments.

    """
    with open(via3_project_fpath, "rb") as fh:
        via3_dict = json.load(fh)
    try:
        coco_dict = coco_dict_from_via3_dict(
            via3_dict,
            image_basedir=image_basedir,
            category_attribute=category_attribute,
        )
    except Exception as ex:
        _logger.error(ex)
        return 1
    json.dump(coco_dict, fp=sys.stdout)
    return 0


def main_to_lisa(
    coco_data_fpath: str,
    *,
    coco_results_fpath: Optional[str],
    category_type: str,
    items_per_page: int,
    ignore_category: bool,
    filepath_prefix: str,
) -> int:
    """Entry point for the "via.coco to-lisa" program.

    Refer to `python3 -m via.coco to-lisa -h` to description of this
    function arguments.

    """
    is_results = coco_results_fpath is not None

    try:
        ## Throw away pycocotools stdout.  pycocotools prints progress
        ## to stdout which our own stdout to be a JSON file.
        with contextlib.redirect_stdout(open(os.devnull, "w")):
            coco = pycocotools.coco.COCO(coco_data_fpath)
    except Exception as ex:
        logging.error(
            "Failed to load COCO data file '%s': %s", coco_data_fpath, ex
        )
        return 1

    if is_results:
        ## COCO.loadRes does not keep the data file 'info' (see
        ## https://github.com/ppwwyyxx/cocoapi/pull/26).  We need that
        ## 'info' for the LISA description field.  Because of this, we
        ## have coco and coco_data variables.
        coco_data = coco
        try:
            ## Throw away pycocotools stdout.
            with contextlib.redirect_stdout(open(os.devnull, "w")):
                coco = coco_data.loadRes(coco_results_fpath)
        except Exception as ex:
            logging.error(
                "Failed to load COCO results file '%s': %s",
                coco_results_fpath,
                ex,
            )
            return 1
        coco.dataset["info"] = coco_data.dataset["info"]

    lisa = via.lisa.LISA()
    lisa.project_name = coco.dataset["info"]["description"]
    lisa.image_filepath_prefix = filepath_prefix

    lisa.define_file_attribute("width", via.lisa.LISALabelAttribute("Width"))
    lisa.define_file_attribute("height", via.lisa.LISALabelAttribute("Height"))

    if not ignore_category:
        attr_lisa_type_to_py_type = {
            "radio": via.lisa.LISARadioAttribute,
            "select": via.lisa.LISASelectAttribute,
        }
        coco_categories = coco.loadCats(coco.getCatIds())
        category_attr = attr_lisa_type_to_py_type[category_type](
            aname="Category",
            options={str(x["id"]): x["name"] for x in coco_categories},
        )
        lisa.define_region_attribute("category", category_attr)

    if is_results:
        lisa.define_region_attribute(
            "score", via.lisa.LISALabelAttribute(aname="Score")
        )

    for image in coco.loadImgs(coco.getImgIds()):
        img_id = str(image["id"])
        lisa.append_image(img_id, image["file_name"])
        lisa.set_file_attribute(img_id, "width", str(image["width"]))
        lisa.set_file_attribute(img_id, "height", str(image["height"]))

    ## XXX: for LISA, it may be more efficient to insert the
    ## annotations at the same time as the images.
    for annotation in coco.loadAnns(coco.getAnnIds()):
        img_id = str(annotation["image_id"])
        region_id = str(annotation["id"])
        attr_id = str(annotation["category_id"])

        rect = via.lisa.LISARect(
            x=float(annotation["bbox"][0]),
            y=float(annotation["bbox"][1]),
            w=float(annotation["bbox"][2]),
            h=float(annotation["bbox"][3]),
        )
        lisa.add_region(img_id, region_id, rect)
        if not ignore_category:
            lisa.set_region_attribute(region_id, "category", attr_id)
        if is_results:
            lisa.set_region_attribute(
                region_id, "score", str(annotation["score"])
            )

    if items_per_page < 1:
        lisa.items_per_page = len(coco.getImgIds())
    else:
        lisa.items_per_page = items_per_page

    json.dump(lisa, fp=sys.stdout, default=via.lisa.LISA.json_encoder)
    return 0


def main(argv: List[str]) -> int:
    logging.basicConfig()
    parser = argparse.ArgumentParser(
        prog="via.coco",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Programs to convert between COCO and VIA file formats",
        epilog=(
            "These programs handle both COCO data and results files."
            " Data files are a single files that include both image"
            " and annotations..  Data files are typically used to"
            " define a dataset or for ground truth annotations."
            "  Result files are a separate file that lists only"
            " annotations and need to be paired with a data files"
            " that lists the corresponding image data.  Format"
            " specification for data and results files are described"
            " at https://cocodataset.org/#format-data and"
            " https://cocodataset.org/#format-results respectively.\n"
            "\n"
            "To convert results files, pass the data file as the"
            " final argument and the results file as the argument to"
            " the `--with-results` option.\n"
            "\n"
            "\n"
            "These programs only handle COCO files for object"
            " detection.  At least for now."
        ),
    )
    subparsers = parser.add_subparsers(dest="action")

    from_via3_subparser = subparsers.add_parser(
        "from-via3",
        help="Convert VIA3 project file into a COCO *data* file",
    )
    from_via3_subparser.add_argument(
        "--category-attribute",
        default="category",
        help=(
            "Name of the VIA3 attribute from where to select an annotation"
            " category.  Must be an attribute of type 'radio' or 'select'."
        ),
    )
    from_via3_subparser.add_argument(
        "--image-basedir",
        default="",
        help=(
            "Directory where image files can be accessed, before any"
            " any file location prefix is applied.  Defaults to the"
            " empty string, meaning current/working directory.\n"
            "\n"
            "This is needed because COCO data files include the image"
            " width and height but a VIA3 project does not.  Image"
            " files are read to get their width and height.\n"
            "\n"
            "Non-local images are not yet supported."
        ),
    )
    from_via3_subparser.add_argument(
        "via3_project",
        metavar="VIA3-PROJECT",
        help="Filepath for the VIA3 project.",
    )

    to_lisa_subparser = subparsers.add_parser(
        "to-lisa",
        help="Convert COCO *data* file into a LISA project",
    )
    to_lisa_subparser.add_argument(
        "--category-type",
        choices=["radio", "select"],
        default="radio",
        help=(
            "Type to display the COCO category in LISA.  'radio' for radio"
            " buttons; 'select' for dropdown list."
        ),
    )
    to_lisa_subparser.add_argument(
        "--items-per-page",
        metavar="NUM",
        type=int,
        default=100,
        help=(
            "Number of images to show by default in LISA.  Use a non-positive"
            " number to display all images by default.  This is the 'm'"
            " keyboard shortcut in LISA."
        ),
    )
    to_lisa_subparser.add_argument(
        "--filepath-prefix",
        default="",
        help=(
            "Prefix to the image filepaths.  This is the 'f' keyboard shortcut"
            " in LISA."
        ),
    )
    to_lisa_subparser.add_argument(
        "--ignore-category",
        action="store_true",
        help=(
            "If set, the annotations category is ignored.  Effectively,"
            " this means that it creates a LISA project with only the"
            " regions/bboxes."
        ),
    )
    to_lisa_subparser.add_argument(
        "--with-results",
        metavar="COCO_RESULTS",
        dest="coco_results",
        default=None,
        help=(
            "Filepath for a COCO results file.  It should describe"
            " results for the COCO_DATA file."
        ),
    )
    to_lisa_subparser.add_argument(
        "coco_data",
        metavar="COCO_DATA",
        help="Filepath for the COCO data file.",
    )

    args = parser.parse_args(argv[1:])
    if args.action == "from-via3":
        return main_from_via3(
            args.via3_project,
            image_basedir=args.image_basedir,
            category_attribute=args.category_attribute,
        )
    elif args.action == "to-lisa":
        return main_to_lisa(
            args.coco_data,
            coco_results_fpath=args.coco_results,
            category_type=args.category_type,
            items_per_page=args.items_per_page,
            ignore_category=args.ignore_category,
            filepath_prefix=args.filepath_prefix,
        )
    else:
        # We should not get here because `parse_args` should error on
        # unknown actions.
        raise Exception(f"Unknown action {args.action}")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
