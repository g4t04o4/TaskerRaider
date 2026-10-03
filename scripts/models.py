from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


        
class TaskSchemaIn(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    
    name: str
    deadline: datetime # date first would cause Pydantic to mistakenly coerce datetime inputs into plain date objects, stripping away the time information
    desc: Optional[str] = ""
    tasktype_id: int
    
class TaskSchema(TaskSchemaIn):   
    id: int
    
    @model_validator(mode="before")
    @classmethod
    def validate_id(cls, t: Any):
        if isinstance(t, dict):
            if t.get("id") == "":
                del t["id"]
        return t
        
    
class TaskTypeSchemaIn(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")    
    
    name: str
    desc: Optional[str] = ""
 
class TaskTypeSchema(TaskTypeSchemaIn):   
    id: int
    
    @model_validator(mode="before")
    @classmethod
    def validate_id(cls, t: Any):
        if isinstance(t, dict):
            if t.get("id") == "":
                del t["id"]
        return t