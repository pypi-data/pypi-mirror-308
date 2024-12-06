#!/home/kyle/Programming/python/py-iec61850-cdc/bin/python3

from pydantic import BaseModel, Field
import json

from py_iec61850_cdc.basetypes  import INT32,field_int32,VisString255
from py_iec61850_cdc.attributes import AnalogueValue
from py_iec61850_cdc.abstracts  import ENC
from py_iec61850_cdc.status     import SPS
from py_iec61850_cdc.measurand  import MV, HWYE

class TestClass(BaseModel):
    i: INT32    = field_int32(default = 0,
                              minimum = 0,
                              maximum = 12,
                              alias   = "yarp")

testmodel = TestClass()

print(testmodel.model_dump_json(by_alias=True))

class TestModel(MV):
    d: VisString255 = Field(default = "TestModel")

testmodel = TestModel()

print(testmodel.model_dump_json())

testmodel.d = "fuckyeah"

print(testmodel.model_dump_json(by_alias=True))

f = open("testfile.txt", "w")
f.write(testmodel.model_dump_json(by_alias=True))
f.close()

print("====== Building testmodel2 ======")
testmodel2 = MV.model_validate_json(testmodel.model_dump_json(by_alias=True))

print("====== Dumping testmodel2 model_dump (json) ======")
json_output = json.loads(testmodel2.model_dump_json(by_alias=True))
print(json.dumps(json_output, indent = 2))

try:
    testmodel.d = 0.0
except Exception:
    print("Can't set testmodel.d to 0.0!")

try:
    testmodel.cdc_name = "ENC"
except Exception:
    print("Can't change to 'ENC'!")

try:
    testmodel.cdc_name = "DERP"
except Exception:
    print("Can't change to 'DERP'!")


