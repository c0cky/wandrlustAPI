from django.db import models
from django.core.mail import EmailMessage
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import hashlib
import random
from django_comments.models import Comment


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The username must be set')
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = username
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        activation_token = hashlib.sha1(salt + usernamesalt).hexdigest()
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, date_joined=now,
                          activation_token=activation_token, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Send an activation email.
        message = "Hello and welcome to Wandrlust, \n"
        message += "Here is your activation token: "
        message += str(activation_token)
        user.send_email('Activate Your Wandrlust Account', message)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/',
                                        blank=True)
    header_picture = models.ImageField(upload_to='header_pictures/',
                                        blank=True)
    password_token = models.CharField(max_length=40, null=True, default='')
    activation_token = models.CharField(max_length=40, null=True,
                                        default='')
    bio = models.CharField(max_length=256, null=True, default='')
    objects = CustomUserManager()

    def send_email(self, subject=None, message=None):
        email = EmailMessage(subject, message, to=[self.email])
        return email.send()


class Image(models.Model):
    image = models.FileField(upload_to='images/', blank=True)
    caption = models.CharField(max_length=256, null=True, default='')


class Video(models.Model):
    video = models.FileField(upload_to='videos/', blank=True)
    caption = models.CharField(max_length=256, null=True, default='')


class Snippet(models.Model):
    snippet = models.TextField(default='', null=True)


class Post(models.Model):
    author = models.ForeignKey(User, null=True)
    submitted_date = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   null=True, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    null=True, default=0)
    title = models.CharField(max_length=100, null=True, default='')
    images = models.ManyToManyField(Image, through="PostImage",
                                    through_fields=('post', 'image'))
    videos = models.ManyToManyField(Video, through="PostVideo",
                                    through_fields=('post', 'video'))
    snippets = models.ManyToManyField(Snippet, through="PostSnippet",
                                      through_fields=('post', 'snippet'))

    def get_images(self):
        post_images = PostImage.objects.filter(post=self)
        return post_images

    def get_videos(self):
        post_videos = PostVideo.objects.filter(post=self)
        return post_videos

    def get_snippets(self):
        post_snippets = PostSnippet.objects.filter(post=self)
        return post_snippets

    def get_comments(self):
        post_comments = Comment.objects.filter(object_pk=self.pk)
        return post_comments


class PostImage(models.Model):
    image = models.ForeignKey(Image)
    post = models.ForeignKey(Post)
    position = models.IntegerField(default=0, null=True)


class PostVideo(models.Model):
    video = models.ForeignKey(Video)
    post = models.ForeignKey(Post)
    position = models.IntegerField(default=0, null=True)


class PostSnippet(models.Model):
    snippet = models.ForeignKey(Snippet)
    post = models.ForeignKey(Post)
    position = models.IntegerField(default=0, null=True)
