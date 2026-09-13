from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, TypeAdapter

class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    deadline: datetime # date first would cause Pydantic to mistakenly coerce datetime inputs into plain date objects, stripping away the time information
    desc: Optional[str]
    tasktype_id: int
    
class TaskTypeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    desc: Optional[str]