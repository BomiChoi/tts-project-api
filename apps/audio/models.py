from django.db import models

class Audio(models.Model):
    audio_id = models.CharField(max_length=30, unique=True)
    text = models.TextField()
    speed = models.DecimalField(max_digits=5, decimal_places=2)
    updated_time = models.DateTimeField(auto_now=True)
