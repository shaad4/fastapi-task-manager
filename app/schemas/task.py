from pydantic import BaseModel, ConfigDict

class TaskCreate(BaseModel):
    title: str 
    description: str | None = None
    priority: int = 1

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: int | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    priority: int

    model_config = ConfigDict(from_attributes=True)