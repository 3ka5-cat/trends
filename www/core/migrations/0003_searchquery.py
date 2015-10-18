# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_vacancy_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255, verbose_name='Text to search')),
                ('note', models.TextField(verbose_name='Note', blank=True)),
            ],
            options={
                'verbose_name': 'Search query',
                'verbose_name_plural': 'Search queries',
            },
            bases=(models.Model,),
        ),
    ]
