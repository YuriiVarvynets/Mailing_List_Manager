# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mail_Manager_Site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='Last_Mail_Date',
            field=models.DateField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
