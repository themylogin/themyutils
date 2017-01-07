# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from celery.schedules import crontab, schedule

__all__ = [b"Cron"]


class Cron(object):
    def __init__(self, celery):
        self.celery = celery

        self.jobs = {}

    def job(self, *args, **kwargs):
        def decorator(func):
            celery_task = self.celery.task(func)

            self.celery.conf.CELERYBEAT_SCHEDULE[celery_task.name] = {
                "task":     celery_task.name,
                "schedule": schedule(*args) if args else crontab(**kwargs),
            }

            self.jobs[celery_task.name] = func

            return celery_task

        return decorator
