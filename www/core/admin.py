# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from django.utils.translation import pgettext_lazy
from .models import Skill, Vacancy, SearchQuery


class SkillsInline(admin.TabularInline):
    model = Skill.vacancies.through
    extra = 0


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'hits', )
    search_fields = ('name', )
    filter_horizontal = ('vacancies', )

    def queryset(self, request):
        qs = super(SkillAdmin, self).queryset(request)
        qs = qs.annotate(hits=models.Count('vacancies'))
        return qs

    def hits(self, obj):
        return obj.hits

    hits.admin_order_field = 'hits'
    hits.short_description = pgettext_lazy('Skill admin column name', 'Hits')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'external_id', )
    list_filter = ('source', )
    search_fields = ('name', 'external_id', )
    inlines = (SkillsInline, )


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('text', )
    search_fields = ('text', 'note', )