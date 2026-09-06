from fastapi import FastAPI
from .router import tasks


app = FastAPI()

@app.get("/")
async def root():
    return{
        "message": "Task Manager API"
    }


app.include_router(tasks.router)  # Included the tasks routes to main app