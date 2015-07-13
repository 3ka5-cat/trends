# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from django.utils.translation import pgettext_lazy
from .models import Term


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'hits', )
    search_fields = ('name', )
    list_filter = ('language', )
    filter_horizontal = ('vacancies', )

    def queryset(self, request):
        qs = super(TermAdmin, self).queryset(request)
        qs = qs.annotate(hits=models.Count('vacancies'))
        return qs

    def hits(self, obj):
        return obj.hits

    hits.admin_order_field = 'hits'
    hits.short_description = pgettext_lazy('Term admin column name', 'Hits')