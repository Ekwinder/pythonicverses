# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voterlist',
            name='voted',
            field=models.IntegerField(default=0),
        ),
    ]
