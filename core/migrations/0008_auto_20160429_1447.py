# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 14:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160429_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issuelog',
            name='object_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_log_object', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issuelog',
            name='subject_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_log_subject', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprojectrole',
            name='user',
            field=models.ManyToManyField(related_name='user_roles', to=settings.AUTH_USER_MODEL),
        ),
    ]
