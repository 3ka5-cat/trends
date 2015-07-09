# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'hits', )
    search_fields = ('name', )