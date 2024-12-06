# py_iec61850_cdc basetypes.py
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

# This file provides the basic IEC types described under clause 6.2.2 of
# IEC 61850-7-2:2010+AMD1:2020 CSV as a Python class. The types are
# deliberately cast to Python types using NewType, mostly so the documentation
# can follow the standard. In reality, simple Python types are used.

# Some helper functions are provided to set up Pydantic Fields in other files.

from typing import NewType, Optional
from pydantic import Field

# BOOLEAN - IEC 61850-7-2 6.2.2.2
BOOLEAN        = NewType('BOOLEAN',bool)

# INT8 - IEC 61850-7-2 6.2.2.3
INT8           = NewType('INT8',int)
INT8_MIN_VALUE = -128
INT8_MAX_VALUE = 127
def field_int8(default: int = 0,
               minimum: int = INT8_MIN_VALUE,
               maximum: int = INT8_MAX_VALUE,
               alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 ge      = minimum,
                 le      = maximum,
                 alias   = alias)

# INT16 - IEC 61850-7-2 6.2.2.4
INT16           = NewType('INT16',int)
INT16_MIN_VALUE = -32768
INT16_MAX_VALUE = 32767
def field_int16(default: int = 0,
                minimum: int = INT16_MIN_VALUE,
                maximum: int = INT16_MAX_VALUE,
                alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 ge      = minimum,
                 le      = maximum,
                 alias   = alias)

# INT32 - IEC 61850-7-2 6.2.2.5
INT32           = NewType('INT32',int)
INT32_MIN_VALUE = -2147483648
INT32_MAX_VALUE = 2147483647
def field_int32(default: int = 0,
                minimum: int = INT32_MIN_VALUE,
                maximum: int = INT32_MAX_VALUE,
                alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 ge      = minimum,
                 le      = maximum,
                 alias   = alias)

# INT64 - IEC 61850-7-2 6.2.2.6
INT64           = NewType('INT64',int)
INT64_MIN_VALUE = -2**63
INT64_MAX_VALUE = (2**63)-1
def field_int64(default: int = 0,
                minimum: int = INT64_MIN_VALUE,
                maximum: int = INT64_MAX_VALUE,
                alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 ge      = minimum,
                 le      = maximum,
                 alias   = alias)

# INT8U - IEC 61850-7-2 6.2.2.7
INT8U           = NewType('INT8U',int)
INT8U_MIN_VALUE = 0
INT8U_MAX_VALUE = 255
def field_int8u(default: int = 0,
                minimum: int = INT8U_MIN_VALUE,
                maximum: int = INT8U_MAX_VALUE,
                alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 ge      = minimum,
                 le      = maximum,
                 alias   = alias)

# INT16U - IEC 61850-7-2 6.2.2.8
INT16U           = NewType('INT16U',int)
INT16U_MIN_VALUE = 0
INT16U_MAX_VALUE = 65535
def field_int16u(default: int = 0,
                 minimum: int = INT16U_MIN_VALUE,
                 maximum: int = INT16U_MAX_VALUE,
                 alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 ge      = minimum,
                 le      = maximum,
                 alias   = alias)

# INT24U - IEC 61850-7-2 6.2.2.9
INT24U           = NewType('INT24U',int)
INT24U_MIN_VALUE = 0
INT24U_MAX_VALUE = 16777215
def field_int24u(default: int = 0,
                 minimum: int = INT24U_MIN_VALUE,
                 maximum: int = INT24U_MAX_VALUE,
                 alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 ge      = minimum,
                 le      = maximum,
                 alias   = alias)

# INT32U - IEC 61850-7-2 6.2.2.10
INT32U           = NewType('INT32U',int)
INT32U_MIN_VALUE = 0
INT32U_MAX_VALUE = 4294967295
def field_int32u(default: int = 0,
                 minimum: int = INT32U_MIN_VALUE,
                 maximum: int = INT32U_MAX_VALUE,
                 alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 ge      = minimum,
                 le      = maximum,
                 alias   = alias)

# FLOAT32 - IEC 61850-7-2 6.2.2.11
FLOAT32      = NewType('FLOAT32',float)
FLOAT32_MIN_VALUE = -3.40*(10**38)
FLOAT32_MAX_VALUE = 3.40*(10**38)
def field_float32(default: float = 0.0,
                  minimum: float = FLOAT32_MIN_VALUE,
                  maximum: float = FLOAT32_MAX_VALUE,
                  alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 ge      = minimum,
                 le      = maximum,
                 alias   = alias)

# OCTET64 - IEC 61850-7-2 6.2.2.12
Octet64      = NewType('Octet64',str)
def field_octet64(default: str = "",
                  alias:   Optional[str] = None) -> Field:
    return Field(default    = default,
                 max_length = 64,
                 alias      = alias)

# VISSTRING64 - IEC 61850-7-2 6.2.2.13
VisString64  = NewType('VisString64',str)
def field_visstring64(default: str = "",
                      alias:   Optional[str] = None) -> Field:
    return Field(default    = default,
                 max_length = 64,
                 alias      = alias)

# VISSTRING129 - IEC 61850-7-2 6.2.2.14
VisString129 = NewType('VisString129',str)
def field_visstring129(default: str = "",
                       alias:   Optional[str] = None) -> Field:
    return Field(default    = default,
                 max_length = 129,
                 alias      = alias)

# VISSTRING255 - IEC 61850-7-2 6.2.2.15
VisString255 = NewType('VisString255',str)
def field_visstring255(default: str = "",
                       alias:   Optional[str] = None) -> Field:
    return Field(default    = default,
                 max_length = 255,
                 alias      = alias)

# UNICODE255 - IEC 61850-7-2 6.2.2.16
Unicode255   = NewType('Unicode255',str)
def field_unicode255(default: str = "",
                     alias:   Optional[str] = None) -> Field:
    return Field(default    = default,
                 max_length = 255,
                 alias      = alias)

# OBJECTREFERENCE - IEC 61850-7-2 6.2.3.4
ObjectReference = NewType('ObjectReference',VisString129)
def field_objectreference(default: str = "",
                          alias:   Optional[str] = None) -> Field:
    return field_visstring129(default = default,
                              alias   = alias)

# PHYCOMADDR - IEC 61850-7-2 6.2.3.2
PhyComAddr   = NewType('PhyComAddr',str)
def field_phycomaddr(default: str = "",
                     alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 alias   = alias)

# ENTRYID - IEC 61850-7-2 6.2.3.5
EntryID      = NewType('EntryID',str)
def field_entryid(default: str = "",
                  alias:   Optional[str] = None) -> Field:
    return Field(default = default,
                 alias   = alias)

# List below sourced from Wikipedia rather than
# the actual standard.  Apologies for errors.
ISO4217_CURRENCY_LIST = [
    "AED",
    "AFN",
    "ALL",
    "AMD",
    "ANG",
    "AOA",
    "ARS",
    "AUD",
    "AWG",
    "AZN",
    "BAM",
    "BBD",
    "BDT",
    "BGN",
    "BHD",
    "BIF",
    "BMD",
    "BND",
    "BOB",
    "BOV",
    "BRL",
    "BSD",
    "BTN",
    "BWP",
    "BYN",
    "BZD",
    "CAD",
    "CDF",
    "CHE",
    "CHF",
    "CHW",
    "CLF",
    "CLP",
    "CNY",
    "COP",
    "COU",
    "CRC",
    "CUP",
    "CVE",
    "CZK",
    "DJF",
    "DKK",
    "DOP",
    "DZD",
    "EGP",
    "ERN",
    "ETB",
    "EUR",
    "FJD",
    "FKP",
    "GBP",
    "GEL",
    "GHS",
    "GIP",
    "GMD",
    "GNF",
    "GTQ",
    "GYD",
    "HKD",
    "HNL",
    "HTG",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "IQD",
    "IRR",
    "ISK",
    "JMD",
    "JOD",
    "JPY",
    "KES",
    "KGS",
    "KHR",
    "KMF",
    "KPW",
    "KRW",
    "KWD",
    "KYD",
    "KZT",
    "LAK",
    "LBP",
    "LKR",
    "LRD",
    "LSL",
    "LYD",
    "MAD",
    "MDL",
    "MGA",
    "MKD",
    "MMK",
    "MNT",
    "MOP",
    "MRU",
    "MUR",
    "MVR",
    "MWK",
    "MXN",
    "MXV",
    "MYR",
    "MZN",
    "NAD",
    "NGN",
    "NIO",
    "NOK",
    "NPR",
    "NZD",
    "OMR",
    "PAB",
    "PEN",
    "PGK",
    "PHP",
    "PKR",
    "PLN",
    "PYG",
    "QAR",
    "RON",
    "RSD",
    "RUB",
    "RWF",
    "SAR",
    "SBD",
    "SCR",
    "SDG",
    "SEK",
    "SGD",
    "SHP",
    "SLE",
    "SOS",
    "SRD",
    "SSP",
    "STN",
    "SVC",
    "SYP",
    "SZL",
    "THB",
    "TJS",
    "TMT",
    "TND",
    "TOP",
    "TRY",
    "TTD",
    "TWD",
    "TZS",
    "UAH",
    "UGX",
    "USD",
    "USN",
    "UYI",
    "UYU",
    "UYW",
    "UZS",
    "VED",
    "VES",
    "VND",
    "VUV",
    "WST",
    "XAF",
    "XAG",
    "XAU",
    "XBA",
    "XBB",
    "XBC",
    "XBD",
    "XCD",
    "XDR",
    "XOF",
    "XPD",
    "XPF",
    "XPT",
    "XSU",
    "XTS",
    "XUA",
    "XXX",
    "YER",
    "ZAR",
    "ZMW",
    "ZWG"
]

# CURRENCY - IEC 61850-7-2 6.2.3.6
Currency     = NewType('Currency',str)
def field_currency(default: str = "XXX",
                   alias:   Optional[str] = None) -> Field:

    # Build the regex string for pattern from the
    # currency list.
    patternstring = ""
    first = True
    for i in ISO4217_CURRENCY_LIST:
        if first:
            patternstring += i
            first = False
        else:
            patternstring += "|"
            patternstring += i 

    return Field(default    = default,
                 max_length = 3,
                 alias      = alias,
                 pattern    = patternstring)
