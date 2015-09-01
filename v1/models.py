from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='', blank=True)
    password_token = models.CharField(max_length=40, null=True, default='')
    activation_token = models.CharField(max_length=40, null=True,
                                        default='')
