# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-26 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slides',
            name='photo',
            field=models.ManyToManyField(related_name='photos', to='database.Photos'),
        ),
    ]
