from celery import Celery

from config import settings, get_apps


celery_app = Celery('tasks', broker=settings.celery_broker_url, backend=settings.celery_broker_url)

for i in get_apps():
    i.init_tasks()


celery_app.on_after_finalize.connect(celery_app.autodiscover_tasks())
# __all__ = ('celery_app', )
