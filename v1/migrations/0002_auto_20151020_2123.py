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
            name='modified_date',
        ),
        migrations.AddField(
            model_name='user',
            name='header_picture',
            field=models.ImageField(upload_to=b'header_pictures/', blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(upload_to=b'images/', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(upload_to=b'profile_pictures/', blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to=b'videos/', blank=True),
        ),
    ]
