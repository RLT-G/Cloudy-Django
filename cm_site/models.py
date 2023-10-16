from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Добавьте свои дополнительные поля здесь
    artist_name = models.CharField('Artist name', max_length=64, blank=False, default="")
