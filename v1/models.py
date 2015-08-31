from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User


# model for the post
class Post(models.Model):
    template = models.IntegerField(null=True, default=0)
    user = models.ForeignKey(User)


class User(AbstractBaseUser):
    profile_picture = models.ImageField(upload_to='', blank=True)
    password_token = models.CharField(length=40, null=True, default='')
    authentication_token = models.CharField(length=40, null=True, default='')
