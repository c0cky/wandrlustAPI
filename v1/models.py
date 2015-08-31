from django.db import models
from django.contrib.auth.models import User


# model for the post
class Post(models.Models):
    template = models.IntegerField(null=True, default=0)
    user = models.ForeignKey(User)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    profile_picture = models.ImageField(upload_to='', blank=True)
    password_token = models.Charfield(length=40, null=True, default='')
    authentication_token = models.CharField(lenght=40, null=True, default='')
