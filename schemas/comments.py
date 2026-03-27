from pydantic import BaseModel, Field, ConfigDict

class CommentCreateSchema(BaseModel):
    text: str = Field(..., min_length=1)

class CommentResponseSchema(BaseModel):
    id: int
    text: str
    task_id: int

    model_config = ConfigDict(from_attributes=True)
