# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from celery import Celery
from flask import has_request_context

__all__ = [b"make_celery"]


def make_celery(app, db=None):
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            if has_request_context():
                return super(ContextTask, self).__call__(*args, **kwargs)
            else:
                with app.app_context():
                    try:
                        return super(ContextTask, self).__call__(*args, **kwargs)

        def after_return(self, status, retval, task_id, args, kwargs, einfo):
            if has_request_context():
                pass
            else:
                if db:
                    db.session.remove()

    celery.Task = ContextTask
    return celery
