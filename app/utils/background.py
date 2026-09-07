from datetime import datetime


def log_task_creation(task_id: int):
    with open("task_activity.log", "a") as file:
        file.write(
            f"Task {task_id} created at "
            f"{datetime.now()}\n"
        )