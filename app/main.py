import time
import uuid
from fastapi import Request

from fastapi import FastAPI
from .router import tasks, auth
from app.db.models.task import Task


app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Request-ID"] = request_id

    print(
        f"[{request_id}] "
        f"{request.method} "
        f"{request.url.path} "
        f"→ {response.status_code} "
        f"→ {process_time:.4f}s"
    )

    return response

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"

    return response

@app.get("/")
async def root():
    return{
        "message": "Task Manager API"
    }


app.include_router(tasks.router)  # Included the tasks routes to main app
app.include_router(auth.router)