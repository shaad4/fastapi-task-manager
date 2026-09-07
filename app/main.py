from fastapi import FastAPI
from .router import tasks
from app.db.models.task import Task


app = FastAPI()

@app.get("/")
async def root():
    return{
        "message": "Task Manager API"
    }


app.include_router(tasks.router)  # Included the tasks routes to main app