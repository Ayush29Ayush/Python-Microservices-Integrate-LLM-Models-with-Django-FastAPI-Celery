from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult

from .task import analyze_repo_task


class StartTaskAPIView(APIView):
    """
    POST /start_task/  
    Accepts JSON with 'repo_url', 'pr_number', and optional 'github_token'.
    Triggers the Celery task and returns the task ID.
    """
    def post(self, request, *args, **kwargs):
        repo_url = request.data.get("repo_url")
        pr_number = request.data.get("pr_number")
        github_token = request.data.get("github_token")

        if not repo_url or pr_number is None:
            return Response({"error": "repo_url and pr_number are required"},status=status.HTTP_400_BAD_REQUEST)

        task = analyze_repo_task.delay(repo_url, pr_number, github_token)
        return Response({"task_id": task.id, "status": "Task started"}, status=status.HTTP_200_OK)


class TaskStatusAPIView(APIView):
    """
    GET /task_status/<task_id>/  
    Returns the current status of the given Celery task and its result or error.
    """
    def get(self, request, task_id, *args, **kwargs):
        result = AsyncResult(task_id)
        data = {"task_id": task_id, "status": result.state, "result": result.result}

        if result.state == "SUCCESS":
            data["result"] = result.result
            return Response(data, status=status.HTTP_200_OK)
        elif result.state == "FAILURE":
            data["error"] = str(result.result)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif result.state == "PENDING":
            return Response(data, status=status.HTTP_202_ACCEPTED)
        elif result.state == "REVOKED":
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data, status=status.HTTP_202_ACCEPTED)
