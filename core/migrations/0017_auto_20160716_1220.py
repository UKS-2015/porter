# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-16 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20160614_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('OPENED', 'Opened'), ('ASSIGNED', 'Assigned'), ('CLOSED', 'Closed')], default='Opened', max_length=8),
        ),
        migrations.AlterField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(blank=True, to='core.Label'),
        ),
    ]