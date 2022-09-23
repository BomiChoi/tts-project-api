from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
