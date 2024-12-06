# py_iec61850_cdc measurand.py
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
    VisString255 # field_visstring255 is not used, because VisString only does cdc_name here.
)

from .enums import (
    HvReferenceKind,
    PhaseAngleReferenceKind,
    PhaseReferenceKind,
    RangeKind,
    SequenceKind
)

from .attributes import (
    AnalogueValue,
    Quality,
    RangeConfig,
    ScaledValueConfig,
    Timestamp,
    Unit,
    Vector
)

from .abstracts import (
    BaseComposedCDC,
    BasePrimitiveCDC,
    HarmonicMeasurandCDC,
    SubstitutionCDC
)

# IEC 61850-7-3 7.4.3
class MV(SubstitutionCDC):
    cdc_name:    VisString255      = Field(default = 'MV',
                                           pattern = 'MV',
                                           alias   = 'cdcName')
    inst_mag:    AnalogueValue     = Field(default_factory = AnalogueValue,
                                           alias           = "instMag")
    mag:         AnalogueValue     = Field(default_factory = AnalogueValue,
                                           alias           = "mag")
    range_v:     RangeKind         = Field(default = RangeKind.normal,
                                           alias   = "range")# Had to rename this one due to Python
    q:           Quality           = Field(default_factory = Quality,
                                           alias           = "q")
    t:           Timestamp         = Field(default_factory = Timestamp,
                                           alias           = "t")
    sub_mag:     AnalogueValue     = Field(default_factory = AnalogueValue,
                                           alias           = "subMag")
    units:       Unit              = Field(default_factory = Unit,
                                           alias           = "units")
    db:          INT32U            = field_int32u(default = 0,
                                                  minimum = INT32U_MIN_VALUE,
                                                  maximum = INT32U_MAX_VALUE,
                                                  alias   = "db")
    zero_db:     INT32U            = field_int32u(default = 0,
                                                  minimum = INT32U_MIN_VALUE,
                                                  maximum = INT32U_MAX_VALUE,
                                                  alias   = "zeroDb")
    svc:         ScaledValueConfig = Field(default_factory = ScaledValueConfig,
                                           alias           = "sVC")
    range_c:     RangeConfig       = Field(default_factory = RangeConfig,
                                           alias           = "rangeC")
    smp_rate:    INT32U            = field_int32u(default = 0,
                                                  minimum = INT32U_MIN_VALUE,
                                                  maximum = INT32U_MAX_VALUE,
                                                  alias   = "smpRate")
    db_ref:      FLOAT32           = field_float32(default = 0.0,
                                                   minimum = FLOAT32_MIN_VALUE,
                                                   maximum = FLOAT32_MAX_VALUE,
                                                   alias   = "dbRef")
    zero_db_ref: FLOAT32           = field_float32(default = 0.0,
                                                   minimum = FLOAT32_MIN_VALUE,
                                                   maximum = FLOAT32_MAX_VALUE,
                                                   alias   = "zeroDbRef")

# IEC 61850-7-3 7.4.4
class CMV(SubstitutionCDC):
    cdc_name:    VisString255            = Field(default = 'CMV',
                                                 pattern = 'CMV',
                                                 alias   = 'cdcName')
    inst_c_val:  Vector                  = Field(default_factory = Vector,
                                                 alias           = "instCVal")
    c_val:       Vector                  = Field(default_factory = Vector,
                                                 alias           = "cVal")
    range_v:     RangeKind               = Field(default = RangeKind.normal,
                                                 alias   = "range") # Rename per Python
    range_ang:   RangeKind               = Field(default = RangeKind.normal,
                                                 alias   = "rangeAng")
    q:           Quality                 = Field(default_factory = Quality,
                                                 alias           = "q")
    t:           Timestamp               = Field(default_factory = Timestamp,
                                                 alias           = "t")
    sub_c_val:   Vector                  = Field(default_factory = Vector,
                                                 alias           = "subCVal")
    units:       Unit                    = Field(default_factory = Unit,
                                                 alias           = "units")
    db:          INT32U                  = field_int32u(default = 0,
                                                        minimum = INT32U_MIN_VALUE,
                                                        maximum = INT32U_MAX_VALUE,
                                                        alias   = "db")
    db_ang:      INT32U                  = field_int32u(default = 0,
                                                        minimum = INT32U_MIN_VALUE,
                                                        maximum = INT32U_MAX_VALUE,
                                                        alias   = "dbAng")
    zero_db:     INT32U                  = field_int32u(default = 0,
                                                        minimum = INT32U_MIN_VALUE,
                                                        maximum = INT32U_MAX_VALUE,
                                                        alias   = "zeroDb")
    range_c:     RangeConfig             = Field(default_factory = RangeConfig,
                                                 alias           = "rangeC")
    range_ang_c: RangeConfig             = Field(default_factory = RangeConfig,
                                                 alias           = "rangeAngC")
    mag_svc:     ScaledValueConfig       = Field(default_factory = ScaledValueConfig,
                                                 alias           = "magSVC")
    ang_svc:     ScaledValueConfig       = Field(default_factory = ScaledValueConfig,
                                                 alias           = "angSVC")
    ang_ref:     PhaseAngleReferenceKind = Field(default = PhaseAngleReferenceKind.vother,
                                                 alias   = "angRef")
    smp_rate:    INT32U                  = field_int32u(default = 0,
                                                        minimum = INT32U_MIN_VALUE,
                                                        maximum = INT32U_MAX_VALUE,
                                                        alias   = "smpRate")
    db_ref:      FLOAT32                 = field_float32(default = 0,
                                                         minimum = FLOAT32_MIN_VALUE,
                                                         maximum = FLOAT32_MAX_VALUE,
                                                         alias   = "dbRef")
    zero_db_ref: FLOAT32                 = field_float32(default = 0,
                                                         minimum = FLOAT32_MIN_VALUE,
                                                         maximum = FLOAT32_MAX_VALUE,
                                                         alias   = "zeroDbRef")
    db_ang_ref:  FLOAT32                 = field_float32(default = 0,
                                                         minimum = FLOAT32_MIN_VALUE,
                                                         maximum = FLOAT32_MAX_VALUE,
                                                         alias   = "dbAngRef")

# IEC 61850-7-3 7.4.5
class SAV(BasePrimitiveCDC):
    cdc_name: VisString255      = Field(default = 'SAV',
                                        pattern = 'SAV',
                                        alias   = 'cdcName')
    inst_mag: AnalogueValue     = Field(default_factory = AnalogueValue,
                                        alias           = "instMag")
    q:        Quality           = Field(default_factory = Quality,
                                        alias           = "q")
    t:        Timestamp         = Field(default_factory = Timestamp,
                                        alias           = "t")
    units:    Unit              = Field(default_factory = Unit,
                                        alias           = "units")
    svc:      ScaledValueConfig = Field(default_factory = ScaledValueConfig,
                                        alias           = "sVC")
    minimum:  AnalogueValue     = Field(default_factory = AnalogueValue,
                                        alias           = "min")
    maximum:  AnalogueValue     = Field(default_factory = AnalogueValue,
                                        alias           = "max")

# IEC 61850-7-3 7.4.6
class WYE(BaseComposedCDC):
    cdc_name:    VisString255            = Field(default = 'WYE',
                                                 pattern = 'WYE',
                                                 alias   = 'cdcName')
    phs_a:       CMV                     = Field(default_factory = CMV,
                                                 alias           = "phsA")
    phs_b:       CMV                     = Field(default_factory = CMV,
                                                 alias           = "phsB")
    phs_c:       CMV                     = Field(default_factory = CMV,
                                                 alias           = "phsC")
    neut:        CMV                     = Field(default_factory = CMV,
                                                 alias           = "neut")
    net:         CMV                     = Field(default_factory = CMV,
                                                 alias           = "net")
    res:         CMV                     = Field(default_factory = CMV,
                                                 alias           = "res")
    ang_ref:     PhaseAngleReferenceKind = Field(default = PhaseAngleReferenceKind.vother,
                                                 alias   = "angRef")
    phs_to_neut: BOOLEAN                 = Field(default = False,
                                                 alias   = "phsToNeut")

# IEC 61850-7-3 7.4.7
class DEL(BaseComposedCDC):
    cdc_name: VisString255            = Field(default = 'DEL',
                                              pattern = 'DEL',
                                              alias   = 'cdcName')
    phs_ab:   CMV                     = Field(default_factory = CMV,
                                              alias           = "phsAB")
    phs_bc:   CMV                     = Field(default_factory = CMV,
                                              alias           = "phsBC")
    phs_ca:   CMV                     = Field(default_factory = CMV,
                                              alias           = "phsCA")
    ang_ref:  PhaseAngleReferenceKind = Field(default = PhaseAngleReferenceKind.vother,
                                              alias           = "angRef")

# IEC 61850-7-3 7.4.8
class SEQ(BaseComposedCDC):
    cdc_name: VisString255       = Field(default = 'SEQ',
                                         pattern = 'SEQ',
                                         alias   = 'cdcName')
    c1:       CMV                = Field(default_factory = CMV,
                                         alias           = "c1")
    c2:       CMV                = Field(default_factory = CMV,
                                         alias           = "c2")
    c3:       CMV                = Field(default_factory = CMV,
                                         alias           = "c3")# Zero sequence is 3 for some reason...
    seq_t:    SequenceKind       = Field(default = SequenceKind.pos_neg_zero,
                                         alias   = "seqT")
    phs_ref:  PhaseReferenceKind = Field(default = PhaseReferenceKind.a,
                                         alias   = "phsRef")

# IEC 61850-7-3 7.4.9
class HMV(HarmonicMeasurandCDC):
    cdc_name:  VisString255    = Field(default = 'HMV',
                                       pattern = 'HMV',
                                       alias   = 'cdcName')
    har:       list[CMV]       = None
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
    max_pts:   INT16U          = field_int16u(default = 0,
                                              minimum = INT16U_MIN_VALUE,
                                              maximum = INT16U_MAX_VALUE,
                                              alias   = "maxPts")

# IEC 61850-7-3 7.4.10
class HWYE(HarmonicMeasurandCDC):
    cdc_name:  VisString255            = Field(default = 'HWYE',
                                               pattern = 'HWYE',
                                               alias   = 'cdcName')
    phs_a_har: list[CMV]               = None
    phs_b_har: list[CMV]               = None
    phs_c_har: list[CMV]               = None
    neut_har:  list[CMV]               = None
    net_har:   list[CMV]               = None
    res_har:   list[CMV]               = None
    num_har:   INT16U                  = field_int16u(default = 0,
                                                      minimum = INT16U_MIN_VALUE,
                                                      maximum = INT16U_MAX_VALUE,
                                                      alias   = "numHar")
    num_cyc:   INT16U                  = field_int16u(default = 0,
                                                      minimum = INT16U_MIN_VALUE,
                                                      maximum = INT16U_MAX_VALUE,
                                                      alias   = "numCyc")
    eval_tm:   INT16U                  = field_int16u(default = 0,
                                                      minimum = INT16U_MIN_VALUE,
                                                      maximum = INT16U_MAX_VALUE,
                                                      alias   = "evalTm")
    ang_ref:   PhaseAngleReferenceKind = Field(default = PhaseAngleReferenceKind.vother,
                                               alias   = "angRef")
    smp_rate:  INT32U                  = field_int32u(default = 0,
                                                      minimum = INT32U_MIN_VALUE,
                                                      maximum = INT32U_MAX_VALUE,
                                                      alias   = "smpRate")
    frequency: FLOAT32                 = field_float32(default = 0,
                                                       minimum = FLOAT32_MIN_VALUE,
                                                       maximum = FLOAT32_MAX_VALUE,
                                                       alias   = "frequency")
    hv_ref:    HvReferenceKind         = Field(default = HvReferenceKind.rms,
                                               alias   = "hvRef")
    rms_cyc:   INT16U                  = field_int16u(default = 0,
                                                      minimum = INT16U_MIN_VALUE,
                                                      maximum = INT16U_MAX_VALUE,
                                                      alias   = "rmsCyc")
    max_pts:   INT16U                  = field_int16u(default = 0,
                                                      minimum = INT16U_MIN_VALUE,
                                                      maximum = INT16U_MAX_VALUE,
                                                      alias   = "maxPts")

# IEC 61850-7-3 7.4.11
class HDEL(HarmonicMeasurandCDC):
    cdc_name:   VisString255    = Field(default = 'HDEL',
                                        pattern = 'HDEL',
                                        alias   = 'cdcName')
    phs_ab_har: list[CMV]       = None
    phs_bc_har: list[CMV]       = None
    phs_ca_har: list[CMV]       = None
    num_har:    INT16U          = field_int16u(default = 0,
                                               minimum = INT16U_MIN_VALUE,
                                               maximum = INT16U_MAX_VALUE,
                                               alias   = "numHar")
    num_cyc:    INT16U          = field_int16u(default = 0,
                                               minimum = INT16U_MIN_VALUE,
                                               maximum = INT16U_MAX_VALUE,
                                               alias   = "numCyc")
    eval_tm:    INT16U          = field_int16u(default = 0,
                                               minimum = INT16U_MIN_VALUE,
                                               maximum = INT16U_MAX_VALUE,
                                               alias   = "evalTm")
    ang_ref:    PhaseAngleReferenceKind = Field(default = PhaseAngleReferenceKind.vother,
                                                alias   = "angRef")
    smp_rate:   INT32U          = field_int16u(default = 0,
                                               minimum = INT16U_MIN_VALUE,
                                               maximum = INT16U_MAX_VALUE,
                                               alias   = "smpRate")
    frequency:  FLOAT32         = field_int16u(default = 0,
                                               minimum = INT16U_MIN_VALUE,
                                               maximum = INT16U_MAX_VALUE,
                                               alias   = "frequency")
    hv_ref:     HvReferenceKind = Field(default = HvReferenceKind.rms,
                                        alias   = "hvRef")
    rms_cyc:    INT16U          = field_int16u(default = 0,
                                               minimum = INT16U_MIN_VALUE,
                                               maximum = INT16U_MAX_VALUE,
                                               alias   = "rmsCyc")
    max_pts:    INT16U          = field_int16u(default = 0,
                                               minimum = INT16U_MIN_VALUE,
                                               maximum = INT16U_MAX_VALUE,
                                               alias   = "maxPts")

