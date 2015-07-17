# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extraction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='blacklisted',
            field=models.BooleanField(default=False, verbose_name='Is blacklisted'),
            preserve_default=True,
        ),
    ]
