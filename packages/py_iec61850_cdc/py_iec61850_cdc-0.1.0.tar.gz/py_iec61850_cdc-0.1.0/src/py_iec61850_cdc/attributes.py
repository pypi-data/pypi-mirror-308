# py_iec61850_cdc attributes.py
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

# This file provides the attribute classes described under various
# IEC 61850-7-2:2010+AMD1:2020 CSV clauses and clause 6 of
# IEC 61850-7-3:2010+AMD1:2020 CSV as Python classes for use with other
# CDCs.

# Follows PEP-8 rules on function / variable naming (e.g. underscores).

from typing import NewType, Optional

from pydantic import BaseModel, Field

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
    INT8U,
    INT8U_MIN_VALUE,
    INT8U_MAX_VALUE,
    field_int8u,
    INT16U,
    INT16U_MIN_VALUE,
    INT16U_MAX_VALUE,
    field_int16u,
    INT24U,
    INT24U_MIN_VALUE,
    INT24U_MAX_VALUE,
    field_int24u,
    INT32U,
    INT32U_MIN_VALUE,
    INT32U_MAX_VALUE,
    field_int32u,
    FLOAT32,
    FLOAT32_MIN_VALUE,
    FLOAT32_MAX_VALUE,
    field_float32,
    Octet64,
    field_octet64
)

from .enums import (
    MonthKind,
    MultiplierKind,
    OccurrenceKind,
    OriginatorCategoryKind,
    OutputSignalKind,
    PeriodKind,
    SIUnitKind,
    SourceKind,
    ValidityKind,
    WeekdayKind
)

# IEC 61850-7-3 6.11.2
class AnalogueValue(BaseModel, validate_assignment = True):
    i: INT32    = field_int32(default = 0,
                              minimum = INT32_MIN_VALUE,
                              maximum = INT32_MAX_VALUE,
                              alias   = "i")
    f: FLOAT32  = field_float32(default = 0.0,
                                minimum = FLOAT32_MIN_VALUE,
                                maximum = FLOAT32_MAX_VALUE,
                                alias   = "f")

# IEC 61850-7-3 6.11.3
class AnalogueValueCtl(BaseModel, validate_assignment = True):
    i: INT32    = field_int32(default = 0,
                              minimum = INT32_MIN_VALUE,
                              maximum = INT32_MAX_VALUE,
                              alias   = "i")
    f: FLOAT32  = field_float32(default = 0.0,
                                minimum = FLOAT32_MIN_VALUE,
                                maximum = FLOAT32_MAX_VALUE,
                                alias = "f")

# IEC 61850-7-3 6.11.4
class AnalogueValueCtlF(BaseModel, validate_assignment = True):
    f: FLOAT32 = field_float32(default = 0.0,
                               minimum = FLOAT32_MIN_VALUE,
                               maximum = FLOAT32_MAX_VALUE,
                               alias   = "f")

# IEC 61850-7-3 6.11.5
class AnalogueValueCtlInt(BaseModel, validate_assignment = True):
    i: INT32 = field_int32(default = 0,
                           minimum = INT32_MIN_VALUE,
                           maximum = INT32_MAX_VALUE,
                           alias   = "i")

# IEC 61850-7-3 6.2
class ScaledValueConfig(BaseModel, validate_assignment = True):
    scale_factor: FLOAT32 = field_float32(default = 1.0,
                                          minimum = FLOAT32_MIN_VALUE,
                                          maximum = FLOAT32_MAX_VALUE,
                                          alias   = "scaleFactor")
    offset:       FLOAT32 = field_float32(default = 0.0,
                                          minimum = FLOAT32_MIN_VALUE,
                                          maximum = FLOAT32_MAX_VALUE,
                                          alias   = "offset")

#IEC 61850-7-3 6.3
class RangeConfig(BaseModel, validate_assignment = True):
    hh_lim:  AnalogueValue = Field(default = AnalogueValue(i = INT32_MAX_VALUE,
                                                           f = FLOAT32_MAX_VALUE),
                                   alias   = "hhLim")
    h_lim:   AnalogueValue = Field(default = AnalogueValue(i = INT32_MAX_VALUE,
                                                           f = FLOAT32_MAX_VALUE),
                                   alias   = "hLim")
    l_lim:   AnalogueValue = Field(default = AnalogueValue(i = INT32_MIN_VALUE,
                                                           f = FLOAT32_MIN_VALUE),
                                   alias   = "lLim")
    ll_lim:  AnalogueValue = Field(default = AnalogueValue(i = INT32_MIN_VALUE,
                                                           f = FLOAT32_MIN_VALUE),
                                   alias   = "llLim")
    minimum: AnalogueValue = Field(default = AnalogueValue(i = INT32_MIN_VALUE,
                                                           f = FLOAT32_MIN_VALUE),
                                   alias   = "min")
    maximum: AnalogueValue = Field(default = AnalogueValue(i = INT32_MAX_VALUE,
                                                           f = FLOAT32_MAX_VALUE),
                                   alias   = "max")
    lim_db:  INT32U = field_int32u(default = 0,
                                   minimum = INT32U_MIN_VALUE,
                                   maximum = INT32U_MAX_VALUE,
                                   alias   = "limDb")

# IEC 61850-7-3 6.4
class ValWithTrans(BaseModel, validate_assignment = True):
    pos_val:   INT8    = Field(default = 0,
                               minimum = INT8_MIN_VALUE,
                               maximum = INT8_MAX_VALUE,
                               alias   = "posVal")
    trans_ind: BOOLEAN = Field(default = False,
                               alias   = "transInd")

# IEC 61850-7-3 6.5
class PulseConfig(BaseModel, validate_assignment = True):
    cmd_qual: OutputSignalKind = Field(default = OutputSignalKind.pulse,
                                       alias   = "cmdQual")
    on_dur:   INT32U = field_int32u(default = 0,
                                    minimum = INT32_MIN_VALUE,
                                    maximum = INT32_MAX_VALUE,
                                    alias   = "onDur")
    off_dur:  INT32U = field_int32u(default = 0,
                                    minimum = INT32_MIN_VALUE,
                                    maximum = INT32_MAX_VALUE,
                                    alias   = "offDur")
    num_pls:  INT32U = field_int32u(default = 0,
                                    minimum = INT32_MIN_VALUE,
                                    maximum = INT32_MAX_VALUE,
                                    alias   = "numPls")

# IEC 61850-7-3 6.6
class Unit(BaseModel, validate_assignment = True):
    si_unit:    SIUnitKind     = Field(default = SIUnitKind.dimensionless,
                                       alias   = "SIUnit")
    multiplier: MultiplierKind = Field(default = MultiplierKind.noprefix,
                                       alias   = "multiplier")

# IEC 61850-7-3 6.7
class Vector(BaseModel, validate_assignment = True):
    mag: AnalogueValue = Field(default = AnalogueValue(i = 0,
                                                       f = 0.0),
                               alias   = "mag")
    ang: AnalogueValue = Field(default = AnalogueValue(i = 0,
                                                       f = 0.0),
                               alias   = "ang")
# IEC 61850-7-3 6.8
class Point(BaseModel, validate_assignment = True):
    x_val: FLOAT32 = field_float32(default = 0.0,
                                   minimum = FLOAT32_MIN_VALUE,
                                   maximum = FLOAT32_MAX_VALUE,
                                   alias   = "xVal")
    y_val: FLOAT32 = field_float32(default = 0.0,
                                   minimum = FLOAT32_MIN_VALUE,
                                   maximum = FLOAT32_MAX_VALUE,
                                   alias   = "yVal")
    z_val: FLOAT32 = field_float32(default = 0.0,
                                   minimum = FLOAT32_MIN_VALUE,
                                   maximum = FLOAT32_MAX_VALUE,
                                   alias   = "zVal")

# IEC 61850-7-3 6.9
class Cell(BaseModel, validate_assignment = True):
    x_start: FLOAT32 = field_float32(default = 0.0,
                                     minimum = FLOAT32_MIN_VALUE,
                                     maximum = FLOAT32_MAX_VALUE,
                                     alias   = "xStart")
    x_end:   Optional[FLOAT32] = field_float32(default = 0.0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "xEnd")
    y_start: Optional[FLOAT32] = field_float32(default = 0.0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "yStart")
    y_end:   Optional[FLOAT32] = field_float32(default = 0.0,
                                               minimum = FLOAT32_MIN_VALUE,
                                               maximum = FLOAT32_MAX_VALUE,
                                               alias   = "yEnd")

# IEC 61850-7-3 6.10
class CalendarTime(BaseModel, validate_assignment = True):
    occ:      INT16U         = field_int16u(default = 0,
                                            minimum = INT16U_MIN_VALUE,
                                            maximum = INT16U_MAX_VALUE,
                                            alias   = "occ")
    occ_type: OccurrenceKind = Field(default = OccurrenceKind.time,
                                     alias   = "occType")
    occ_per:  PeriodKind     = Field(default = PeriodKind.hour,
                                     alias   = "occPer")
    week_day: WeekdayKind    = Field(default = WeekdayKind.monday,
                                     alias   = "weekDay")
    month:    MonthKind      = Field(default = MonthKind.january,
                                     alias   = "month")
    day:      INT8U          = field_int8u(default = 1,
                                           minimum = 1,
                                           maximum = 31,
                                           alias   = "day")
    hr:       INT8U          = field_int8u(default = 0,
                                           minimum = 0,
                                           maximum = 23,
                                           alias   = "hr")
    mn:       INT8U          = field_int8u(default = 0,
                                           minimum = 0,
                                           maximum = 59,
                                           alias   = "mn")

# IEC 61850-7-2 6.2.3.17
class Originator(BaseModel, validate_assignment = True):
    or_cat:   OriginatorCategoryKind = Field(default = OriginatorCategoryKind.process,
                                             alias   = "orCat")
    or_ident: Octet64                = field_octet64(default = "",
                                                     alias   = "orIdent")

# IEC 61850-7-2 6.2.3.10
class DetailQual(BaseModel):
    overflow:      BOOLEAN = Field(default = False,
                                   alias   = "overflow")
    out_of_range:  BOOLEAN = Field(default = False,
                                   alias   = "outOfRange")
    bad_reference: BOOLEAN = Field(default = False,
                                   alias   = "badReference")
    oscillatory:   BOOLEAN = Field(default = False,
                                   alias   = "oscillatory")
    failure:       BOOLEAN = Field(default = False,
                                   alias   = "failure")
    old_data:      BOOLEAN = Field(default = False,
                                   alias   = "oldData")
    inconsistent:  BOOLEAN = Field(default = False,
                                   alias   = "inconsistent")
    inaccurate:    BOOLEAN = Field(default = False,
                                   alias   = "inaccurate")

# IEC 61850-7-2 6.2.3.9
class Quality(BaseModel, validate_assignment = True):
    detail_qual:      DetailQual   = Field(default_factory = DetailQual,
                                           alias           = "detailQual")
    validity:         ValidityKind = Field(default = ValidityKind.good,
                                           alias   = "validity")
    source:           SourceKind   = Field(default = SourceKind.process,
                                           alias   = "source")
    test:             BOOLEAN      = Field(default = False,
                                           alias   = "test")
    operator_blocked: BOOLEAN      = Field(default = False,
                                           alias   = "operatorBlocked")

# IEC 61850-7-2 6.2.3.13
class RCBReportOptions(BaseModel, validate_assignment = True):
    sequence_number:      BOOLEAN = Field(default = False,
                                          alias   = "sequence-number")
    report_time_stamp:    BOOLEAN = Field(default = False,
                                          alias   = "report-time-stamp")
    reason_for_inclusion: BOOLEAN = Field(default = False,
                                          alias   = "reason-for-inclusion")
    data_set_name:        BOOLEAN = Field(default = False,
                                          alias   = "data-set-name")
    data_reference:       BOOLEAN = Field(default = False,
                                          alias   = "data-reference")
    buffer_overflow:      BOOLEAN = Field(default = False,
                                          alias   = "buffer-overflow")
    entry_id:             BOOLEAN = Field(default = False,
                                          alias   = "entryID")
    conf_revision:        BOOLEAN = Field(default = False,
                                          alias   = "conf-revision")
    segmentation:         BOOLEAN = Field(default = False,
                                          alias   = "segmentation")

# IEC 61850-7-2 6.2.3.15
class SVMessageOptions(BaseModel, validate_assignment = True):
    refresh_time:          BOOLEAN = Field(default = False,
                                           alias   = "refresh-time")
    reserved:              BOOLEAN = Field(default = False,
                                           alias   = "reserved")
    sample_rate:           BOOLEAN = Field(default = False,
                                           alias   = "sample-rate")
    data_set_name:         BOOLEAN = Field(default = False,
                                           alias   = "data-set-name")
    sample_mode:           BOOLEAN = Field(default = False,
                                           alias   = "sample-mode")
    synch_source_identity: BOOLEAN = Field(default = False,
                                           alias   = "synch-source-identity")

# IEC 61850-7-2 6.2.3.8
class TimeQuality(BaseModel, validate_assignment = True):
    leap_seconds_known:     BOOLEAN = Field(default = False,
                                            alias   = "LeapSecondsKnown")
    clock_failure:          BOOLEAN = Field(default = False,
                                            alias   = "ClockFailure")
    clock_not_synchronized: BOOLEAN = Field(default = False,
                                            alias   = "ClockNotSynchronized")
    time_accuracy:          INT8U   = field_int8u(default = 0,
                                                  minimum = 0,
                                                  maximum = 31,
                                                  alias   = "TimeAccuracy")

# IEC 61850-7-2 6.2.3.7
class Timestamp(BaseModel, validate_assignment = True):
    seconds_since_epoch: INT32U = field_int32u(default = 0,
                                               minimum = INT32U_MIN_VALUE,
                                               maximum = INT32U_MAX_VALUE,
                                               alias   = "SecondSinceEpoch")
    fraction_of_second:  INT24U = field_int24u(default = 0,
                                               minimum = INT24U_MIN_VALUE,
                                               maximum = INT24U_MAX_VALUE,
                                               alias   = "FractionOfSecond")
    time_quality:        TimeQuality = Field(default_factory = TimeQuality,
                                             alias           = "TimeQuality")

# IEC 61850-7-2 6.2.3.11
EntryTime = NewType('EntryTime',Timestamp)

# IEC 61850-7-2 6.2.3.12
class TriggerConditions(BaseModel, validate_assignment = True):
    data_change:           BOOLEAN = Field(default = False,
                                           alias   = "data-change")
    quality_change:        BOOLEAN = Field(default = False,
                                           alias   = "quality-change")
    data_update:           BOOLEAN = Field(default = False,
                                           alias   = "data-update")
    integrity:             BOOLEAN = Field(default = False,
                                           alias   = "integrity")
    general_interrogation: BOOLEAN = Field(default = False,
                                           alias   = "general-interrogation")

# IEC 61850-7-2 6.2.3.16
class CheckConditions(BaseModel, validate_assignment = True):
    synchrocheck:    BOOLEAN = Field(default = False,
                                     alias   = "synchrocheck")
    interlock_check: BOOLEAN = Field(default = False,
                                     alias   = "interlockCheck")

