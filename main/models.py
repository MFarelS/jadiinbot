from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Session(models.Model):
    owner = models.OneToOneField(User, on_delete = models.PROTECT)
    session = models.TextField()