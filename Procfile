# use honcho for running worker and web on single dyno
# web: honcho -f www/ProcfileHoncho start
web: gunicorn deploy.wsgi.dev --log-file -