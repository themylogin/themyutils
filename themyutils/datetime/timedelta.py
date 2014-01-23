# -*- coding=utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
import pytils


def timedelta_in_words(td, accuracy=1):
    if not isinstance(td, timedelta):
        td = timedelta(seconds=td)

    now = datetime.now()
    return pytils.dt.distance_of_time_in_words(now + td, accuracy, now).\
        replace("менее чем через минуту", "менее минуты").\
        replace("через ", "").\
        replace("послезавтра", u"2 дня").\
        replace("завтра", u"1 день")
