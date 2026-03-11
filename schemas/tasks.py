from typing import Literal

from pydantic import BaseModel, Field

class BaseTask(BaseModel):
    name: str = Field(min_length=2, max_length=14)
    priority: Literal["low", "middle", "high"]
    description: str
    
class CreateTask(BaseTask):
    responsible: str
    deadline: str
    
class EditTask(BaseTask):
    description: str