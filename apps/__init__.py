from config import config

for i in config.get_apps():
    i.init_tasks()

celery_app = config.celery

celery_app.on_after_finalize.connect(celery_app.autodiscover_tasks())
__all__ = ('celery_app', )
