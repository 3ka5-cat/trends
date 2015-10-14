# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from topia.termextract.extract import DefaultFilter
from .models import Term


class BlackListFilter(DefaultFilter):

    def __call__(self, word, occur, strength):
        if super(BlackListFilter, self).__call__(word, occur, strength):
            return not Term.objects.blacklisted().filter(name=word).exists()
        return False