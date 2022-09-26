from django.db import models

from apps.common.models import TimeStampedModel
from apps.project.models import Project


class Audio(TimeStampedModel):
    audio_id = models.PositiveIntegerField(default=0)
    text = models.TextField()
    speed = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_time = None

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['audio_id', 'project'], name='unique_audio_project')
        ]

    def __str__(self):
        return f'Audio {self.id} - {self.text}'
