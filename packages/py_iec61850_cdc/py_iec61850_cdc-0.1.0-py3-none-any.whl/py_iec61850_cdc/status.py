# py_iec61850_cdc status.py
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

# This file provides the binary object datatypes described in
# IEC 61850-7-2:2010+AMD1:2020 CSV and IEC 61850-7-3:2010+AMD1:2020 CSV
# as (e.g. BOOLEAN-based classes).

from pydantic import Field

from .basetypes import (
    BOOLEAN,
    INT16,
    INT16_MIN_VALUE,
    INT16_MAX_VALUE,
    field_int16,
    INT32,
    INT32_MIN_VALUE,
    INT32_MAX_VALUE,
    field_int32,
    INT64,
    INT64_MIN_VALUE,
    INT64_MAX_VALUE,
    field_int64,
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
    Octet64,
    field_octet64,
    Unicode255,
    field_unicode255,
    VisString64,
    field_visstring64,
    VisString255,
    field_visstring255,
)

from .enums import (
    DpStatusKind,
    EnumDA,
    FaultDirectionKind,
    PhaseFaultDirectionKind,
    SeverityKind
)

from .attributes import (
    Cell,
    Originator,
    Quality,
    Timestamp,
    Unit
)

from .abstracts import (
    BasePrimitiveCDC,
    SubstitutionCDC
)

# IEC 61850-7-3 7.3.2
class SPS(SubstitutionCDC):
    cdc_name: VisString255 = Field(default = 'SPS',
                                   pattern = 'SPS',
                                   alias   = 'cdcName')
    st_val:   BOOLEAN      = Field(default = False,
                                   alias   = "stVal")
    q:        Quality      = Field(default_factory = Quality,
                                   alias           = "q")
    t:        Timestamp    = Field(default_factory = Timestamp,
                                   alias           = "t")
    sub_val:  BOOLEAN      = Field(default = False,
                                   alias           = "subVal")

# IEC 61850-7-3 7.3.3
class DPS(SubstitutionCDC):
    cdc_name: VisString255 = Field(default = 'DPS',
                                   pattern = 'DPS',
                                   alias   = 'cdcName')
    st_val:   DpStatusKind = Field(default = DpStatusKind.off,
                                   alias   = "stVal")
    q:        Quality      = Field(default_factory = Quality,
                                   alias           = "q")
    t:        Timestamp    = Field(default_factory = Timestamp,
                                   alias           = "t")
    sub_val:  DpStatusKind = Field(default = DpStatusKind.off,
                                   alias   = "subVal")

# IEC 61850-7-3 7.3.4
class INS(SubstitutionCDC):
    cdc_name: VisString255 = Field(default = 'INS',
                                   pattern = 'INS',
                                   alias   = 'cdcName')
    st_val:  INT32         = field_int32(default = 0,
                                         minimum = INT32_MIN_VALUE,
                                         maximum = INT32_MAX_VALUE,
                                         alias   = "stVal")
    q:       Quality       = Field(default_factory = Quality,
                                   alias           = "q")
    t:       Timestamp     = Field(default_factory = Timestamp,
                                   alias           = "t")
    sub_val: INT32         = field_int32(default = 0,
                                         minimum = INT32_MIN_VALUE,
                                         maximum = INT32_MAX_VALUE,
                                         alias   = "subVal")
    units:   Unit          = Field(default_factory = Unit,
                                   alias           = "units")

# IEC 61850-7-3 7.3.5
class ENS(SubstitutionCDC):
    cdc_name: VisString255 = Field(default = 'ENS',
                                   pattern = 'ENS',
                                   alias   = 'cdcName')
    st_val:  EnumDA        = Field(default = 0,
                                   alias   = "stVal")
    q:       Quality       = Field(default_factory = Quality,
                                   alias           = "q")
    t:       Timestamp     = Field(default_factory = Timestamp,
                                   alias           = "t")
    sub_val: EnumDA        = Field(default = 0,
                                   alias   = "subVal")

# IEC 61850-7-3 7.3.6
class ACT(BasePrimitiveCDC):
    cdc_name:      VisString255 = Field(default = 'ACT',
                                        pattern = 'ACT',
                                        alias   = 'cdcName')
    general:       BOOLEAN      = Field(default = False,
                                        alias   = "general")
    phs_a:         BOOLEAN      = Field(default = False,
                                        alias   = "phsA")
    phs_b:         BOOLEAN      = Field(default = False,
                                        alias   = "phsB")
    phs_c:         BOOLEAN      = Field(default = False,
                                        alias   = "phsC")
    neut:          BOOLEAN      = Field(default = False,
                                        alias   = "neut")
    q:             Quality      = Field(default_factory = Quality,
                                        alias           = "q")
    t:             Timestamp    = Field(default_factory = Timestamp,
                                        alias           = "t")
    origin_src:    Originator   = Field(default_factory = Originator,
                                        alias           = "originSrc")
    oper_tm_phs_a: Timestamp    = Field(default_factory = Timestamp,
                                        alias           = "operTmPhsA")
    oper_tm_phs_b: Timestamp    = Field(default_factory = Timestamp,
                                        alias           = "operTmPhsB")
    oper_tm_phs_c: Timestamp    = Field(default_factory = Timestamp,
                                        alias           = "operTmPhsC")

# IEC 61850-7-3 7.3.7
class ACD(BasePrimitiveCDC):
    cdc_name:    VisString255 = Field(default = 'ACD',
                                      pattern = 'ACD',
                                      alias   = 'cdcName')
    general:     BOOLEAN                 = Field(default = False,
                                                 alias   = "general")
    dir_general: FaultDirectionKind      = Field(default = FaultDirectionKind.unknown,
                                                 alias   = "dirGeneral")
    phs_a:       BOOLEAN                 = Field(default = False,
                                                 alias   = "phsA")
    dir_phs_a:   PhaseFaultDirectionKind = Field(default = PhaseFaultDirectionKind.unknown,
                                                 alias   = "dirPhsA")
    phs_b:       BOOLEAN                 = Field(default = False,
                                                 alias   = "phsB")
    dir_phs_b:   PhaseFaultDirectionKind = Field(default = PhaseFaultDirectionKind.unknown,
                                                 alias   = "dirPhsB")
    phs_c:       BOOLEAN                 = Field(default = False,
                                                 alias   = "phsC")
    dir_phs_c:   PhaseFaultDirectionKind = Field(default = PhaseFaultDirectionKind.unknown,
                                                 alias   = "dirPhsC")
    neut:        BOOLEAN                 = Field(default = False,
                                                 alias   = "neut")
    dir_neut:    PhaseFaultDirectionKind = Field(default = PhaseFaultDirectionKind.unknown,
                                                 alias   = "dirNeut")
    q:           Quality                 = Field(default_factory = Quality,
                                                 alias           = "q")
    t:           Timestamp               = Field(default_factory = Timestamp,
                                                 alias           = "t")

# IEC 61850-7-3 7.3.8
class SEC(BasePrimitiveCDC):
    cdc_name: VisString255 = Field(default = 'SEC',
                                   pattern = 'SEC',
                                   alias   = 'cdcName')
    cnt:      INT32U       = field_int32u(default = 0,
                                          minimum = INT32_MIN_VALUE,
                                          maximum = INT32_MAX_VALUE,
                                          alias   = "cnt")
    sev:      SeverityKind = Field(default = SeverityKind.unknown,
                                   alias   = "sev")
    t:        Timestamp    = Field(default_factory = Timestamp,
                                   alias           = "t")
    addr:     Octet64      = field_octet64(default = "",
                                           alias   = "addr")
    add_info: VisString64  = field_visstring64(default = "",
                                               alias   = "addInfo")

# IEC 61850-7-3 7.3.9
class BCR(BasePrimitiveCDC):
    cdc_name:    VisString255 = Field(default = 'ACD',
                                      pattern = 'ACD',
                                      alias   = 'cdcName')
    act_val:  INT64     = field_int64(default = 0,
                                      minimum = INT64_MIN_VALUE,
                                      maximum = INT64_MAX_VALUE,
                                      alias   = "actVal")
    fr_val:   INT64     = field_int64(default = 0,
                                      minimum = INT64_MIN_VALUE,
                                      maximum = INT64_MAX_VALUE,
                                      alias   = "frVal")
    fr_tm:    Timestamp = Field(default_factory = Timestamp,
                                alias           = "frTm")
    q:        Quality   = Field(default_factory = Quality,
                                alias           = "q")
    t:        Timestamp = Field(default_factory = Timestamp,
                                alias           = "t")
    units:    Unit      = Field(default_factory = Unit,
                                alias           = "units")
    puls_qty: FLOAT32   = field_float32(default = 0.0,
                                        minimum = FLOAT32_MIN_VALUE,
                                        maximum = FLOAT32_MAX_VALUE,
                                        alias   = "pulsQty")
    fr_ena:   BOOLEAN   = Field(default = False,
                                alias   = "frEna")
    str_tm:   Timestamp = Field(default_factory = Timestamp,
                                alias           = "strTm")
    fr_pd:    INT32     = field_int32(default = 0,
                                      minimum = INT32_MIN_VALUE,
                                      maximum = INT32_MAX_VALUE,
                                      alias   = "frPd")
    fr_rs:    BOOLEAN   = Field(default = False,
                                alias   = "frRs")

# IEC 61850-7-3 7.3.10
class HST(BasePrimitiveCDC):
    cdc_name:    VisString255 = Field(default = 'ACD',
                                      pattern = 'ACD',
                                      alias   = 'cdcName')
    hst_val:    list[INT32]  = None # Probably needs field for the alias...
    q:          Quality      = Field(default_factory = Quality,
                                     alias           = "q")
    t:          Timestamp    = Field(default_factory = Timestamp,
                                     alias           = "t")
    num_pts:    INT16U       = field_int16u(default = 0,
                                            minimum = INT16_MIN_VALUE,
                                            maximum = INT16_MAX_VALUE,
                                            alias   = "numPts")
    hst_rangec: list[Cell]   = None # Probably needs field for the alias...
    xUnits:     Unit         = Field(default_factory = Unit,
                                     alias           = "xUnits")
    yUnits:     Unit         = Field(default_factory = Unit,
                                     alias           = "yUnits")
    units:      Unit         = Field(default_factory = Unit,
                                     alias           = "units")
    max_pts:    INT16U       = field_int16u(default = 0,
                                            minimum = INT16_MIN_VALUE,
                                            maximum = INT16_MAX_VALUE,
                                            alias   = "maxPts")
    xd:         VisString255 = field_visstring255(default = "",
                                                  alias   = "xD")
    xdu:        Unicode255   = field_unicode255(default = "",
                                                alias   = "xDU")
    yd:         VisString255 = field_visstring255(default = "",
                                                  alias   = "yD")
    ydu:        Unicode255   = field_unicode255(default = "",
                                                alias   = "yDU")

# IEC 61850-7-3 7.3.11
class VSS(BasePrimitiveCDC):
    cdc_name: VisString255 = Field(default = 'VSS',
                                   pattern = 'VSS',
                                   alias   = 'cdcName')
    st_val:   VisString255 = field_visstring255(default = "",
                                                alias   = "stVal")
    q:        Quality      = Field(default_factory = Quality,
                                   alias           = "q")
    t:        Timestamp    = Field(default_factory = Timestamp,
                                   alias           = "t")

# IEC 61850-7-3 7.3.12
class ORS(BasePrimitiveCDC):
    cdc_name: VisString255  = Field(default = 'ORS',
                                    pattern = 'ORS',
                                    alias   = 'cdcName')
    st_val: ObjectReference = Field(default = "",
                                    alias   = "stVal")
    q:      Quality         = Field(default_factory = Quality,
                                    alias           = "q")
    t:      Timestamp       = Field(default_factory = Timestamp,
                                    alias           = "t")

# IEC 61850-7-3 7.3.13
class TCS(BasePrimitiveCDC):
    cdc_name: VisString255 = Field(default = 'TCS',
                                   pattern = 'TCS',
                                   alias   = 'cdcName')
    st_val:   Timestamp    = Field(default_factory = Timestamp,
                                   alias           = "stVal")
    q:        Quality      = Field(default_factory = Quality,
                                   alias           = "q")
    t:        Timestamp    = Field(default_factory = Timestamp,
                                   alias           = "t")

