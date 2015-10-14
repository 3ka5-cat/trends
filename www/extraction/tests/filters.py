# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.html import strip_tags
import pytest
import pprint
from extraction.extractors import RussianTermExtractor, EnglishTermExtractor
from extraction.filters import BlackListFilter
from extraction.models import Term


class UTFDecodePrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return object.encode('utf-8'), True, False
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


@pytest.fixture
def ru_vacancy():
    return {
        'id': '14702977',
        'name': 'Старший разработчик Python (Backend)',
        'description': '<p>Мы - небольшая, узкоспециализированная компания '
                       'по разработке сложного программного обеспечения для '
                       'зарубежных заказчиков.</p> '
                       '<p> </p> <p><strong> Требуются:</strong></p> '
                       '<ul> <li>Глубокие знания Python</li> '
                       '<li>Уверенное знание Flask, Django и других фреймворков</li> '
                       '<li>Понимание принципов ООП, паттернов проектирования и рефакторинга</li> '
                       '<li>Опыт работы с базами данных MySQL, MongoDB, etc и ORM SQLAlchemy, etc.</li> '
                       '<li>Приветствуется знание JavaScript, AngularJS</li> '
                       '<li>Дополнительным плюсом будут знания алгоритмов и структур данных</li> '
                       '</ul> <p> </p> <p><strong>Задачи:</strong></p> <ul> '
                       '<li>Разработка backend систем с использованием Flask, NumPy, Django, Celery</li> '
                       '<li>Разработка проектов, связанных с данными: поиск, обработка, аналитика, алгоритмы</li> '
                       '</ul> <p> </p> <p><strong>Условия</strong>:</p> <ul> '
                       '<li>Работа удаленная</li> '
                       '<li>Готовы обсудить варианты с частичной занятостью</li> '
                       '<li>Почасовая ставка от 600 рублей в час</li> '
                       '<li>Очень сильная команда разработки с опытом работы в Яндекс</li> '
                       '<li>Дружеская позитивная атмосфера :)</li> </ul>',
        'key_skills': [
            {'name': 'Python'},
            {'name': 'MongoDB'},
            {'name': 'Django Framework'},
            {'name': 'Flask'},
        ]
    }


@pytest.fixture
def en_vacancy():
    return {
        'id': '14785485',
        'name': 'FICON Driver Developer (Linux kernel drivers and C)',
        'description': '<p><strong>FICON Driver Developer (Linux kernel drivers and C)</strong></p> '
                       '<p><strong>EMC Overview</strong></p> '
                       '<p> </p> '
                       '<p>Today, information technology is being transformed by four '
                       'powerful trends—mobile, cloud computing, Big Data and social networking. '
                       'Our strategy is to lead our customers on their journey to transform both '
                       'their IT and business to stay ahead of these market trends.</p> '
                       '<p>We pursue this strategy through our unique EMC Federation that '
                       'includes EMC Information Infrastructure (EMCii), VMware, Pivotal and RSA.</p>'
                       ' <p>EMC Corporation is the world leader in information management solutions'
                       ' that store, protect, move, manage and access the explosion of content. '
                       'We help people and businesses around the world unleash the power of '
                       'their digital information.</p> <p>If you are passionate about technology '
                       'and want to be part of the information management revolution, join more '
                       'than 60,000+ EMCers around the world.</p> <p><strong>Job Description</strong></p> '
                       '<p>We are looking for an engineer to join our team responsible for developing'
                       ' and maintaining Linux drivers that support the FICON interface. '
                       'FICON is a protocol that runs on top of Fibre Channel and is the interface '
                       'used to connect the Disk Library for Mainframe (DLM) to the mainframe. '
                       'DLm brings together technology from our Data Domain, VNX, Symmetrix and '
                       'Mainframe development groups, to create a Mainframe Virtual Tape appliance.</p> '
                       '<p>You will be a contributing development engineer, and participate in '
                       'product design, review, system integration, and validation. You will work in '
                       'the Linux kernel and user space environments on a variety of high performance drivers and '
                       'applications.</p> <p> </p> '
                       '<p><strong>Required Skills &amp; Experience</strong></p> '
                       '<ul> <li>Expert skills in C programing</li> '
                       '<li>Experience writing and debugging Linux kernel drivers for a '
                       'multi processor environment</li> <li>Excellent knowledge of the Linux kernel</li> '
                       '<li>Knowledge of the FICON and Fibre Channel protocols</li> <li>Ability to communicate '
                       'well through both written and spoken English</li>'
                       ' <li>Experience with products through the entire product development cycle '
                       '(specification &amp; design, implementation, documentation, bug tracking system, '
                       'code version control)</li> <li>Ability to work in teams that have a wide range '
                       'of development skill</li> <li>Self-motivated in his/her work</li> </ul> '
                       '<p><strong>Other Desired Skills &amp; Experience</strong></p> '
                       '<ul> <li>Skilled in various scripting and development languages '
                       'including Bash/Python/Perl.</li> <li>IBM channel knowledge</li> '
                       '<li>PowerPC embedded processor development experience</li>'
                       ' <li>Working knowledge of Storage Area Networks</li>'
                       ' <li>Working knowledge of IP networks, including experience with both'
                       ' WAN and LAN technologies</li> <li>Experience with any storage subsystems</li> '
                       '<li>Fluent English</li> </ul> <p><strong>Joining us, you will get:</strong></p> '
                       '<ul> <li>Salary to be discussed on the results of the interview, but not lower '
                       'than the markets average</li> '
                       '<li>Medical, Life insurance for employees and your family in Russia and '
                       'abroad</li> <li>Opportunity to train in different sport teams: volleyball,'
                       ' football, kicker, chess, cycling, etc</li> <li>Opportunity to participate in '
                       'sports competitions among IT Community</li> <li>Corporate trainings and '
                       'certifications; Corporate English Classes</li> '
                       '<li>Possibility in Flexible working hours and Working from home</li> '
                       '<li>33 days of paid vacation days plus 5 paid days off</li> <li>Paid sick days;'
                       ' Doctor’s consultation at the office</li> <li>Opportunity to participate in '
                       'charity activities</li> <li>Comfortable 24/7 office in the City Centre</li> '
                       '<li>Partial reimbursement of any sport activities</li> <li>Regular teambuilding '
                       'and corporate events</li> <li>Corporate cell phone service and laptop</li> '
                       '<li>EMC Corporation stocks options available</li> </ul>',
        'key_skills': [
            {'name': 'FICON'},
            {'name': 'Kernel'},
            {'name': 'Linux'},
            {'name': 'Linux drivers'}
        ],
    }


@pytest.fixture
def blacklisted_ru_term():
    blacklisted_term_name = 'ПАРАБЕЛЛУМ'
    normalized_term_name = blacklisted_term_name.lower()
    Term.objects.create(name=normalized_term_name, language='ru', blacklisted=True)
    return {'name': blacklisted_term_name, 'normalized_name': normalized_term_name}


@pytest.fixture
def blacklisted_en_term():
    blacklisted_term_name = normalized_term_name = 'BLACKLISTED'
    Term.objects.create(name=blacklisted_term_name, language='en', blacklisted=True)
    return {'name': blacklisted_term_name, 'normalized_name': normalized_term_name}


@pytest.mark.django_db
def test_ru_blacklist_filter(ru_vacancy, blacklisted_ru_term):
    pp = UTFDecodePrinter(indent=4)
    extractor = RussianTermExtractor()

    ru_vacancy['description'] = strip_tags(ru_vacancy['description'])
    # because default filter ignores words which were occur less than 3 times
    ru_vacancy['description'] += ', '.join([blacklisted_ru_term['normalized_name']]*3)
    extracted_terms = map(lambda term: term.normalized, extractor(ru_vacancy['description']))
    extracted_blacklisted_terms = Term.objects.blacklisted().filter(name__in=extracted_terms)
    print 'Extracted without filter: '
    pp.pprint(extracted_terms)
    assert blacklisted_ru_term['normalized_name'] in extracted_terms
    assert extracted_blacklisted_terms.count() > 0

    extractor.filter = BlackListFilter()
    extracted_terms = map(lambda term: term.normalized, extractor(ru_vacancy['description']))
    extracted_blacklisted_terms = Term.objects.blacklisted().filter(name__in=extracted_terms)
    print 'Extracted with filter: '
    pp.pprint(extracted_terms)
    assert blacklisted_ru_term['normalized_name'] not in extracted_terms
    assert extracted_blacklisted_terms.count() == 0


@pytest.mark.django_db
def test_en_blacklist_filter(en_vacancy, blacklisted_en_term):
    pp = UTFDecodePrinter(indent=4)
    extractor = EnglishTermExtractor()

    en_vacancy['description'] = strip_tags(en_vacancy['description'])
    # because default filter ignores words which were occur less than 3 times
    en_vacancy['description'] += ', '.join([blacklisted_en_term['name']]*3)
    extracted_terms = map(lambda term: term[0], extractor(en_vacancy['description']))
    extracted_blacklisted_terms = Term.objects.blacklisted().filter(name__in=extracted_terms)
    print 'Extracted without filter: '
    pp.pprint(extracted_terms)
    assert blacklisted_en_term['name'] in extracted_terms
    assert extracted_blacklisted_terms.count() > 0

    extractor.filter = BlackListFilter()
    extracted_terms = map(lambda term: term[0], extractor(en_vacancy['description']))
    extracted_blacklisted_terms = Term.objects.blacklisted().filter(name__in=extracted_terms)
    print 'Extracted with filter: '
    pp.pprint(extracted_terms)
    assert blacklisted_en_term['name'] not in extracted_terms
    assert extracted_blacklisted_terms.count() == 0