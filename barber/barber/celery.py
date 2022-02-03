from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from django.utils.translation import gettext

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barber.settings')
app = Celery('barber')

#1
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))