from django.db import models
from apps.user.models import User

class Project(models.Model):
    project_id = models.CharField(max_length=30, unique=True)
    project_title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)
