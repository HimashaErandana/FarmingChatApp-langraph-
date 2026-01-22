'''from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v,**kwargs):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class MesaageModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    message: str
    msgType: str   # user | ai
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
'''
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class MessageModel(BaseModel):
    # Make _id optional, default to None, Pydantic alias _id
    id: Optional[str] = Field(default=None, alias="_id")  
    message: str
    msgType: str  # "user" or "AI"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        # Use this so Pydantic can ignore None values on export
        exclude_none=True
    )


#working

'''

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Any
from bson import ObjectId
from datetime import datetime
import json


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, *args, **kwargs):
        from pydantic_core import core_schema
        
        def validate_from_str(value: str) -> ObjectId:
            if ObjectId.is_valid(value):
                return ObjectId(value)
            raise ValueError("Invalid ObjectId")
        
        from_str_schema = core_schema.chain_schema([
            core_schema.str_schema(),
            core_schema.no_info_plain_validator_function(validate_from_str)
        ])
        
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                from_str_schema,
            ]),
            serialization=core_schema.to_string_ser_schema(),
        )


class MesaageModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    message: str
    msgType: str  # user | ai
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str,
        }
    )

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        if v is None:
            return PyObjectId()
        return v
'''