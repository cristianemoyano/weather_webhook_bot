from celery import Celery


def make_celery(app):
    celery = Celery(
        app.name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.conf.update(
        # Will decrease connection usage
        broker_pool_limit=1,
        # We're using TCP keep-alive instead
        broker_heartbeat=None,
        # May require a long timeout due to Linux DNS timeouts etc
        broker_connection_timeout=30,
        # Will delete all celeryev. queues without consumers after 1 minute.
        event_queue_expires=60,
        # Disable prefetching, it's causes problems and doesn't help performance
        worker_prefetch_multiplier=1,
        # If you tasks are CPU bound, then limit to the number of cores, otherwise increase substainally
        worker_concurrency=50
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
