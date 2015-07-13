# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('language', models.CharField(max_length=2, verbose_name='Language code (ISO 639-1)')),
                ('vacancies', models.ManyToManyField(to='core.Vacancy', null=True, verbose_name='Vacancies', blank=True)),
            ],
            options={
                'verbose_name': 'Term',
                'verbose_name_plural': 'Terms',
            },
            bases=(models.Model,),
        ),
    ]
