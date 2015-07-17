# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extraction', '0002_term_blacklisted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='vacancies',
            field=models.ManyToManyField(related_name='terms', null=True, verbose_name='Vacancies', to='core.Vacancy', blank=True),
            preserve_default=True,
        ),
    ]
