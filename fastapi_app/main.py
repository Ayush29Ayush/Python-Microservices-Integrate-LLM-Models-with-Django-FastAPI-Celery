import time
from fastapi import FastAPI, status
import httpx
from decouple import config
from .models import AnalyzePRRequest

app = FastAPI()

DJANGO_API_URL = config("DJANGO_API_URL", default="http://localhost:8001")

@app.get("/")
async def root():
    """
    This is the root endpoint
    """
    # Time taken to run this endpoint
    start_time = time.time()
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    return {"message": "Hello World", "response_time": response_time}

@app.post("/start_task/")
async def start_task_endpoint(task_request: AnalyzePRRequest):
    """
    Trigger the task in Django and return the task ID.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DJANGO_API_URL}/start_task/",
            data={
                "repo_url": task_request.repo_url,
                "pr_number": task_request.pr_number,
                "github_token": task_request.github_token,
            },
        )
        if response.status_code != 200:
            return {"error": "Failed to start task", "details": response.text, "status": status.HTTP_500_INTERNAL_SERVER_ERROR}
        task_id = response.json().get("task_id")
        return {"task_id": task_id, "status": "Task started"}


@app.get("/task_status/{task_id}/")
async def task_status_endpoint(task_id: str):
    """
    Check the status of the task by making a request to Django.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_API_URL}/task_status/{task_id}/")
        return response.json()

    return {"message": "something went wrong", "details": response.text , "status": status.HTTP_400_BAD_REQUEST}