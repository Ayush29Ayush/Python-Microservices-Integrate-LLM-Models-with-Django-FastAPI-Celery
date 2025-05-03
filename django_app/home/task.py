from celery import Celery
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import TaskStatus
from groq import Groq
from celery import shared_task
from .models import RepoData
from home.utils.ai_agent import analyze_pr

# Set up Celery in Django
# app = Celery("django_app")
# app.config_from_object("django.conf:settings", namespace="CELERY")


# Celery task for processing file content and analyzing it
@shared_task
def analyze_repo_task(owner, repo, github_token=None):
    result = analyze_pr(owner, repo, github_token=None)
    return result
