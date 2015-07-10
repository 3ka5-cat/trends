# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('hits', models.IntegerField(default=0, verbose_name='Hits')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=255, verbose_name='Source')),
                ('external_id', models.CharField(max_length=255, verbose_name='ID in source system')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('skills', models.ManyToManyField(to='core.Skill', null=True, verbose_name='Skills', blank=True)),
            ],
            options={
                'verbose_name': 'Vacancy',
                'verbose_name_plural': 'Vacancies',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vacancy',
            unique_together=set([('source', 'external_id')]),
        ),
    ]
