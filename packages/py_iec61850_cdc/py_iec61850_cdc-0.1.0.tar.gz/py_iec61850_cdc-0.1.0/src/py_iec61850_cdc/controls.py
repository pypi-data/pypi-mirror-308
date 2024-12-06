# py_iec61850_cdc controls.py
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

# This file provides the analog info CDCs described under Clause 7.4 of
# IEC 61850-7-3:2010+AMD1:2020 CSV as Python dataclasses.

from pydantic import Field

from .basetypes import (
    BOOLEAN,
    INT8,
    INT8_MIN_VALUE,
    INT8_MAX_VALUE,
    field_int8,
    INT32,
    INT32_MIN_VALUE,
    INT32_MAX_VALUE,
    field_int32,
    FLOAT32,
    FLOAT32_MIN_VALUE,
    FLOAT32_MAX_VALUE,
    field_float32,
    INT8U,
    INT8U_MIN_VALUE,
    INT8U_MAX_VALUE,
    field_int8u,
    INT32U,
    INT32U_MIN_VALUE,
    INT32U_MAX_VALUE,
    field_int32u,
    VisString255 # field_visstring255 is not used. VisString255 used only for cdc_name.
)

from .enums import (
    CtlModelKind,
    DpStatusKind,
    SboClassKind,
    StepControlKind
)

from .attributes import (
    AnalogueValue,
    AnalogueValueCtl,
    Originator,
    PulseConfig,
    Quality,
    ScaledValueConfig,
    Timestamp,
    Unit,
    ValWithTrans
)

from .abstracts import (
    ControlTestingCDC
)

# IEC 61850-7-3 7.5.3
class SPC(ControlTestingCDC):
    cdc_name:     VisString255 = Field(default = 'SPC',
                                       pattern = 'SPC',
                                       alias   = 'cdcName')
    origin:       Originator   = Field(default_factory = Originator,
                                       alias           = 'origin')
    ctl_num:      INT8U        = field_int8u(default = 0,
                                             minimum = INT8_MIN_VALUE,
                                             maximum = INT8_MAX_VALUE,
                                             alias   = "ctlNum")
    st_val:       BOOLEAN      = Field(default = False
                                       alias   = "stVal")
    q:            Quality      = Field(default_factory = Quality,
                                       alias           = "q")
    t:            Timestamp    = Field(default_factory = Timestamp,
                                       alias           = "t")
    st_seld:      BOOLEAN      = Field(default = False,
                                       alias   = "stSeld")
    pulse_config: PulseConfig  = Field(default_factory = PulseConfig,
                                       alias           = "pulseConfig")
    ctl_model:    CtlModelKind = Field(default = CtlModelKind.direct_with_normal_security,
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
    ctl_val:      BOOLEAN      = Field(default = False,
                                       alias   = "ctlVal")

# IEC 61850-7-3 7.5.4
class DPC(ControlTestingCDC):
    cdc_name:     VisString255 = Field(default = 'DPC',
                                       pattern = 'DPC',
                                       alias   = 'cdcName')
    origin:       Originator   = Field(default_factory = Originator,
                                       alias           = "origin")
    ctl_num:      INT8U        = field_int8u(default = 0,
                                             minimum = INT8U_MIN_VALUE,
                                             maximum = INT8U_MAX_VALUE,
                                             alias   = "ctlNum")
    st_val:       DpStatusKind = Field(default = DpStatusKind.off,
                                       alias   = "stVal")
    q:            Quality      = Field(default_factory = Quality,
                                       alias           = "q")
    t:            Timestamp    = Field(default_factory = Timestamp,
                                       alias           = "t")
    st_seld:      BOOLEAN      = Field(default = False,
                                       alias   = "stSeld")
    sub_val:      DpStatusKind = Field(default = DpStatusKind.off,
                                       alias   = "subVal")
    pulse_config: PulseConfig  = Field(default_factory = PulseConfig,
                                       alias           = "pulseConfig")
    ctl_model:    CtlModelKind = Field(default = CtlModelKind.direct_with_normal_security,
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
    ctl_val:      BOOLEAN      = Field(default = False,
                                       alias   = "ctlVal")

# IEC 61850-7-3 7.5.5
class INC(ControlTestingCDC):
    cdc_name:     VisString255 = Field(default = 'INC',
                                       pattern = 'INC',
                                       alias   = 'cdcName')
    origin:       Originator   = Field(default_factory = Originator,
                                       alias           = "origin")
    ctl_num:      INT8U        = field_int8u(default = 0,
                                             minimum = INT8U_MIN_VALUE,
                                             maximum = INT8U_MAX_VALUE,
                                             alias   = "ctlNum")
    st_val:       INT32        = field_int32(default = 0,
                                             minimum = INT32_MIN_VALUE,
                                             maximum = INT32_MAX_VALUE,
                                             alias   = "stVal")
    q:            Quality      = Field(default_factory = Quality,
                                       alias           = "q")
    t:            Timestamp    = Field(default_factory = Timestamp,
                                       alias           = "t")
    st_seld:      BOOLEAN      = Field(default = False,
                                       alias   = "stSeld")
    sub_val:      INT32        = field_int32(default = 0,
                                             minimum = INT32_MIN_VALUE,
                                             maximum = INT32_MAX_VALUE,
                                             alias   = "subVal")
    ctl_model:    CtlModelKind = Field(default = CtlModelKind.direct_with_normal_security,
                                       alias   = "ctlModel")
    sbo_timeout:  INT32U       = field_int32u(default = 0,
                                              minimum = INT32U_MIN_VALUE,
                                              maximum = INT32U_MAX_VALUE,
                                              alias   = "sboTimeout")
    sbo_class:    SboClassKind = Field(default = SboClassKind.operate_once,
                                       alias   = "sboClass")
    min_val:      INT32        = field_int32(default = 0,
                                             minimum = INT32_MIN_VALUE,
                                             maximum = INT32_MAX_VALUE,
                                             alias   = "minVal")
    max_val:      INT32        = field_int32(default = 0,
                                             minimum = INT32_MIN_VALUE,
                                             maximum = INT32_MAX_VALUE,
                                             alias   = "maxVal")
    step_size:    INT32U       = field_int32u(default = 0,
                                              minimum = INT32U_MIN_VALUE,
                                              maximum = INT32U_MAX_VALUE,
                                              alias   = "stepSize")
    oper_timeout: INT32U       = field_int32u(default = 0,
                                              minimum = INT32U_MIN_VALUE,
                                              maximum = INT32U_MAX_VALUE,
                                              alias   = "operTimeout")
    units:        Unit         = Field(default_factory = Unit,
                                       alias           = "units")
    ctl_val:      INT32        = field_int32(default = 0,
                                             minimum = INT32_MIN_VALUE,
                                             maximum = INT32_MAX_VALUE,
                                             alias   = "ctlVal")

# IEC 61850-7-3 7.5.7
class BSC(ControlTestingCDC):
    cdc_name:     VisString255    = Field(default = 'BSC',
                                          pattern = 'BSC',
                                          alias   = 'cdcName')
    origin:       Originator      = Field(default = Originator,
                                          alias   = "origin")
    ctl_num:      INT8U           = field_int8u(default = 0,
                                                minimum = INT8U_MIN_VALUE,
                                                maximum = INT8U_MAX_VALUE,
                                                alias   = "ctlNum")
    val_w_tr:     ValWithTrans    = Field(default_factory = ValWithTrans,
                                          alias           = "valWTr")
    q:            Quality         = Field(default_factory = Quality,
                                          alias           = "q")
    t:            Timestamp       = Field(default_factory = Timestamp,
                                          alias           = "t")
    st_seld:      BOOLEAN         = Field(default = False,
                                          alias   = "stSeld")
    sub_val:      ValWithTrans    = Field(default_factory = ValWithTrans,
                                          alias           = "subVal")
    persistent:   BOOLEAN         = Field(default = False,
                                          alias   = "persistent")
    ctl_model:    CtlModelKind    = Field(default = CtlModelKind.direct_with_normal_security,
                                          alias   = "ctlModel")
    sbo_timeout:  INT32U          = field_int32u(default = 0,
                                                 minimum = INT32U_MIN_VALUE,
                                                 maximum = INT32U_MAX_VALUE,
                                                 alias   = "sboTimeout")
    sbo_class:    SboClassKind    = Field(default = SboClassKind.operate_once,
                                          alias   = "sboClass")
    min_val:      INT8            = field_int8(default = 0,
                                               minimum = INT8_MIN_VALUE,
                                               maximum = INT8_MAX_VALUE,
                                               alias   = "minVal")
    max_val:      INT8            = field_int8(default = 0,
                                               minimum = INT8_MIN_VALUE,
                                               maximum = INT8_MAX_VALUE,
                                               alias   = "maxVal")
    oper_timeout: INT32U          = field_int32u(default = 0,
                                                 minimum = INT32U_MIN_VALUE,
                                                 maximum = INT32U_MAX_VALUE,
                                                 alias   = "operTimeout")
    ctl_val:      StepControlKind = Field(default = StepControlKind.stop,
                                          alias   = "ctlVal")

# IEC 61850-7-3 7.5.8
class ISC(ControlTestingCDC):
    cdc_name:     VisString255 = Field(default = 'ISC',
                                       pattern = 'ISC',
                                       alias   = 'cdcName')
    origin:       Originator   = Field(default_factory = Originator,
                                       alias           = "origin")
    ctl_num:      INT8U        = field_int8u(default = 0,
                                             minimum = INT8U_MIN_VALUE,
                                             maximum = INT8U_MAX_VALUE,
                                             alias   = "ctlNum")
    val_w_tr:     ValWithTrans = Field(default_factory = ValWithTrans,
                                       alias           = "valWTr")
    q:            Quality      = Field(default_factory = Quality,
                                       alias           = "q")
    t:            Timestamp    = Field(default_factory = Timestamp,
                                       alias           = "t")
    st_seld:      BOOLEAN      = Field(default = False,
                                       alias   = "stSeld")
    sub_val:      ValWithTrans = Field(default_factory = ValWithTrans,
                                       alias           = "subVal")
    ctl_model:    CtlModelKind = Field(default = CtlModelKind.direct_with_normal_security,
                                       alias   = "ctlModel")
    sbo_timeout:  INT32U       = field_int32u(default = 0,
                                              minimum = INT32U_MIN_VALUE,
                                              maximum = INT32U_MAX_VALUE,
                                              alias   = "sboTimeout")
    min_val:      INT8         = field_int8(default = 0,
                                            minimum = INT8_MIN_VALUE,
                                            maximum = INT8_MAX_VALUE,
                                            alias   = "minVal")
    max_val:      INT8         = field_int8(default = 0,
                                            minimum = INT8_MIN_VALUE,
                                            maximum = INT8_MAX_VALUE,
                                            alias   = "maxVal")
    oper_timeout: INT32U       = field_int32u(default = 0,
                                              minimum = INT32U_MIN_VALUE,
                                              maximum = INT32U_MAX_VALUE,
                                              alias   = "operTimeout")
    ctl_val:      INT8         = field_int8(default = 0,
                                            minimum = INT8_MIN_VALUE,
                                            maximum = INT8_MAX_VALUE,
                                            alias   = "ctlVal")

# IEC 61850-7-3 7.5.9
class APC(ControlTestingCDC):
    cdc_name:     VisString255      = Field(default = 'APC',
                                            pattern = 'APC',
                                            alias   = 'cdcName')
    origin:       Originator        = Field(default_factory = Originator,
                                            alias           = "origin")
    ctl_num:      INT8U             = field_int8u(default = 0,
                                                  minimum = INT8U_MIN_VALUE,
                                                  maximum = INT8U_MAX_VALUE,
                                                  alias   = "ctlNum")
    mx_val:       AnalogueValue     = Field(default_factory = AnalogueValue,
                                            alias           = "mxVal")
    q:            Quality           = Field(default_factory = Quality,
                                            alias           = "q")
    t:            Timestamp         = Field(default_factory = Timestamp,
                                            alias           = "t")
    st_seld:      BOOLEAN           = Field(default = False,
                                            alias   = "stSeld")
    sub_val:      AnalogueValue     = Field(default_factory = AnalogueValue,
                                            alias           = "subVal")
    ctl_model:    CtlModelKind      = Field(default = CtlModelKind.direct_with_normal_security,
                                            alias   = "ctlModel")
    sbo_timeout:  INT32U            = field_int32u(default = 0,
                                                   minimum = INT32U_MIN_VALUE,
                                                   maximum = INT32U_MAX_VALUE,
                                                   alias   = "sboTimeout")
    sbo_class:    SboClassKind      = Field(default = SboClassKind.operate_once,
                                            alias   = "sboClass")
    units:        Unit              = Field(default_factory = Unit,
                                            alias           = "units")
    db:           INT32U            = field_int32u(default = 0,
                                                   minimum = INT32U_MIN_VALUE,
                                                   maximum = INT32U_MAX_VALUE,
                                                   alias   = "db")
    svc:          ScaledValueConfig = Field(default_factory = ScaledValueConfig,
                                            alias           = "sVC")
    min_val:      AnalogueValue     = Field(default_factory = AnalogueValue,
                                            alias           = "minVal")
    max_val:      AnalogueValue     = Field(default_factory = AnalogueValue,
                                            alias           = "maxVal")
    step_size:    AnalogueValue     = Field(default_factory = AnalogueValue,
                                            alias           = "stepSize")
    oper_timeout: INT32U            = field_int32u(default = 0,
                                                   minimum = INT32U_MIN_VALUE,
                                                   maximum = INT32U_MAX_VALUE,
                                                   alias   = "operTimeout")
    db_ref:       FLOAT32           = field_float32(default = 0.0,
                                                    minimum = FLOAT32_MIN_VALUE,
                                                    maximum = FLOAT32_MAX_VALUE,
                                                    alias   = "operTimeout")
    ctl_val:      AnalogueValueCtl  = Field(default_factory = AnalogueValueCtl,
                                            alias           = "ctlVal")

# IEC 61850-7-3 7.5.10
class BAC(ControlTestingCDC):
    cdc_name:     VisString255      = Field(default = 'BAC',
                                            pattern = 'BAC',
                                            alias   = 'cdcName')
    origin:       Originator        = Field(default_factory = Originator,
                                            alias           = "origin")
    ctl_num:      INT8U             = field_int8u(default = 0,
                                                  minimum = INT8U_MIN_VALUE,
                                                  maximum = INT8U_MAX_VALUE,
                                                  alias   = "ctlNum")
    mx_val:       AnalogueValue     = Field(default_Factory = AnalogueValue,
                                            alias           = "mxVal")
    q:            Quality           = Field(default_factory = Quality,
                                            alias           = "q")
    t:            Timestamp         = Field(default_factory = Timestamp,
                                            alias           = "t")
    st_seld:      BOOLEAN           = Field(default = False,
                                            alias   = "stSeld")
    sub_val:      AnalogueValue     = Field(default_factory = AnalogueValue,
                                            alias           = "subVal")
    persistent:   BOOLEAN           = Field(default = False,
                                            alias   = "persistent")
    ctl_model:    CtlModelKind      = Field(default = CtlModelKind.direct_with_normal_security,
                                            alias   = "ctlModel")
    sbo_timeout:  INT32U            = field_int32u(default = 0,
                                                   minimum = INT32U_MIN_VALUE,
                                                   maximum = INT32U_MAX_VALUE,
                                                   alias   = "sboTimeout")
    sbo_class:    SboClassKind      = Field(default = SboClassKind.operate_once,
                                            alias   = "sboClass")
    units:        Unit              = Field(default_factory = Unit,
                                            alias           = "units")
    db:           INT32U            = field_int32u(default = 0,
                                                   minimum = INT32U_MIN_VALUE,
                                                   maximum = INT32U_MAX_VALUE,
                                                   alias   = "db")
    svc:          ScaledValueConfig = Field(default_factory = ScaledValueConfig,
                                            alias           = "sVC")
    min_val:      AnalogueValue     = Field(default_factory = AnalogueValue,
                                            alias           = "minVal")
    max_val:      AnalogueValue     = Field(default_factory = AnalogueValue,
                                            alias           = "maxVal")
    step_size:    AnalogueValue     = Field(default_factory = AnalogueValue,
                                            alias           = "stepSize")
    oper_timeout: INT32U            = field_int32u(default = 0,
                                                   minimum = INT32U_MIN_VALUE,
                                                   maximum = INT32U_MAX_VALUE,
                                                   alias   = "operTimeout")
    db_ref:       FLOAT32           = field_float32(default = 0,
                                                    minimum = FLOAT32_MIN_VALUE,
                                                    maximum = FLOAT32_MAX_VALUE,
                                                    alias   = "dbRef")
    ctl_val:      StepControlKind   = Field(default = StepControlKind.stop,
                                            alias   = "ctlVal")

