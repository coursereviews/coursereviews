web: newrelic-admin run-program gunicorn -c gunicorn.py.ini wsgi
scheduler: python manage.py celery worker -B -E --maxtasksperchild=1000
worker: python manage.py celery worker -E --maxtasksperchild=1000 --loglevel=debug