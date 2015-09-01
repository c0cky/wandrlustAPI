# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='authentication_token',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password_token',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=b'', max_length=40),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=b'', max_length=40),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
