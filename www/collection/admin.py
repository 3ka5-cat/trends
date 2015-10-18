# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from djcelery.models import TaskMeta


@admin.register(TaskMeta)
class TaskMetaAdmin(admin.ModelAdmin):
    list_display = ('source', 'date_done', 'status', 'vacancies', )
    search_fields = ('source', )
    list_filter = ('status', )
    readonly_fields = ('source', 'status', 'date_done', 'result', 'task_id', 'traceback', )

    def source(self, obj):
        return obj.result['source']

    def vacancies(self, obj):
        return obj.result['vacancies_created']