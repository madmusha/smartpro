# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 18:53
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0008_auto_20160926_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutproduct',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 9, 26, 18, 53, 5, 506958, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='consumableincome',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 9, 26, 18, 53, 5, 506333, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 26, 18, 53, 5, 509225)),
        ),
    ]
