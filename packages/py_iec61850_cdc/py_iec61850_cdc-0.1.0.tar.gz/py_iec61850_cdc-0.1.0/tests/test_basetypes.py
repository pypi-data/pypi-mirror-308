# Test to confirm behavior of base IEC types.
# Basic IEC types are intended for use with Pydantic
# BaseModel to validate that the allowable ranges
# are obeyed (e.g. -128 <= INT8 <= 127).

import pytest
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError
)

# Note that TYPE_MIN_VALUE and TYPE_MAX_VALUE are
# not imported, as the field_TYPE functions should
# have optional parameters that auto-set maximums.
from py_iec61850_cdc.basetypes import (
    INT8,
    field_int8,
    INT16,
    field_int16,
    INT32,
    field_int32,
    INT64,
    field_int64,
    INT8U,
    field_int8u,
    INT16U,
    field_int16u,
    INT24U,
    field_int24u,
    INT32U,
    field_int32u,
    FLOAT32,
    field_float32,
    Octet64,
    field_octet64,
    VisString64,
    field_visstring64,
    VisString129,
    field_visstring129,
    VisString255,
    field_visstring255,
    Unicode255,
    field_unicode255,
    ObjectReference,
    field_objectreference,
    PhyComAddr,
    field_phycomaddr,
    ISO4217_CURRENCY_LIST,
    Currency,
    field_currency
)

# Test use of INT8 field within a pydantic BaseModel.
class INT8Test(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    int8_field: INT8 = field_int8()

class INT16Test(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    int16_field: INT16 = field_int16()

class INT32Test(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    int32_field: INT32 = field_int32()

class INT64Test(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    int64_field: INT64 = field_int64()

class INT8UTest(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    int8u_field: INT8U = field_int8u()

class INT16UTest(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    int16u_field: INT16U = field_int16u()

class INT24UTest(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    int24u_field: INT24U = field_int24u()

class INT32UTest(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    int32u_field: INT32U = field_int32u()

class FLOAT32Test(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    float32_field: FLOAT32 = field_float32()

class Octet64Test(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    octet64_field: Octet64 = field_octet64()

class VisString64Test(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    visstring64_field: VisString64 = field_visstring64()

class VisString129Test(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    visstring129_field: VisString129 = field_visstring129()

class VisString255Test(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    visstring255_field: VisString255 = field_visstring255()

class Unicode255Test(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    unicode255_field: Unicode255 = field_unicode255()

class ObjectReferenceTest(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    objectreference_field: ObjectReference = field_objectreference()

class PhyComAddrTest(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    phycomaddr_field: PhyComAddr = field_phycomaddr()

class EntryIDTest(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    phycomaddr_field: PhyComAddr = field_phycomaddr()

class CurrencyTest(BaseModel):
    model_config = ConfigDict(validate_assignment = True)
    currency_field: Currency = field_currency()

@pytest.fixture
def fix_int8():
    return INT8Test()

def test_int8_normal(fix_int8):
    myobj = fix_int8
    myobj.int8_field = -128
    myobj.int8_field = 127
    myobj.int8_field = 0
    
def test_int8_max(fix_int8):
    myobj = fix_int8
    with pytest.raises(ValidationError) as exc:
        myobj.int8_field = 128

def test_int8_min(fix_int8):
    myobj = fix_int8
    with pytest.raises(ValidationError) as exc:
        myobj.int8_field = -129

@pytest.fixture
def fix_int16():
    return INT16Test()

def test_int16_normal(fix_int16):
    myobj = fix_int16
    myobj.int16_field = -32768
    myobj.int16_field = 32767
    myobj.int16_field = 0

def test_int16_max(fix_int16):
    myobj = fix_int16
    with pytest.raises(ValidationError) as exc:
        myobj.int16_field = 32768

def test_int16_min(fix_int16):
    myobj = fix_int16
    with pytest.raises(ValidationError) as exc:
        myobj.int16_field = -32769

@pytest.fixture
def fix_int32():
    return INT32Test()

def test_int32_normal(fix_int32):
    myobj = fix_int32
    myobj.int32_field = -2147483648
    myobj.int32_field = 2147483647
    myobj.int32_field = 0

def test_int32_max(fix_int32):
    myobj = fix_int32
    with pytest.raises(ValidationError) as exc:
        myobj.int32_field = 2147483648

def test_int32_min(fix_int32):
    myobj = fix_int32
    with pytest.raises(ValidationError) as exc:
        myobj.int32_field = -2147483649

@pytest.fixture
def fix_int64():
    return INT64Test()

def test_int16_normal(fix_int64):
    myobj = fix_int64
    myobj.int64_field = -2**63
    myobj.int64_field = 2**63-1
    myobj.int64_field = 0

def test_int64_max(fix_int64):
    myobj = fix_int64
    with pytest.raises(ValidationError) as exc:
        myobj.int64_field = 2**63

def test_int64_min(fix_int64):
    myobj = fix_int64
    with pytest.raises(ValidationError) as exc:
        myobj.int64_field = -2**63-1

@pytest.fixture
def fix_int8u():
    return INT8UTest()

def test_int8u_normal(fix_int8u):
    myobj = fix_int8u
    myobj.int8u_field = 0
    myobj.int8u_field = 255
    myobj.int8u_field = 128

def test_int8u_max(fix_int8u):
    myobj = fix_int8u
    with pytest.raises(ValidationError) as exc:
        myobj.int8u_field = 256

def test_int8u_min(fix_int8u):
    myobj = fix_int8u
    with pytest.raises(ValidationError) as exc:
        myobj.int8u_field = -1

@pytest.fixture
def fix_int16u():
    return INT16UTest()

def test_int8u_normal(fix_int16u):
    myobj = fix_int16u
    myobj.int16u_field = 0
    myobj.int16u_field = 65535
    myobj.int16u_field = 32767

def test_int16u_max(fix_int16u):
    myobj = fix_int16u
    with pytest.raises(ValidationError) as exc:
        myobj.int16u_field = 65536

def test_int16u_min(fix_int16u):
    myobj = fix_int16u
    with pytest.raises(ValidationError) as exc:
        myobj.int16u_field = -1

@pytest.fixture
def fix_int24u():
    return INT24UTest()

def test_int24u_normal(fix_int24u):
    myobj = fix_int24u
    myobj.int24u_field = 0
    myobj.int24u_field = 16777215
    myobj.int24u_field = 65535

def test_int24u_max(fix_int24u):
    myobj = fix_int24u
    with pytest.raises(ValidationError) as exc:
        myobj.int24u_field = 16777216

def test_int24u_min(fix_int24u):
    myobj = fix_int24u
    with pytest.raises(ValidationError) as exc:
        myobj.int24u_field = -1

@pytest.fixture
def fix_int32u():
    return INT32UTest()

def test_int32u_normal(fix_int32u):
    myobj = fix_int32u
    myobj.int32u_field = 0
    myobj.int32u_field = 4294967295
    myobj.int32u_field = 16777215

def test_int32u_max(fix_int32u):
    myobj = fix_int32u
    with pytest.raises(ValidationError) as exc:
        myobj.int32u_field = 4294967296

def test_int32u_min(fix_int32u):
    myobj = fix_int32u
    with pytest.raises(ValidationError) as exc:
        myobj.int32u_field = -1

@pytest.fixture
def fix_float32():
    return FLOAT32Test()

def test_float32_normal(fix_float32):
    myobj = fix_float32
    myobj.float32_field = -3.4*(10**38)
    myobj.float32_field = 3.4*(10**38)
    myobj.float32_field = 0

def test_float32_max(fix_float32):
    myobj = fix_float32
    with pytest.raises(ValidationError) as exc:
        myobj.float32_field = 3.5*(10**38)
    with pytest.raises(ValidationError) as exc:
        myobj.float32_field = 3.4*(10**39)

def test_float32_min(fix_float32):
    myobj = fix_float32
    with pytest.raises(ValidationError) as exc:
        myobj.float32_field = -3.5*(10**38)
    with pytest.raises(ValidationError) as exc:
        myobj.float32_field = -3.4*(10**39)

@pytest.fixture
def fix_octet64():
    return Octet64Test()

def test_octet64_normal(fix_octet64):
    myobj = fix_octet64
    for i in range(64):
        myobj.octet64_field+="1"

def test_octet64_max(fix_octet64):
    myobj = fix_octet64
    for i in range(64):
        myobj.octet64_field+="1"
    with pytest.raises(ValidationError) as exc:
        myobj.octet64_field+="1"

@pytest.fixture
def fix_visstring64():
    return VisString64Test()

def test_visstring64_normal(fix_visstring64):
    myobj = fix_visstring64
    for i in range(64):
        myobj.visstring64_field+="1"

def test_visstring64_max(fix_visstring64):
    myobj = fix_visstring64
    for i in range(64):
        myobj.visstring64_field+="1"
    with pytest.raises(ValidationError) as exc:
        myobj.visstring64_field+="1"

@pytest.fixture
def fix_visstring129():
    return VisString129Test()

def test_visstring129_normal(fix_visstring129):
    myobj = fix_visstring129
    for i in range(129):
        myobj.visstring129_field+="1"

def test_visstring129_max(fix_visstring129):
    myobj = fix_visstring129
    for i in range(129):
        myobj.visstring129_field+="1"
    with pytest.raises(ValidationError) as exc:
        myobj.visstring129_field+="1"

@pytest.fixture
def fix_visstring255():
    return VisString255Test()

def test_visstring255_normal(fix_visstring255):
    myobj = fix_visstring255
    for i in range(255):
        myobj.visstring255_field+="1"

def test_visstring255_max(fix_visstring255):
    myobj = fix_visstring255
    for i in range(255):
        myobj.visstring255_field+="1"
    with pytest.raises(ValidationError) as exc:
        myobj.visstring255_field+="1"

@pytest.fixture
def fix_unicode255():
    return Unicode255Test()

def test_unicode255_normal(fix_unicode255):
    myobj = fix_unicode255
    for i in range(255):
        myobj.unicode255_field+="1"

def test_unicode255_max(fix_unicode255):
    myobj = fix_unicode255
    for i in range(255):
        myobj.unicode255_field+="1"
    with pytest.raises(ValidationError) as exc:
        myobj.unicode255_field+="1"

# ObjectReference is not tested.
# Other than enforcing a string type, it doesn't really
# do much.

# EntryID is not tested.
# Other than enforcing a string type, it doesn't really
# do much.

@pytest.fixture
def fix_currency():
    return CurrencyTest()

def test_currency_normal(fix_currency):
    myobj = fix_currency
    for i in ISO4217_CURRENCY_LIST:
        myobj.currency_field=i

def test_currency_len(fix_currency):
    myobj = fix_currency
    with pytest.raises(ValidationError) as exc:
        myobj.currency_field+="1"

def test_currency_fakecurrency(fix_currency):
    myobj = fix_currency
    with pytest.raises(ValidationError) as exc:
        myobj.currency_field="ZZZ"

