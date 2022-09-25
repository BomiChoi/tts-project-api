from django.db import models

from apps.common.models import TimeStampedModel
from apps.user.models import User


class Project(TimeStampedModel):
    project_id = models.PositiveIntegerField(default=0)
    project_title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project_id', 'user'], name='unique_project_user')
        ]
