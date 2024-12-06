# py_iec61850_cdc enumerated_data_attribute_types.py
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

# This file provides the enums described in IEC 61850-7-2:2010+AMD1:2020 and
# IEC 61850-7-3:2010+AMD1:2020 CSV as Python enums.  Some 61850-7-2 enums are
# not included.  The focus was on those necessary for 61850-7-3.

# Follows PEP-8 rules on function / variable naming (e.g. underscores).

from enum import Enum
from typing import NewType

# Casting Enum to EnumDA is based on text in IEC 61850-7-2.
# The implication is that many kinds of Enums could fit.
# So you'd have to pick one on the fly.
# All enumerations in this library are also derived from Enum,
# so the typing should work.
EnumDA = NewType('EnumDA',Enum)

# IEC 61850-7-3 8.2
class AngleReferenceKind(Enum):
    v             = 0
    a             = 1
    other         = 2
    synchrophaser = 3

# IEC 61850-7-3 8.3
class CtlModelKind(Enum):
    status_only                   = 0
    direct_with_normal_security   = 1
    sbo_with_normal_security      = 2
    direct_with_enhanced_security = 3
    sbo_with_enhanced_security    = 4

# IEC 61850-7-2 6.2.4.5
class ControlServiceStatusKind(Enum):
    unknown                        = 1
    not_supported                  = 2
    blocked_by_switching_hierarchy = 3
    select_failed                  = 4
    invalid_position               = 5
    position_reached               = 6
    parameter_change_in_execution  = 7
    step_limit                     = 8
    blocked_by_mode                = 9
    blocked_by_process             = 10
    blocked_by_interlocking        = 11
    command_already_in_execution   = 12
    blocked_by_health              = 13
    one_of_n_control               = 14
    abortion_by_cancel             = 15
    time_limit_over                = 16
    abortion_by_trip               = 17
    object_not_selected            = 18
    object_already_selected        = 19
    no_access_authority            = 20
    ended_with_overshoot           = 21
    abortion_due_to_deviation      = 22
    abortion_by_communication_loss = 23
    blocked_by_command             = 24
    none                           = 25
    inconsistent_parameters        = 26
    locked_by_other_client         = 27

# IEC 61850-7-3 8.4
class CurveCharKind(Enum):
    none                        = 0
    ansi_extremely_inverse      = 1
    ansi_very_inverse           = 2
    ansi_normal_inverse         = 3
    ansi_moderate_inverse       = 4
    ansi_definite_time          = 5
    long_time_extremely_inverse = 6
    long_time_very_inverse      = 7
    long_time_inverse           = 8
    iec_normal_inverse          = 9
    iec_very_inverse            = 10
    iec_inverse                 = 11
    iec_extremely_inverse       = 12
    iec_short_time_inverse      = 13
    iec_long_time_inverse       = 14
    iec_definite_time           = 15
    reserved                    = 16
    polynom_1                   = 17
    polynom_2                   = 18
    polynom_3                   = 19
    polynom_4                   = 20
    polynom_5                   = 21
    polynom_6                   = 22
    polynom_7                   = 23
    polynom_8                   = 24
    polynom_9                   = 25
    polynom_10                  = 26
    polynom_11                  = 27
    polynom_12                  = 28
    polynom_13                  = 29
    polynom_14                  = 30
    polynom_15                  = 31
    polynom_16                  = 32
    multiline_1                 = 33
    multiline_2                 = 34
    multiline_3                 = 35
    multiline_4                 = 36
    multiline_5                 = 37
    multiline_6                 = 38
    multiline_7                 = 39
    multiline_8                 = 40
    multiline_9                 = 41
    multiline_10                = 42
    multiline_11                = 43
    multiline_12                = 44
    multiline_13                = 45
    multiline_14                = 46
    multiline_15                = 47
    multiline_16                = 48

# IEC 61850-7-2 6.2.5.3
class DpStatusKind(Enum):
    intermediate_state= 0
    off=                1
    on=                 2
    bad_state=          3

# IEC 61850-7-3 8.5
class FaultDirectionKind(Enum):
    unknown  = 0
    forward  = 1
    backward = 2
    both     = 3

# IEC 61850-7-3 8.6
class HvReferenceKind(Enum):
    fundamental = 0
    rms         = 1
    absolute    = 2

# IEC 61850-7-3 8.7
class MonthKind(Enum):
    reserved  = 0
    january   = 1
    february  = 2
    march     = 3
    april     = 4
    may       = 5
    june      = 6
    july      = 7
    august    = 8
    september = 9
    october   = 10
    november  = 11
    december  = 12

# IEC 61850-7-3 8.8
# Note that 'u' is used instead of greek letter mu for Python purposes.
# 'noprefix' is used for the empty prefix for Python purposes.
class MultiplierKind(Enum):
    y  = -24
    z  = -21
    a  = -18
    f  = -15
    p  = -12
    n  = -9
    u  = -6
    m  = -3
    c  = -2
    d  = -1
    noprefix = 0
    da = 1
    h  = 2
    k  = 3
    M  = 6
    G  = 9
    T  = 12
    P  = 15
    E  = 18
    Z  = 21
    Y  = 24

# IEC 61850-7-3 8.9
class OccurrenceKind(Enum):
    time         = 0
    week_day     = 1
    week_of_year = 2
    day_of_month = 3
    day_of_year  = 4
    none         = 5

# IEC 61850-7-2 6.2.4.4
class OriginatorCategoryKind(Enum):
    not_supported     = 0
    bay_control       = 1
    station_control   = 2
    remote_control    = 3
    automatic_bay     = 4
    automatic_station = 5
    automatic_remote  = 6
    maintenance       = 7
    process           = 8

# IEC 61850-7-3 8.10
class OutputSignalKind(Enum):
    pulse               = 0
    persistent          = 1
    persistent_feedback = 2

# IEC 61850-7-3 8.11
class PeriodKind(Enum):
    hour  = 0
    day   = 1
    week  = 2
    month = 3
    year  = 4

# IEC 61850-7-3 8.12
class PhaseAngleReferenceKind(Enum):
    va            = 0
    vb            = 1
    vc            = 2
    aa            = 3
    ab            = 4
    ac            = 5
    vab           = 6
    vbc           = 7
    vca           = 8
    vother        = 9
    aother        = 10
    synchrophasor = 11

# IEC 61850-7-3 8.13
class PhaseFaultDirectionKind(Enum):
    unknown  = 0
    forward  = 1
    backward = 2

# IEC 61850-7-3 8.14
class PhaseReferenceKind(Enum):
    a             = 0
    b             = 1
    c             = 2
    synchrophasor = 3

# IEC 61850-7-3 8.15
class RangeKind(Enum):
    normal    = 0
    high      = 1
    low       = 2
    high_high = 3
    low_low   = 4

# IEC 61850-7-2 6.2.4.6
class SamplingModeKind(Enum):
    samples_per_period = 0
    samples_per_second = 1
    seconds_per_sample = 2

# IEC 61850-7-3 8.17
class SboClassKind(Enum):
    operate_once = 0
    operate_many = 1

# IEC 61850-7-3 8.18
class SequenceKind(Enum):
    pos_neg_zero  = 0
    dir_quad_zero = 1

# IEC 61850-7-2 6.2.4.2
class ServiceNameKind(Enum):
    unknown                      = 0
    associate                    = 1
    abort                        = 2
    release                      = 3
    get_server_directory         = 4
    get_logical_device_directory = 5
    get_all_data_values          = 6
    get_data_values              = 7
    set_data_values              = 8
    get_data_directory           = 9
    get_data_definition          = 10
    get_data_set_values          = 11
    set_data_set_values          = 12
    create_data_set              = 13
    delete_data_set              = 14
    get_data_set_directory       = 15
    select_active_sg             = 16
    select_edit_sg               = 17
    set_edit_sg_value            = 18
    confirm_edit_sg_values       = 19
    get_edit_sg_value            = 20
    get_sgcb_values              = 21
    report                       = 22
    get_brcb_values              = 23
    set_brcb_values              = 24
    get_urcb_values              = 25
    set_urcb_values              = 26
    get_lcb_values               = 27
    set_lcb_values               = 28
    query_log_by_time            = 29
    query_log_after              = 30
    get_log_status_values        = 31
    send_goose_message           = 32
    get_go_cb_values             = 33
    set_go_cb_values             = 34
    get_go_reference             = 35
    get_goose_element_number     = 36
    send_msv_message             = 37
    get_msvcb_values             = 38
    set_msvcb_values             = 39
    send_usv_message             = 40 # deprecated
    get_usvcb_values             = 41 # deprecated
    set_usvcb_values             = 42 # deprecated
    select                       = 43
    select_with_value            = 44
    cancel                       = 45
    operate                      = 46
    command_termination          = 47
    time_activated_operate       = 48
    get_file                     = 49
    set_file                     = 50
    delete_file                  = 51
    get_file_attributes          = 52
    time_synchronization         = 53
    internal_change              = 54
    get_logical_node_directory   = 55
    get_msv_reference            = 56
    get_msv_element_number       = 57

# IEC 61850-7-2 6.2.4.3
class ServiceStatusKind(Enum):
    no_error                                = 0
    instance_not_available                  = 1
    instance_in_use                         = 2
    access_violation                        = 3
    access_not_allowed_in_current_state     = 4
    parameter_value_inappropriate           = 5
    parameter_value_inconsistent            = 6
    class_not_supported                     = 7
    instance_locked_by_other_client         = 8
    control_must_be_selected                = 9 # deprecated
    type_conflict                           = 10
    failed_due_to_communications_constraint = 11
    failed_due_to_server_constraint         = 12

# IEC 61850-7-3 8.19
class SeverityKind(Enum):
    unknown  = 0
    critical = 1
    major    = 2
    minor    = 3
    warning  = 4

# IEC 61850-7-3 8.16
# Uses description names instead of enumerators, due to symbology.
# e.g. m/s is not OK in Python
# e.g. metres_per_second is OK in Python
# Watch the international spellings (e.g. metre vs meter) - as per IEC.
class SIUnitKind(Enum):
    dimensionless                 = 1
    metre                         = 2
    kilogram                      = 3
    second                        = 4
    ampere                        = 5
    kelvin                        = 6
    mole                          = 7
    candela                       = 8
    degrees                       = 9
    radian                        = 10
    steradian                     = 11
    gray                          = 21
    becquerel                     = 22
    degrees_celsius               = 23
    sievert                       = 24
    farad                         = 25
    coulomb                       = 26
    siemens                       = 27
    henry                         = 28
    volt                          = 29
    ohm                           = 30
    joule                         = 31
    newton                        = 32
    hertz                         = 33
    lux                           = 34
    lumen                         = 35
    weber                         = 36
    tesla                         = 37
    watt                          = 38
    pascal                        = 39
    square_meter                  = 41
    cubic_meter                   = 42
    metres_per_second             = 43
    metres_per_second_square      = 44
    cubic_metres_per_second       = 45
    metres_per_cubic_metre        = 46
    kilogram_metre                = 47
    kilogram_per_cubic_metre      = 48
    metre_square_per_second       = 49
    watt_per_metre_kelvin         = 50
    joule_per_kelvin              = 51
    parts_per_million             = 52
    rotations_per_second          = 53
    radian_per_second             = 54
    watt_per_square_metre         = 55
    watt_seconds_per_square_metre = 56
    siemens_per_metre             = 57
    kelvin_per_second             = 58
    pascal_per_second             = 59
    joule_per_kilogram_per_kelvin = 60
    volt_ampere                   = 61
    watts_deprecated              = 62
    volt_ampere_reactive          = 63
    phase_angle_deprecated        = 64
    power_factor                  = 65 # Also dimensionless...
    volt_seconds                  = 66
    volt_squared                  = 67
    amp_second                    = 68
    amp_square                    = 69
    amp_squared_time              = 70
    volt_ampere_hours             = 71
    watt_hours                    = 72
    volt_ampere_reactive_hours    = 73
    volts_per_hertz               = 74
    hertz_per_second              = 75
    characters                    = 76
    characters_per_second         = 77
    kilogram_square_metre         = 78 # 'kg square meter' in the standard, but aligning with kg above.
    decibel                       = 79
    joule_per_watt_hour           = 80
    watt_per_second               = 81
    litres_per_second             = 82
    power_level_dbm               = 83 # dBm
    hour                          = 84
    minute                        = 85
    ohm_per_metre                 = 86
    percentage_per_second         = 87
    ampere_per_volt               = 88
    ampere_per_volt_second        = 89

# IEC 61850-7-2 6.2.5.4
class SourceKind(Enum):
    process     = 0
    substituted = 1

# IEC 61850-7-2 6.2.5.2
class StepControlKind(Enum):
    stop     = 0
    lower    = 1
    higher   = 2
    reserved = 3

# IEC 61850-7-2 6.2.5.5
class ValidityKind(Enum):
    good         = 0
    invalid      = 1
    reserved     = 2
    questionable = 3

# IEC 61850-7-3 8.20
class WeekdayKind(Enum):
    reserved  = 0
    monday    = 1
    tuesday   = 2
    wednesday = 3
    thursday  = 4
    friday    = 5
    saturday  = 6
    sunday    = 7

