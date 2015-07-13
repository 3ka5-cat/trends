# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from django.utils.translation import pgettext_lazy
from .models import Skill, Vacancy


class VacanciesInline(admin.TabularInline):
    model = Vacancy.skills.through
    extra = 0


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'hits', )
    search_fields = ('name', )
    inlines = (VacanciesInline, )

    def queryset(self, request):
        qs = super(SkillAdmin, self).queryset(request)
        qs = qs.annotate(hits=models.Count('vacancy'))
        return qs

    def hits(self, obj):
        return obj.hits

    hits.admin_order_field = 'hits'
    hits.short_description = pgettext_lazy('Skill admin column name', 'Hits')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('source', 'external_id', )
    list_filter = ('source', )
    search_fields = ('external_id', )
    filter_horizontal = ('skills', )