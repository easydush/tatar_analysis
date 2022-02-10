import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tatar_analysis.settings')
app = Celery('get_news', broker=settings.CELERY_BROKER_URL)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    # update vk news
    'add-update-vk-news': {
        'task': 'core.tasks.update_vk_content',
        # every 5 min
        # todo: update time
        'schedule': crontab(minute='*/2'),
    },
    # task to check news for trigger words
    'add-update-kpfu-content': {
        'task': 'core.tasks.update_kpfu_content',
        # every minute
        # todo: update time
        'schedule': crontab(minute='*/2'),
    },

}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
