import os

from django.apps import AppConfig


class DayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'day'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            from .jobs import JobManager

            manager = JobManager()
            manager.ready()
