# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import datetime
import isodate
import isodate.isoduration
import isodate.isoerror

from themyutils.json.hooks.base import EncodeDecodeHook


class DateTimeHook(EncodeDecodeHook):
    hook_for = datetime.datetime
    class_name = "datetime"

    def encode(self, o):
        return o.isoformat()

    def decode(self, s):
        return isodate.parse_datetime(s)


class TimeDeltaHook(EncodeDecodeHook):
    hook_for = datetime.timedelta
    class_name = "timedelta"

    def encode(self, o):
        return isodate.isoduration.duration_isoformat(o)

    def decode(self, s):
        return isodate.isoduration.parse_duration(s)
