# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import datetime
import isodate
import isodate.isoduration
import isodate.isoerror


class DateTimeHook(object):
    hook_for = datetime.datetime
    class_name = "datetime"

    @staticmethod
    def encode(o):
        return o.isoformat()

    @staticmethod
    def decode(s):
        return isodate.parse_datetime(s)


class TimeDeltaHook(object):
    hook_for = datetime.timedelta
    class_name = "timedelta"

    @staticmethod
    def encode(o):
        return isodate.isoduration.duration_isoformat(o)

    @staticmethod
    def decode(s):
        return isodate.isoduration.parse_duration(s)
