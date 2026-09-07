from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import select

from app.dependencies.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.db.models.task import Task


router = APIRouter()



@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
   


@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    db: Session = Depends(get_db),
    completed: bool | None = None,
    skip: int = 0,
    limit: int = 10
):
    statement = select(Task)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    statement = statement.offset(skip).limit(limit)

    result = db.execute(statement)

    return result.scalars().all()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Task).where(Task.id == task_id)

    result = db.execute(statement)

    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status=404,
            detail="Task is Not Found"
        )
    
    return task
    


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    statement = select(Task).where(Task.id == task_id)

    result = db.execute(statement)

    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )

    if task_update.title is not None:
        task.title = task_update.title

    if task_update.description is not None:
        task.description = task_update.description

    if task_update.completed is not None:
        task.completed = task_update.completed

    if task_update.priority is not None:
        task.priority = task_update.priority

    db.commit()
    db.refresh(task)

    return task

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Task).where(Task.id == task_id)
    result = db.execute(statement)

    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
                status_code=404,
                detail="Task Not Found"
            )

    db.delete(task)
    db.commit()

    return {
        "message" : "Task is Deleted"
    }

    
    
