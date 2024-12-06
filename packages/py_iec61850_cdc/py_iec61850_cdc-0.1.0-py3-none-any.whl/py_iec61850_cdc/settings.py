# py_iec61850_cdc settings.py
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

# This file provides the settings classes described in
# IEC 61850-7-2:2010+AMD1:2020 CSV and IEC 61850-7-3:2010+AMD1:2020 CSV
# as Python ABCs.

from pydantic import Field

from .basetypes import (
    BOOLEAN,
    INT32,
    INT32_MIN_VALUE,
    INT32_MAX_VALUE,
    field_int32,
    INT16U,
    INT16U_MIN_VALUE,
    INT16U_MAX_VALUE,
    field_int16u,
    FLOAT32,
    FLOAT32_MIN_VALUE,
    FLOAT32_MAX_VALUE,
    field_float32,
    VisString255,
    field_visstring255,
    Currency,
    field_currency
)

from .enums import (
    CurveCharKind,
    EnumDA
)

from .attributes import (
    AnalogueValueCtl,
    Point
)

from .abstracts import (
    ASG,
    CSG,
    CUG,
    CURVE,
    ENG,
    ING,
    SPG,
    VSG
)

# IEC 61850-7-3 7.7.2.3
class ASG_SP(ASG):
    cdc_name: VisString255     = Field(default = 'ASG_SP',
                                       pattern = 'ASG_SP',
                                       alias   = 'cdcName')
    set_mag:  AnalogueValueCtl = Field(default_factory = AnalogueValueCtl,
                                       alias           = "setMag")

# IEC 61850-7-3 7.7.2.4
class ASG_SG(ASG):
    cdc_name: VisString255     = Field(default = 'ASG_SG',
                                       pattern = 'ASG_SG',
                                       alias   = 'cdcName')
    set_mag: AnalogueValueCtl = Field(default_factory = AnalogueValueCtl,
                                      alias           = "setMag")

# IEC 61850-7-3 7.7.2.5
class ASG_SE(ASG):
    cdc_name: VisString255     = Field(default = 'ASG_SE',
                                       pattern = 'ASG_SE',
                                       alias   = 'cdcName')
    set_mag: AnalogueValueCtl = Field(default_factory = AnalogueValueCtl,
                                      alias           = "setMag")

# IEC 61850-7-3 7.7.4.3
class CSG_SP(CSG):
    cdc_name: VisString255     = Field(default = 'CSG_SP',
                                       pattern = 'CSG_SP',
                                       alias   = 'cdcName')
    point_z: FLOAT32     = field_float32(default = 0,
                                         minimum = FLOAT32_MIN_VALUE,
                                         maximum = FLOAT32_MAX_VALUE,
                                         alias   = "pointZ")
    num_pts: INT16U      = field_int16u(default = 0,
                                        minimum = INT16U_MIN_VALUE,
                                        maximum = INT16U_MAX_VALUE,
                                        alias   = "numPts")
    crv_pts: list[Point] = None

# IEC 61850-7-3 7.7.4.4
class CSG_SG(CSG):
    cdc_name: VisString255     = Field(default = 'CSG_SG',
                                       pattern = 'CSG_SG',
                                       alias   = 'cdcName')
    point_z: FLOAT32     = field_float32(default = 0,
                                         minimum = FLOAT32_MIN_VALUE,
                                         maximum = FLOAT32_MAX_VALUE,
                                         alias   = "pointZ")
    num_pts: INT16U      = field_int16u(default = 0,
                                        minimum = INT16U_MIN_VALUE,
                                        maximum = INT16U_MAX_VALUE,
                                        alias   = "numPts")
    crv_pts: list[Point] = None

# IEC 61850-7-3 7.7.4.5
class CSG_SE(CSG):
    cdc_name: VisString255     = Field(default = 'CSG_SE',
                                       pattern = 'CSG_SE',
                                       alias   = 'cdcName')
    point_z: FLOAT32     = field_float32(default = 0,
                                         minimum = FLOAT32_MIN_VALUE,
                                         maximum = FLOAT32_MAX_VALUE,
                                         alias   = "pointZ")
    num_pts: INT16U      = field_int16u(default = 0,
                                        minimum = INT16U_MIN_VALUE,
                                        maximum = INT16U_MAX_VALUE,
                                        alias   = "numPts")
    crv_pts: list[Point] = None

# IEC 61850-7-3 7.6.7.3
class CUG_SP(CUG):
    cdc_name: VisString255     = Field(default = 'CUG_SP',
                                       pattern = 'CUG_SP',
                                       alias   = 'cdcName')
    cur: Currency = field_currency(default = "XXX",
                                   alias   = "cur")

# IEC 61850-7-3 7.6.7.4
class CUG_SG(CUG):
    cdc_name: VisString255     = Field(default = 'CUG_SG',
                                       pattern = 'CUG_SG',
                                       alias   = 'cdcName')
    cur: Currency = field_currency(default = "XXX",
                                   alias   = "cur")

# IEC 61850-7-3 7.6.7.5
class CUG_SE(CUG):
    cdc_name: VisString255     = Field(default = 'CUG_SE',
                                       pattern = 'CUG_SE',
                                       alias   = 'cdcName')
    cur: Currency = field_currency(default = "XXX",
                                   alias   = "cur")

# IEC 61850-7-3 7.7.3.3
class CURVE_SP(CURVE):
    cdc_name: VisString255     = Field(default = 'CURVE_SP',
                                       pattern = 'CURVE_SP',
                                       alias   = 'cdcName')
    set_charact: CurveCharKind = Field(default = CurveCharKind.none,
                                       alias   = "setCharact")
    set_par_a:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParA")
    set_par_b:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParB")
    set_par_c:   FLOAT32       = field_float32(default = 0, 
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParC")
    set_par_d:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParD")
    set_par_e:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParE")
    set_par_f:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParF")

# IEC 61850-7-3 7.7.3.4
class CURVE_SG(CURVE):
    cdc_name: VisString255     = Field(default = 'CURVE_SG',
                                       pattern = 'CURVE_SG',
                                       alias   = 'cdcName')
    set_charact: CurveCharKind = Field(default = CurveCharKind.none,
                                       alias   = "setCharact")
    set_par_a:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParA")
    set_par_b:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParB")
    set_par_c:   FLOAT32       = field_float32(default = 0, 
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParC")
    set_par_d:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParD")
    set_par_e:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParE")
    set_par_f:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParF")

# IEC 61850-7-3 7.7.3.5
class CURVE_SE(CURVE):
    cdc_name: VisString255     = Field(default = 'CURVE_SE',
                                       pattern = 'CURVE_SE',
                                       alias   = 'cdcName')
    set_charact: CurveCharKind = Field(default = CurveCharKind.none,
                                       alias   = "setCharact")
    set_par_a:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParA")
    set_par_b:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParB")
    set_par_c:   FLOAT32       = field_float32(default = 0, 
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParC")
    set_par_d:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParD")
    set_par_e:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParE")
    set_par_f:   FLOAT32       = field_float32(default = 0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "setParF")

# IEC 61850-7-3 7.6.4.3
class ENG_SP(ENG):
    cdc_name: VisString255     = Field(default = 'CMV',
                                       pattern = 'CMV',
                                       alias   = 'ENG_SP')
    set_val: EnumDA = Field(default_factory = EnumDA,
                            alias           = "setVal")

# IEC 61850-7-3 7.6.4.4
class ENG_SG(ENG):
    cdc_name: VisString255     = Field(default = 'ENG_SG',
                                       pattern = 'ENG_SG',
                                       alias   = 'cdcName')
    set_val: EnumDA = Field(default_factory = EnumDA,
                            alias           = "setVal")

# IEC 61850-7-3 7.6.4.5
class ENG_SE(ENG):
    cdc_name: VisString255     = Field(default = 'ENG_SE',
                                       pattern = 'ENG_SE',
                                       alias   = 'cdcName')
    set_val: EnumDA = Field(default_factory = EnumDA,
                            alias           = "setVal")

# IEC 61850-7-3 7.6.3.3
class ING_SP(ING):
    cdc_name: VisString255     = Field(default = 'ING_SP',
                                       pattern = 'ING_SP',
                                       alias   = 'cdcName')
    set_val: INT32 = field_int32(default = 0,
                                 minimum = INT32_MIN_VALUE,
                                 maximum = INT32_MAX_VALUE,
                                 alias   = "setVal")

# IEC 61850-7-3 7.6.3.4
class ING_SG(ING):
    cdc_name: VisString255     = Field(default = 'ING_SG',
                                       pattern = 'ING_SG',
                                       alias   = 'cdcName')
    set_val: INT32 = field_int32(default = 0,
                                 minimum = INT32_MIN_VALUE,
                                 maximum = INT32_MAX_VALUE,
                                 alias   = "setVal")

# IEC 61850-7-3 7.6.3.5
class ING_SE(ING):
    cdc_name: VisString255     = Field(default = 'ING_SE',
                                       pattern = 'ING_SE',
                                       alias   = 'cdcName')
    set_val: INT32 = field_int32(default = 0,
                                 minimum = INT32_MIN_VALUE,
                                 maximum = INT32_MAX_VALUE,
                                 alias   = "setVal")

# IEC 61850-7-3 7.6.2.3
class SPG_SP(SPG):
    cdc_name: VisString255     = Field(default = 'SPG_SP',
                                       pattern = 'SPG_SP',
                                       alias   = 'cdcName')
    set_val: BOOLEAN = Field(default = False,
                             alias   = "setVal")

# IEC 61850-7-3 7.6.2.4
class SPG_SG(SPG):
    cdc_name: VisString255     = Field(default = 'SPG_SG',
                                       pattern = 'SPG_SG',
                                       alias   = 'cdcName')
    set_val: BOOLEAN = Field(default = False,
                             alias   = "setVal")

# IEC 61850-7-3 7.6.2.5
class SPG_SE(SPG):
    cdc_name: VisString255     = Field(default = 'SPG_SE',
                                       pattern = 'SPG_SE',
                                       alias   = 'cdcName')
    set_val: BOOLEAN = Field(default = False,
                             alias   = "setVal")

# IEC 61850-7-3 7.6.8.3
class VSG_SP(VSG):
    cdc_name: VisString255     = Field(default = 'VSG_SP',
                                       pattern = 'VSG_SP',
                                       alias   = 'cdcName')
    set_val: VisString255 = field_visstring255(default = "",
                                               alias   = "setVal")

# IEC 61850-7-3 7.6.8.4
class VSG_SG(VSG):
    cdc_name: VisString255     = Field(default = 'VSG_SG',
                                       pattern = 'VSG_SG',
                                       alias   = 'cdcName')
    set_val: VisString255 = field_visstring255(default = "",
                                               alias   = "setVal")

# IEC 61850-7-3 7.6.8.5
class VSG_SE(VSG):
    cdc_name: VisString255     = Field(default = 'VSG_SE',
                                       pattern = 'VSG_SE',
                                       alias   = 'cdcName')
    set_val: VisString255 = field_visstring255(default = "",
                                               alias   = "setVal")

