# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 21:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0011_auto_20160504_2116'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='porteruser',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='password',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='porteruser',
            name='username',
        ),
        migrations.AddField(
            model_name='porteruser',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
