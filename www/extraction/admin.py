# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from django.utils.translation import pgettext_lazy
from core.models import Skill, Vacancy
from .models import Term


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'hits', 'blacklisted', )
    search_fields = ('name', )
    list_filter = ('language', 'blacklisted', )
    filter_horizontal = ('vacancies', )
    actions = ('make_skill', 'make_blacklisted', 'mark_as_russian', 'mark_as_english', )

    def queryset(self, request):
        qs = super(TermAdmin, self).queryset(request)
        qs = qs.annotate(hits=models.Count('vacancies'))
        return qs

    def hits(self, obj):
        return obj.hits
    hits.admin_order_field = 'hits'
    hits.short_description = pgettext_lazy('Term admin column name', 'Hits')

    def make_blacklisted(self, request, queryset):
        # without such explicit re-selection,
        # updating of annotated queryset raises an exception about too big subquery
        Term.objects.filter(id__in=queryset.values_list('id', flat=True)).update(blacklisted=True)
    make_blacklisted.short_description = pgettext_lazy('Term admin action name',
                                                       'Mark selected terms as blacklisted')

    def mark_as_russian(self, request, queryset):
        # without such explicit re-selection,
        # updating of annotated queryset raises an exception about too big subquery
        Term.objects.filter(id__in=queryset.values_list('id', flat=True)).update(language='ru')
    mark_as_russian.short_description = pgettext_lazy('Term admin action name',
                                                      'Mark selected terms as russian terms')

    def mark_as_english(self, request, queryset):
        # without such explicit re-selection,
        # updating of annotated queryset raises an exception about too big subquery
        Term.objects.filter(id__in=queryset.values_list('id', flat=True)).update(language='en')
    mark_as_english.short_description = pgettext_lazy('Term admin action name',
                                                      'Mark selected terms as english terms')

    def make_skill(self, request, queryset):
        for term in queryset.iterator():
            vacancies = Vacancy.objects.filter(id__in=term.vacancies.all().values_list('id', flat=True))
            Skill.objects.create_or_update_with_vacancies(name=term.name, vacancies_qs=vacancies)
            term.delete()
    make_skill.short_description = pgettext_lazy('Term admin action name',
                                                 'Turn selected terms into skills')