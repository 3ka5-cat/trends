# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from rutermextract import TermExtractor
from topia.termextract.extract import TermExtractor as EnglishTermExtractor, DefaultFilter


class RussianTermExtractor(TermExtractor):
    def __init__(self, tokenizer=None, parser=None, labeler=None,
                 extractor=None, normalizer=None, ranker=None,
                 filter=None):
        super(RussianTermExtractor, self).__init__(tokenizer, parser, labeler, extractor, normalizer, ranker)
        if filter is None:
            filter = DefaultFilter()
        self.filter = filter

    def __call__(self, text, limit=None, weight=None, strings=False, nested=False):
        terms = super(RussianTermExtractor, self).__call__(text, limit, weight, strings, nested)
        return [term for term in terms if self.filter(term.normalized, term.count, term.word_count)]