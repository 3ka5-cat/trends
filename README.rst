This project builds trends on skills required from software developers.
It is implemented as Django application, based on boilerplate from Tangent Labs 
(https://github.com/tangentlabs/tangent-django-boilerplate).

This application makes search request with specified query to site with vacancies (like hh.ru), 
collects found vacancies with description and specified key skills, 
and trying to extract terms, which looks like name of tools used in development or knowledge areas in CS, 
from collected information.
Results of such analytics are available at admin site.

It uses PostgreSQL as RDBMS, 
Celery for launching collect tasks, 
Sentry for catching errors, 
topia and rutermextract for term extraction.
It is hosted on Heroku PAAS.
