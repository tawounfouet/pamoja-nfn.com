from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    #bio = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    




