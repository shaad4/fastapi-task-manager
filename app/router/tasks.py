from fastapi import APIRouter, HTTPException
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

tasks=[]

@router.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    new_task ={
        "id": len(tasks)+1,
        "title": task.title,
        "description": task.description,
        "completed": False
    }

    tasks.append(new_task)

    return new_task


@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    completed: bool | None = None,
    skip: int = 0,
    limit: int = 10
):
    filtered_tasks = tasks

    if completed is not None:
        filtered_tasks = [
            task
            for task in filtered_tasks
            if task["completed"] == completed
        ]

    return filtered_tasks[skip:skip+limit]


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task Not Found"
    )


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate
):
    for task in tasks:
        if task["id"] == task_id:

            if task_update.title is not None:
                task["title"] = task_update.title

            if task_update.description is not None:
                task["description"] = task_update.description

            if task_update.completed is not None:
                task["completed"] = task_update.completed

            return task

    raise HTTPException(
        status_code=404,
        detail="Task Not Found"
    )


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)

            return {
                "message" : "Task is deleted"
            }

    raise HTTPException(
        status_code=404,
        detail="Task Not Found"
    )
    
