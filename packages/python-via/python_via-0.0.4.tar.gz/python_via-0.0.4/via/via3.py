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

"""Tools to handle VIA3 project files.
"""

import enum


class VIA3AttributeType(enum.IntEnum):
    TEXT = 1
    CHECKBOX = 2
    RADIO = 3
    SELECT = 4
    IMAGE = 5


class VIA3FileType(enum.IntEnum):
    IMAGE = 2
    VIDEO = 4
    AUDIO = 8


class VIA3FileLoc(enum.IntEnum):
    LOCAL = 1
    URIHTTP = 2
    URIFILE = 3
    INLINE = 4


class VIA3RegionShape(enum.IntEnum):
    POINT = 1
    RECTANGLE = 2
    CIRCLE = 3
    ELLIPSE = 4
    LINE = 5
    POLYLINE = 6
    POLYGON = 7
    EXTREME_RECTANGLE = 8
    EXTREME_CIRCLE = 9
