# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-16 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_parser', '0004_parsedata_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='parsedata',
            name='education',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]