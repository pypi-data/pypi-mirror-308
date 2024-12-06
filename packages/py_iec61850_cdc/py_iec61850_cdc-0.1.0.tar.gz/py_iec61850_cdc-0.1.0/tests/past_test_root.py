#!/home/kyle/Programming/python/py-iec61850-cdc/bin/python3

import json

from typing import List

from pydantic import BaseModel, RootModel, Field
#from pydantic.schema import schema

class ListItem(BaseModel):
    i: int = Field(default = 0)
    f: int = Field(default = 0)

class MyList(RootModel):
    root: List[ListItem] = None

class ListContainer(BaseModel):
    mylist: MyList = Field(default_factory=MyList)

mynewlist = ListContainer()
mynewlist.mylist = MyList([ListItem(i=3,f=4),ListItem(i=2,f=1)])

mynewnewlist = ListContainer.model_validate_json(mynewlist.model_dump_json())
print(json.dumps(mynewnewlist.model_dump(),indent=2))

