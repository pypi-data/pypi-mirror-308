# py_iec61850_cdc abstracts.py
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

# This file provides the abstract base classes described in
# IEC 61850-7-2:2010+AMD1:2020 CSV and IEC 61850-7-3:2010+AMD1:2020 CSV
# as Python ABCs.

from typing import Literal
from abc import ABC
from pydantic import BaseModel, ConfigDict, Field

from .basetypes import (
    BOOLEAN,
    INT32,
    INT32_MIN_VALUE,
    INT32_MAX_VALUE,
    field_int32,
    INT8U,
    INT8U_MIN_VALUE,
    INT8U_MAX_VALUE,
    field_int8u,
    INT16U,
    INT16U_MIN_VALUE,
    INT16U_MAX_VALUE,
    field_int16u,
    INT32U,
    INT32U_MIN_VALUE,
    INT32U_MAX_VALUE,
    field_int32u,
    FLOAT32,
    FLOAT32_MIN_VALUE,
    FLOAT32_MAX_VALUE,
    field_float32,
    ObjectReference,
    field_objectreference,
    Unicode255,
    field_unicode255,
    VisString64,
    field_visstring64,
    VisString255,
    field_visstring255
)

from .enums import (
    CtlModelKind,
    EnumDA,
    HvReferenceKind,
    SboClassKind
)

from .attributes import (
    AnalogueValue,
    Originator,
    Quality,
    ScaledValueConfig,
    Timestamp,
    Unit
)

# IEC 61850-7-3 7.2.2
class BasePrimitiveCDC(ABC, BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    cdc_name: VisString255 = Field(default = 'BasePrimitiveCDC',
                                   pattern = 'BasePrimitiveCDC',
                                   alias   = 'cdcName')
    d:        VisString255 = field_visstring255(default = "",
                                                alias   = "d")
    du:       Unicode255   = field_unicode255(default = "",
                                              alias   = "dU")
    data_ns:  VisString255 = field_visstring255(default = "",
                                                alias   = "dataNs")

# IEC 61850-7-3 7.2.3
class BaseComposedCDC(ABC, BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    cdc_name: VisString255 = Field(default = 'BaseComposedCDC',
                                   pattern = 'BaseComposedCDC',
                                   alias   = 'cdcName')
    d:        VisString255 = field_visstring255(default = "",
                                                alias   = "d")
    du:       Unicode255   = field_unicode255(default = "",
                                              alias   = "dU")
    data_ns:  VisString255 = field_visstring255(default = "",
                                                alias   = "dataNs")

# IEC 61850-7-3 7.2.4
class SubstitutionCDC(BasePrimitiveCDC):
    model_config = ConfigDict(validate_assignment = True)
    cdc_name: VisString255 = Field(default = 'SubstitutionCDC',
                                   pattern = 'SubstitutionCDC',
                                   alias   = 'cdcName')
    sub_q:    Quality      = Field(default_factory = Quality,
                                   alias   = "subQ")
    sub_id:   VisString64  = field_visstring64(default = "",
                                               alias   = "subID")
    sub_ena:  BOOLEAN      = Field(default = False,
                                   alias   = "subEna")
    blk_ena:  BOOLEAN      = Field(default = False,
                                   alias   = "blkEna")

# IEC 61850-7-3 7.7.2.2
class ASG(BasePrimitiveCDC, ABC):
    cdc_name:  VisString255      = Field(default = 'ASG',
                                         pattern = 'ASG',
                                         alias   = 'cdcName')
    units:     Unit              = Field(default_factory = Unit,
                                         alias           = "units")
    svc:       ScaledValueConfig = Field(default_factory = ScaledValueConfig,
                                         alias           = "sVC")
    min_val:   AnalogueValue     = Field(default_factory = AnalogueValue,
                                         alias           = "minVal")
    max_val:   AnalogueValue     = Field(default_factory = AnalogueValue,
                                         alias           = "maxVal")
    step_size: AnalogueValue     = Field(default_factory = AnalogueValue,
                                         alias           = "stepSize")

# IEC 61850-7-3 7.4.2
class HarmonicMeasurandCDC(BaseComposedCDC, ABC):
    cdc_name:  VisString255    = Field(default = 'HarmonicMeasurandCDC',
                                       pattern = 'HarmonicMeasurandCDC',
                                       alias   = 'cdcName')
    num_har:   INT16U          = field_int16u(default = 0,
                                              minimum = INT16U_MIN_VALUE,
                                              maximum = INT16U_MAX_VALUE,
                                              alias   = "numHar")
    num_cyc:   INT16U          = field_int16u(default = 0,
                                              minimum = INT16U_MIN_VALUE,
                                              maximum = INT16U_MAX_VALUE,
                                              alias   = "numCyc")
    eval_tm:   INT16U          = field_int16u(default = 0,
                                              minimum = INT16U_MIN_VALUE,
                                              maximum = INT16U_MAX_VALUE,
                                              alias   = "evalTm")
    smp_rate:  INT32U          = field_int32u(default = 0,
                                              minimum = INT32U_MIN_VALUE,
                                              maximum = INT32U_MAX_VALUE,
                                              alias   = "smpRate")
    frequency: FLOAT32         = field_float32(default = 0.0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "frequency")
    hv_ref:    HvReferenceKind = Field(default = HvReferenceKind.rms,
                                       alias   = "hvRef")
    rms_cyc:   INT16U          = field_int16u(default = 0,
                                              minimum = INT16U_MIN_VALUE,
                                              maximum = INT16U_MAX_VALUE,
                                              alias   = "rmsCyc")
    maxpts:    INT16U          = field_int16u(default = 0,
                                              minimum = INT16U_MIN_VALUE,
                                              maximum = INT16U_MAX_VALUE,
                                              alias   = "maxPts")

# IEC 61850-7-3 7.5.2
class ControlTestingCDC(SubstitutionCDC, ABC):
    cdc_name: VisString255 = Field(default = 'ControlTestingCDC',
                                   pattern = 'ControlTestingCDC',
                                   alias   = 'cdcName')
    op_rcvd:  BOOLEAN      = Field(default = False,
                                   alias   = "opRcvd")
    op_ok:    BOOLEAN      = Field(default = False,
                                   alias   = "opOk")
    t_op_ok:  Timestamp    = Field(default_factory = Timestamp,
                                   alias   = "tOpOk")

# IEC 61850-7-3 7.7.4.2
class CSG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'CSG',
                                   pattern = 'CSG',
                                   alias   = 'cdcName')
    x_units:  Unit         = Field(default_factory = Unit,
                                   alias           = "xUnits")
    y_units:  Unit         = Field(default_factory = Unit,
                                   alias           = "yUnits")
    z_units:  Unit         = Field(default_factory = Unit,
                                   alias           = "zUnits")
    max_pts:  INT16U       = field_int16u(default = 1,
                                          alias   = "maxPts")
    xd:       VisString255 = field_visstring255(default = "",
                                                alias   = "xD")
    xdu:      Unicode255   = field_unicode255(default = "",
                                              alias   = "xDU")
    yd:       VisString255 = field_visstring255(default = "",
                                                alias   = "yD")
    ydu:      Unicode255   = field_unicode255(default = "",
                                              alias   = "yDU")
    zd:       VisString255 = field_visstring255(default = "",
                                                alias   = "zD")
    zdu:      Unicode255   = field_unicode255(default = "",
                                              alias   = "zDU")

# IEC 61850-7-3 7.6.7.2
class CUG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'CUG',
                                   pattern = 'CUG',
                                   alias   = 'cdcName')

# IEC 61850-7-3 7.7.3.2
class CURVE(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'CURVE',
                                   pattern = 'CURVE',
                                   alias   = 'cdcName')

# IEC 61850-7-3 7.5.6
class ENC(ControlTestingCDC, ABC):
    cdc_name:     VisString255 = Field(default = 'ENC',
                                       pattern = 'ENC',
                                       alias   = 'cdcName')
    origin:       Originator   = Field(default_factory = Originator,
                                       alias           = "origin")
    ctl_num:      INT8U        = field_int8u(default = 0,
                                             minimum = INT8U_MIN_VALUE,
                                             maximum = INT8U_MAX_VALUE,
                                             alias   = "ctlNum")
    st_val:       EnumDA       = Field(default = 0,
                                       alias   = "stVal") # Not sure what to do here.
    q:            Quality      = Field(default_factory = Quality,
                                       alias           = "q")
    t:            Timestamp    = Field(default_factory = Timestamp,
                                       alias           = "t")
    st_seld:      BOOLEAN      = Field(default = False,
                                       alias   = "stSeld")
    sub_val:      EnumDA       = Field(default = 0,
                                       alias   = "subVal") # Not sure what to do here.
    ctl_model:    CtlModelKind = Field(default = CtlModelKind.status_only,
                                       alias   = "ctlModel")
    sbo_timeout:  INT32U       = field_int32u(default = 0,
                                              minimum = INT32U_MIN_VALUE,
                                              maximum = INT32U_MAX_VALUE,
                                              alias   = "sboTimeout")
    sbo_class:    SboClassKind = Field(default = SboClassKind.operate_once,
                                       alias   = "sboClass")
    oper_timeout: INT32U       = field_int32u(default = 0,
                                              minimum = INT32U_MIN_VALUE,
                                              maximum = INT32U_MAX_VALUE,
                                              alias   = "operTimeout")
    ctl_val:      EnumDA       = Field(default = 0,
                                       alias   = "ctlVal") # Not sure what to do here.

# IEC 61850-7-3 7.6.4.2
class ENG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'ENG',
                                   pattern = 'ENG',
                                   alias   = 'cdcName')

# IEC 61850-7-3 7.6.3.2
class ING(BasePrimitiveCDC, ABC):
    cdc_name:  VisString255 = Field(default = 'ING',
                                    pattern = 'ING',
                                    alias   = 'cdcName')
    min_val:   INT32        = field_int32(default = INT32_MIN_VALUE,
                                          minimum = INT32_MIN_VALUE,
                                          maximum = INT32_MAX_VALUE,
                                          alias   = "minVal")
    max_val:   INT32        = field_int32(default = INT32_MAX_VALUE,
                                          minimum = INT32_MIN_VALUE,
                                          maximum = INT32_MAX_VALUE,
                                          alias   = "maxVal")
    step_size: INT32U       = field_int32u(default = 1,
                                           minimum = INT32U_MIN_VALUE,
                                           maximum = INT32U_MAX_VALUE,
                                           alias   = "stepSize")
    units:     Unit         = Field(default_factory = Unit,
                                    alias           = "units")

# IEC 61850-7-3 7.6.5.2
class ORG(BasePrimitiveCDC, ABC):
    cdc_name:    VisString255    = Field(default = 'ORG',
                                         pattern = 'ORG',
                                         alias   = 'cdcName')
    set_src_ref: ObjectReference = field_objectreference(default = "",
                                                         alias   = "setSrcRef")
    set_tst_ref: ObjectReference = field_objectreference(default = "",
                                                         alias   = "setTstRef")
    set_src_cb:  ObjectReference = field_objectreference(default = "",
                                                         alias   = "setSrcCB")
    set_tst_cb:  ObjectReference = field_objectreference(default = "",
                                                         alias   = "setTstCB")
    int_addr:    VisString255    = field_visstring255(default = "",
                                                      alias   = "intAddr")
    tst_ena:     BOOLEAN         = Field(default = False,
                                         alias   = "tstEna")
    purpose:     VisString255    = field_visstring255(default = "",
                                                      alias   = "purpose")

# IEC 61850-7-3 7.6.2.2
class SPG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'SPG',
                                   pattern = 'SPG',
                                   alias   = 'cdcName')

# IEC 61850-7-3 7.6.8.3
class VSG(BasePrimitiveCDC, ABC):
    cdc_name: VisString255 = Field(default = 'VSG',
                                   pattern = 'VSG',
                                   alias   = 'cdcName')

