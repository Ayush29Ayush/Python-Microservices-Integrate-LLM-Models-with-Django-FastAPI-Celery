from django.db import models


class TaskStatus(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, default="PENDING")
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task {self.task_id} - {self.status}"


class RepoData(models.Model):
    repo_name = models.CharField(max_length=100)
    code_analysis = models.TextField()
