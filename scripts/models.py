from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

    
class TaskSchemaIn(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    
    name: str
    deadline: datetime # date first would cause Pydantic to mistakenly coerce datetime inputs into plain date objects, stripping away the time information
    desc: Optional[str] = ""
    tasktype_id: int
    
class TaskSchema(TaskSchemaIn):   
    id: int
    
class TaskTypeSchemaIn(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")    
    
    name: str
    desc: Optional[str] = ""
 
class TaskTypeSchema(TaskTypeSchemaIn):   
    id: int