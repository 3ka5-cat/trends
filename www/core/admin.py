# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from .models import Skill, Vacancy


class VacanciesInline(admin.TabularInline):
    model = Vacancy.skills.through
    extra = 0


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'hits', )
    search_fields = ('name', )
    inlines = (VacanciesInline, )


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('source', 'external_id', )
    list_filter = ('source', )
    search_fields = ('external_id', )
    filter_horizontal = ('skills',)