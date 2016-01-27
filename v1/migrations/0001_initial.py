# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import v1.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profile_picture', models.ImageField(upload_to=b'', blank=True)),
                ('password_token', models.CharField(default=b'', max_length=40, null=True)),
                ('activation_token', models.CharField(default=b'', max_length=40, null=True)),
                ('bio', models.CharField(default=b'', max_length=256, null=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', v1.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.FileField(upload_to=b'', blank=True)),
                ('caption', models.CharField(default=b'', max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submitted_date', models.DateTimeField(auto_now=True)),
                ('modified_date', models.DateTimeField(default=0, null=True)),
                ('latitude', models.DecimalField(default=0, null=True, max_digits=9, decimal_places=6)),
                ('longitude', models.DecimalField(default=0, null=True, max_digits=9, decimal_places=6)),
                ('title', models.CharField(default=b'', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField(default=0, null=True)),
                ('image', models.ForeignKey(to='v1.Image')),
                ('post', models.ForeignKey(to='v1.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PostSnippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField(default=0, null=True)),
                ('post', models.ForeignKey(to='v1.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PostVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField(default=0, null=True)),
                ('post', models.ForeignKey(to='v1.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('snippet', models.TextField(default=b'', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video', models.FileField(upload_to=b'', blank=True)),
                ('caption', models.CharField(default=b'', max_length=256, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='postvideo',
            name='video',
            field=models.ForeignKey(to='v1.Video'),
        ),
        migrations.AddField(
            model_name='postsnippet',
            name='snippet',
            field=models.ForeignKey(to='v1.Snippet'),
        ),
        migrations.AddField(
            model_name='post',
            name='images',
            field=models.ManyToManyField(to='v1.Image', through='v1.PostImage'),
        ),
        migrations.AddField(
            model_name='post',
            name='snippets',
            field=models.ManyToManyField(to='v1.Snippet', through='v1.PostSnippet'),
        ),
        migrations.AddField(
            model_name='post',
            name='videos',
            field=models.ManyToManyField(to='v1.Video', through='v1.PostVideo'),
        ),
    ]
