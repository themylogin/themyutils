# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from celery.schedules import crontab


__all__ = [b"cron_jobs", b"cron_job"]

cron_jobs = {}


def cron_job(celery, *crontab_args, **crontab_kwargs):
    def decorator(func):
        celery_task = celery.task(func)

        celery.conf.CELERYBEAT_SCHEDULE[celery_task.name] = {
            "task":     celery_task.name,
            "schedule": crontab(*crontab_args, **crontab_kwargs),
        }

        cron_jobs[celery_task.name] = func

    return decorator
