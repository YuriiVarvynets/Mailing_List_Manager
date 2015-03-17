# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.CharField(serialize=False, max_length=82, primary_key=True)),
                ('Owner_Label_Name', models.CharField(max_length=100, null=True)),
                ('Mail_Address', models.CharField(max_length=50, null=True)),
                ('Mail_City', models.CharField(max_length=25, null=True)),
                ('Mail_State', models.CharField(max_length=2, null=True)),
                ('Mail_Zip', models.CharField(max_length=5, null=True)),
                ('Property_Address', models.CharField(max_length=50, null=True)),
                ('Property_City', models.CharField(max_length=25, null=True)),
                ('Property_State', models.CharField(max_length=2, null=True)),
                ('Property_Zip', models.IntegerField(max_length=5, null=True)),
                ('Property_Type', models.CharField(max_length=20, null=True)),
                ('Equity', models.CharField(max_length=3, null=True, blank=True)),
                ('Absentee_Owned', models.CharField(max_length=3, null=True)),
                ('Last_Mail_Date', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
