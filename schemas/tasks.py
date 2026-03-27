from pydantic import BaseModel, Field, ConfigDict

class TaskBaseSchema(BaseModel):
    title: str = Field(min_length=3, max_length=100, description="Task title must be between 3 and 100 characters")
    description: str | None = Field(default=None, max_length=500)
    is_completed: bool = False

class TaskCreateSchema(TaskBaseSchema):
    pass

class TaskUpdateSchema(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    is_completed: bool | None = None

class TaskResponseSchema(TaskBaseSchema):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

