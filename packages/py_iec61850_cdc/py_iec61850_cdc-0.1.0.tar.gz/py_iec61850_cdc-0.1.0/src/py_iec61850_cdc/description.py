# py_iec61850_cdc cdc_description.py
# Copyright 2024 Kyle Hawkings
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Follows PEP-8 rules on function / variable naming (e.g. underscores).

# This file provides the description CDCs described under Clause 7.8 of
# IEC 61850-7-3:2010+AMD1:2020 CSV as Python dataclasses.

from pydantic import Field

from .basetypes import (
    INT32,
    INT32_MIN_VALUE,
    INT32_MAX_VALUE,
    field_int32,
    FLOAT32,
    FLOAT32_MIN_VALUE,
    FLOAT32_MAX_VALUE,
    field_float32,
    INT16U,
    INT16U_MIN_VALUE,
    INT16U_MAX_VALUE,
    field_int16u,
    VisString64,
    field_visstring64,
    VisString255,
    field_visstring255,
    Unicode255,
    field_unicode255
)

from .attributes import (
    Point,
    Unit
)

from .abstracts import (
    BasePrimitiveCDC
)

# IEC 61850-7-3 7.8.2
class DPL(BasePrimitiveCDC):
    cdc_name:    VisString255 = Field(default = 'DPL',
                                      pattern = 'DPL',
                                      alias   = 'cdcName')
    vendor:      VisString255 = field_visstring255(default = "",
                                                   alias   = "vendor")
    hw_rev:      VisString255 = field_visstring255(default = "",
                                                   alias   = "hwRev")
    sw_rev:      VisString255 = field_visstring255(default = "",
                                                   alias   = "swRev")
    ser_num:     VisString255 = field_visstring255(default = "",
                                                   alias   = "serNum")
    model:       VisString255 = field_visstring255(default = "",
                                                   alias   = "model")
    location:    VisString255 = field_visstring255(default = "",
                                                   alias   = "location")
    name:        VisString64  = field_visstring64(default = "",
                                                  alias   = "name")
    owner:       VisString255 = field_visstring255(default = "",
                                                   alias   = "owner")
    eps_name:    VisString255 = field_visstring255(default = "",
                                                   alias   = "ePSName")
    prime_oper:  VisString255 = field_visstring255(default = "",
                                                   alias   = "primeOper")
    second_oper: VisString255 = field_visstring255(default = "",
                                                   alias   = "secondOper")
    latitude:    FLOAT32      = field_float32(default = 0,
                                              minimum = FLOAT32_MIN_VALUE,
                                              maximum = FLOAT32_MAX_VALUE,
                                              alias   = "latitude")
    longitude:   FLOAT32      = field_float32(default = 0,
                                              minimum = FLOAT32_MIN_VALUE,
                                              maximum = FLOAT32_MAX_VALUE,
                                              alias   = "longitude")
    altitude:    FLOAT32      = field_float32(default = 0,
                                              minimum = FLOAT32_MIN_VALUE,
                                              maximum = FLOAT32_MAX_VALUE,
                                              alias   = "altitude")
    mrid:        VisString255 = field_visstring255(default = "",
                                                   alias   = "mRID")

# IEC 61850-7-3 7.8.3
class LPL(BasePrimitiveCDC):
    cdc_name:   VisString255 = Field(default = 'LPL',
                                     pattern = 'LPL',
                                     alias   = 'cdcName')
    param_rev:  INT32        = field_int32(default = 0,
                                           minimum = INT32_MIN_VALUE,
                                           maximum = INT32_MAX_VALUE,
                                           alias   = "paramRev")
    val_rev:    INT32        = field_int32(default = 0,
                                           minimum = INT32_MIN_VALUE,
                                           maximum = INT32_MAX_VALUE,
                                           alias   = "valRev")
    vendor:     VisString255 = field_visstring255(default = "",
                                                  alias   = "vendor")
    sw_rev:     VisString255 = field_visstring255(default = "",
                                                  alias   = "swRev")
    lnns:       VisString255 = field_visstring255(default = "",
                                                  alias   = "ldNs")
    config_rev: VisString255 = field_visstring255(default = "",
                                                  alias   = "configRev")

# IEC 61850-7-3 7.8.4
class CSD(BasePrimitiveCDC):
    cdc_name: VisString255 = Field(default = 'CSD',
                                   pattern = 'CSD',
                                   alias   = 'cdcName')
    x_units:  Unit         = Field(default_factory = Unit,
                                   alias           = "xUnits")
    xd:       VisString255 = field_visstring255(default = "",
                                                alias   = "xD")
    xdu:      Unicode255   = field_visstring255(default = "",
                                                alias   = "xDU")
    y_units:  Unit         = Field(default_factory = Unit,
                                   alias           = "yUnits")
    yd:       VisString255 = field_visstring255(default = "",
                                                alias   = "yD")
    ydu:      Unicode255   = field_visstring255(default = "",
                                                alias   = "yDU")
    z_units:  Unit         = Field(default_factory = Unit,
                                   alias           = "zUnits")
    zd:       VisString255 = field_visstring255(default = "",
                                                alias   = "zD")
    zdu:      Unicode255   = field_visstring255(default = "",
                                                alias   = "zDU")
    num_pts:  INT16U       = field_int16u(default = 0,
                                          minimum = INT16U_MIN_VALUE,
                                          maximum = INT16U_MAX_VALUE,
                                          alias   = "numPts")
    crv_pts:  list[Point]  = None
    max_pts:  INT16U       = field_int16u(default = 0,
                                          minimum = INT16U_MIN_VALUE,
                                          maximum = INT16U_MAX_VALUE,
                                          alias   = "maxPts")

# IEC 61850-7-3 7.8.5
class VSD(BasePrimitiveCDC):
    cdc_name: VisString255 = Field(default = 'VSD',
                                   pattern = 'VSD',
                                   alias   = 'cdcName')
    val:      VisString255 = field_visstring255(default = "",
                                                alias   = "val")

