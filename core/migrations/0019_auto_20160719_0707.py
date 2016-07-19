# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-19 07:07
from __future__ import unicode_literals

import colorful.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='color',
            field=colorful.fields.RGBColorField(default='#ffffff'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='label',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='repository',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
    ]
