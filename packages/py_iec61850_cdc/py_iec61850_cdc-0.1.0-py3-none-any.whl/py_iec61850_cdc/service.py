# py_iec61850_cdc service.py
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

# This file provides the service status CDCs described under Clause 7.9 of
# IEC 61850-7-3:2010+AMD1:2020 CSV as Python dataclasses.

from typing import Any
from pydantic import Field

from .basetypes import (
    BOOLEAN,
    EntryID,
    field_entryid,
    INT16,
    INT16_MIN_VALUE,
    INT16_MAX_VALUE,
    field_int16,
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
    ObjectReference,
    field_objectreference,
    Octet64,
    field_octet64,
    PhyComAddr,
    field_phycomaddr,
    Unicode255,
    field_unicode255,
    VisString129,
    field_visstring129,
    VisString255,
    field_visstring255
)

from .enums import (
    ControlServiceStatusKind,
    SamplingModeKind,
    ServiceNameKind,
    ServiceStatusKind
)

from .attributes import (
    CheckConditions,
    EntryTime,
    Originator,
    RCBReportOptions,
    SVMessageOptions,
    Timestamp,
    TriggerConditions
)

from .abstracts import (
    BasePrimitiveCDC
)

# IEC 61850-7-3 7.9.10
class CTS(BasePrimitiveCDC):
    cdc_name:       VisString255             = Field(default = 'CTS',
                                                     pattern = 'CTS',
                                                     alias   = 'cdcName')
    obj_ref:        ObjectReference          = field_objectreference(default = "",
                                                                     alias   = "objRef")
    service_type:   ServiceNameKind          = Field(default = ServiceNameKind.unknown,
                                                     alias   = "serviceType")
    error_code:     ServiceStatusKind        = Field(default = ServiceStatusKind.no_error,
                                                     alias   = "errorCode")
    originator_id:  Octet64                  = field_octet64(default = "",
                                                             alias   = "originatorID")
    t:              Timestamp                = Field(default_factory = Timestamp,
                                                     alias           = "t")
    cert_issuer:    Unicode255               = field_unicode255(default = "",
                                                                alias   = "certIssuer"),
    ctl_val:        Any                      = None
    operTm:         Timestamp                = Field(default_factory = Timestamp,
                                                     alias           = "operTm")
    origin:         Originator               = Field(default_factory = Originator,
                                                     alias           = "originator")
    ctl_num:        INT8U                    = field_int8u(default = 0,
                                                           minimum = INT8U_MIN_VALUE,
                                                           maximum = INT8U_MAX_VALUE,
                                                           alias   = "ctlNum")
    T:              Timestamp                = Field(default_factory = Timestamp,
                                                     alias           = "T")
    test:           BOOLEAN                  = Field(default = False,
                                                     alias   = "test")
    check:          CheckConditions          = Field(default_factory = CheckConditions,
                                                     alias           = "check")
    resp_add_cause: ControlServiceStatusKind = Field(default = ControlServiceStatusKind.unknown,
                                                     alias   = "respAddCause")


# IEC 61850-7-3 7.9.9
class STS(BasePrimitiveCDC):
    cdc_name:      VisString255      = Field(default = 'STS',
                                             pattern = 'STS',
                                             alias   = 'cdcName')
    obj_ref:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "objRef")
    service_type:  ServiceNameKind   = Field(default = ServiceNameKind.unknown,
                                             alias   = "serviceType")
    error_code:    ServiceStatusKind = Field(default = ServiceStatusKind.no_error,
                                             alias   = "errorCode")
    originator_id: Octet64           = field_octet64(default = "",
                                                     alias   = "originatorID")
    t:             Timestamp         = Field(default_factory = Timestamp,
                                             alias           = "t")
    cert_issuer:   Unicode255        = field_unicode255(default = "",
                                                        alias   = "certIssuer")
    num_of_sg:     INT8U             = field_int8u(default = 0,
                                                   minimum = INT8U_MIN_VALUE,
                                                   maximum = INT8U_MAX_VALUE,
                                                   alias   = "numOfSG")
    act_sg:        INT8U             = field_int8u(default = 0,
                                                   minimum = INT8U_MIN_VALUE,
                                                   maximum = INT8U_MAX_VALUE,
                                                   alias   = "actSG")
    edit_sg:       INT8U             = field_int8u(default = 0,
                                                   minimum = INT8U_MIN_VALUE,
                                                   maximum = INT8U_MAX_VALUE,
                                                   alias   = "editSG")
    cnf_edit:      BOOLEAN           = Field(default = False,
                                             alias   = "cnfEdit")
    i_act_tm:      Timestamp         = Field(default_factory = Timestamp,
                                             alias           = "iActTm")
    resv_tms:      INT16U            = field_int16u(default = 0,
                                                    minimum = INT16U_MIN_VALUE,
                                                    maximum = INT16U_MAX_VALUE,
                                                    alias   = "resvTms")

# IEC 61850-7-3 7.9.8
class NTS(BasePrimitiveCDC):
    cdc_name:      VisString255      = Field(default = 'NTS',
                                             pattern = 'NTS',
                                             alias   = 'cdcName')
    obj_ref:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "objRef")
    service_type:  ServiceNameKind   = Field(default = ServiceNameKind.unknown,
                                             alias   = "serviceType")
    error_code:    ServiceStatusKind = Field(default = ServiceStatusKind.no_error,
                                             alias   = "errorCode")
    originator_id: Octet64           = field_octet64(default = "",
                                                     alias   = "originatorID")
    t:             Timestamp         = Field(default_factory = Timestamp,
                                             alias           = "t")
    sv_ena:        BOOLEAN           = Field(default = False,
                                             alias   = "svEna")
    resv:          BOOLEAN           = Field(default = False,
                                             alias   = "resv")
    usv_id:        VisString129      = field_visstring129(default = "",
                                                          alias   = "usvID")
    dat_set:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "datSet")
    conf_rev:      INT32U            = field_int32u(default = 0,
                                                    minimum = INT32U_MIN_VALUE,
                                                    maximum = INT32U_MAX_VALUE,
                                                    alias   = "confRev")
    smp_mod:       SamplingModeKind  = Field(default = SamplingModeKind.samples_per_second,
                                             alias   = "smpMod")
    smp_rate:      INT16U            = field_int16u(default = 0,
                                                    minimum = INT16U_MIN_VALUE,
                                                    maximum = INT16U_MAX_VALUE,
                                                    alias   = "smpRate")
    opt_flds:      SVMessageOptions  = Field(default_factory = SVMessageOptions,
                                             alias           = "optFlds")
    dst_address:   PhyComAddr        = field_phycomaddr(default = "",
                                                        alias   = "dstAddress")

# IEC 61850-7-3 7.9.7
class MTS(BasePrimitiveCDC):
    cdc_name:      VisString255      = Field(default = 'MTS',
                                             pattern = 'MTS',
                                             alias   = 'cdcName')
    obj_ref:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "objRef")
    service_type:  ServiceNameKind   = Field(default = ServiceNameKind.unknown,
                                             alias   = "serviceType")
    error_code:    ServiceStatusKind = Field(default = ServiceStatusKind.no_error,
                                             alias   = "errorCode")
    originator_id: Octet64           = field_octet64(default = "",
                                                     alias   = "originatorID")
    t:             Timestamp         = Field(default_factory = Timestamp,
                                             alias           = "t")
    cert_issuer:   Unicode255        = field_unicode255(default = "",
                                                        alias   = "certIssuer")
    sv_ena:        BOOLEAN           = Field(default = False,
                                             alias   = "svEna")
    msv_id:        VisString129      = field_visstring129(default = "",
                                                          alias   = "msvID")
    dat_set:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "datSet")
    conf_rev:      INT32U            = field_int32u(default = 0,
                                                    minimum = INT32U_MIN_VALUE,
                                                    maximum = INT32U_MAX_VALUE,
                                                    alias   = "confRev")
    smp_rate:      INT16U            = field_int16u(default = 0,
                                                    minimum = INT16U_MIN_VALUE,
                                                    maximum = INT16U_MAX_VALUE,
                                                    alias   = "smpMod")
    opt_flds:      SVMessageOptions  = Field(default_factory = SVMessageOptions,
                                             alias           = "optFlds")
    smp_mod:       SamplingModeKind  = Field(default = SamplingModeKind.samples_per_second,
                                             alias   = "smpMod")
    dst_address:   PhyComAddr        = field_phycomaddr(default = "",
                                                        alias   = "dstAddress")

# IEC 61850-7-3 7.9.6
class GTS(BasePrimitiveCDC):
    cdc_name:      VisString255      = Field(default = 'GTS',
                                             pattern = 'GTS',
                                             alias   = 'cdcName')
    obj_ref:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "objRef")
    service_type:  ServiceNameKind   = Field(default = ServiceNameKind.unknown,
                                             alias   = "serviceType")
    error_code:    ServiceStatusKind = Field(default = ServiceStatusKind.no_error,
                                             alias   = "errorCode")
    originator_id: Octet64           = field_octet64(default = "",
                                                     alias   = "originatorID")
    t:             Timestamp         = Field(default_factory = Timestamp,
                                             alias           = "t")
    cert_issuer:   Unicode255        = field_unicode255(default = "",
                                                        alias   = "certIssuer")
    go_ena:        BOOLEAN           = Field(default = False,
                                             alias   = "goEna")
    go_id:         VisString129      = field_visstring129(default = "",
                                                          alias   = "goID")
    dat_set:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "datSet")
    conf_rev:      INT32U            = field_int32u(default = 0,
                                                    minimum = INT32U_MIN_VALUE,
                                                    maximum = INT32U_MAX_VALUE,
                                                    alias   = "confRev")
    nds_com:       BOOLEAN           = Field(default = False,
                                             alias   = "ndsCom")
    dst_address:   PhyComAddr        = field_phycomaddr(default = "",
                                                        alias   = "dstAddress")

# IEC 61850-7-3 7.9.5
class LTS(BasePrimitiveCDC):
    cdc_name:      VisString255      = Field(default = 'LTS',
                                             pattern = 'LTS',
                                             alias   = 'cdcName')
    obj_ref:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "objRef")
    service_type:  ServiceNameKind   = Field(default = ServiceNameKind.unknown,
                                             alias   = "serviceType")
    error_code:    ServiceStatusKind = Field(default = ServiceStatusKind.no_error,
                                             alias   = "errorCode")
    originator_id: Octet64           = field_octet64(default = "",
                                                     alias   = "originatorID")
    t:             Timestamp         = Field(default_factory = Timestamp,
                                             alias           = "t")
    cert_issuer:   Unicode255        = field_unicode255(default = "",
                                                        alias   = "certIssuer")
    log_ena:       BOOLEAN           = Field(default = False,
                                             alias   = "logEna")
    log_ref:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "logRef")
    dat_set:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "datSet")
    old_entr_tm:   EntryTime         = Field(default_factory = EntryTime,
                                             alias           = "oldEntrTm")
    new_entr_tm:   EntryTime         = Field(default_factory = EntryTime,
                                             alias           = "newEntrTm")
    old_ent:       EntryID           = field_entryid(default = "",
                                                     alias   = "oldEnt")
    new_ent:       EntryID           = field_entryid(default = "",
                                                     alias   = "newEnt")
    trg_ops:       TriggerConditions = Field(default_factory = TriggerConditions,
                                             alias           = "trgOps")
    intg_pd:       INT32U            = field_int32u(default = 0,
                                                    minimum = INT32U_MIN_VALUE,
                                                    maximum = INT32U_MAX_VALUE,
                                                    alias   = "intgPd")

# IEC 61850-7-3 7.9.4
class UTS(BasePrimitiveCDC):
    cdc_name:      VisString255      = Field(default = 'UTS',
                                             pattern = 'UTS',
                                             alias   = 'cdcName')
    obj_ref:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "objRef")
    service_type:  ServiceNameKind   = Field(default = ServiceNameKind.unknown,
                                             alias   = "serviceType")
    error_code:    ServiceStatusKind = Field(default = ServiceStatusKind.no_error,
                                             alias   = "errorCode")
    originator_id: Octet64           = field_octet64(default = "",
                                                     alias   = "originatorID")
    t:             Timestamp         = Field(default_factory = Timestamp,
                                             alias           = "t")
    cert_issuer:   Unicode255        = field_unicode255(default = "",
                                                        alias   = "certIssuer")
    rpt_id:        VisString129      = field_visstring129(default = "",
                                                          alias   = "rptID")
    rpt_ena:       BOOLEAN           = Field(default = False,
                                             alias   = "rptEna")
    resv:          BOOLEAN           = Field(default = False,
                                             alias   = "resv")
    dat_set:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "datSet")
    conf_rev:      INT32U            = field_int32u(default = 0,
                                                    minimum = INT32U_MIN_VALUE,
                                                    maximum = INT32U_MAX_VALUE,
                                                    alias   = "confRev")
    opt_flds:      RCBReportOptions  = Field(default_factory = RCBReportOptions,
                                             alias           = "optFlds")
    buf_tm:        INT32U            = field_int32u(default = 0,
                                                    minimum = INT32U_MIN_VALUE,
                                                    maximum = INT32U_MAX_VALUE,
                                                    alias   = "bufTm")
    sq_num:        INT8U             = field_int8u(default = 0,
                                                   minimum = INT8U_MIN_VALUE,
                                                   maximum = INT8U_MAX_VALUE,
                                                   alias   = "sqNum")
    trg_ops:       TriggerConditions = Field(default_factory = TriggerConditions,
                                             alias           = "trgOps")
    intg_pd:       INT32U            = field_int32u(default = 0,
                                                    minimum = INT32U_MIN_VALUE,
                                                    maximum = INT32U_MAX_VALUE,
                                                    alias   = "intgPd")
    gi:            BOOLEAN           = Field(default = False,
                                             alias   = "gi")
    owner:         Octet64           = field_octet64(default = "",
                                                     alias   = "owner")

# IEC 61850-7-3 7.9.3
class BTS(BasePrimitiveCDC):
    cdc_name:      VisString255      = Field(default = 'BTS',
                                             pattern = 'BTS',
                                             alias   = 'cdcName')
    obj_ref:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "objRef")
    service_type:  ServiceNameKind   = Field(default = ServiceNameKind.unknown,
                                             alias   = "serviceType")
    error_code:    ServiceStatusKind = Field(default = ServiceStatusKind.no_error,
                                             alias   = "errorCode")
    originator_id: Octet64           = field_octet64(default = "",
                                                     alias   = "originatorID")
    t:             Timestamp         = Field(default_factory = Timestamp,
                                             alias           = "t")
    cert_issuer:   Unicode255        = field_unicode255(default = "",
                                                        alias   = "certIssuer")
    rpt_id:        VisString129      = field_visstring129(default = "",
                                                          alias   = "rptID")
    rpt_ena:       BOOLEAN           = Field(default = False,
                                             alias   = "rptEna")
    dat_set:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "datSet")
    conf_rev:      INT32U            = field_int32u(default = 0,
                                                    minimum = INT32U_MIN_VALUE,
                                                    maximum = INT32U_MAX_VALUE,
                                                    alias   = "confRev")
    opt_flds:      RCBReportOptions  = Field(default_factory = RCBReportOptions,
                                             alias           = "optFlds")
    buf_tm:        INT32U            = field_int32u(default = 0,
                                                    minimum = INT32U_MIN_VALUE,
                                                    maximum = INT32U_MAX_VALUE,
                                                    alias   = "bufTm")
    sq_num:        INT16U            = field_int16u(default = 0,
                                                    minimum = INT16U_MIN_VALUE,
                                                    maximum = INT16U_MAX_VALUE,
                                                    alias   = "sqNum")
    trg_ops:       TriggerConditions = Field(default_factory = TriggerConditions,
                                             alias           = "trgOps")
    intg_pd:       INT32U            = field_int32u(default = 0,
                                                    minimum = INT32U_MIN_VALUE,
                                                    maximum = INT32U_MAX_VALUE,
                                                    alias   = "intgPd")
    gi:            BOOLEAN           = Field(default = False,
                                             alias   = "gi")
    purge_buf:     BOOLEAN           = Field(default = False,
                                             alias   = "purgeBuf")
    entry_id:      EntryID           = field_entryid(default = "",
                                                     alias   = "entryID")
    time_of_entry: EntryTime         = Field(default_factory = EntryTime,
                                             alias           = "timeOfEntry")
    resv_tms:      INT16             = field_int16(default = 0,
                                                   minimum = INT16_MIN_VALUE,
                                                   maximum = INT16_MAX_VALUE,
                                                   alias   = "resvTms")
    owner:         Octet64           = field_octet64(default = "",
                                                     alias   = "owner")

# IEC 61850-7-3 7.9.2
class CST(BasePrimitiveCDC):
    cdc_name:      VisString255      = Field(default = 'CST',
                                             pattern = 'CST',
                                             alias   = 'cdcName')
    obj_ref:       ObjectReference   = field_objectreference(default = "",
                                                             alias   = "objRef")
    service_type:  ServiceNameKind   = Field(default = ServiceNameKind.unknown,
                                             alias   = "serviceType")
    error_code:    ServiceStatusKind = Field(default = ServiceStatusKind.no_error,
                                             alias   = "errorCode")
    originator_id: Octet64           = field_octet64(default = "",
                                                     alias   = "originatorID")
    t:             Timestamp         = Field(default_factory = Timestamp,
                                             alias           = "t")
    cert_issuer:   Unicode255        = field_unicode255(default = "",
                                                        alias   = "certIssuer")

