web: gunicorn app.wsgi --log-file -
worker: celery -A chatbot.tasks.celery worker --loglevel=info
