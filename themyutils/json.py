# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import datetime
import isodate
import isodate.isoduration
import isodate.isoerror
import re
import json


class Hook(object):
    pass


class DateTimeHook(Hook):
    hook_for = datetime.datetime
    class_name = "datetime"

    @staticmethod
    def encode(o):
        return o.isoformat()

    @staticmethod
    def decode(s):
        return isodate.parse_datetime(s)


class TimeDeltaHook(Hook):
    hook_for = datetime.timedelta
    class_name = "timedelta"

    @staticmethod
    def encode(o):
        return isodate.isoduration.duration_isoformat(o)

    @staticmethod
    def decode(s):
        return isodate.isoduration.parse_duration(s)

hooks = [DateTimeHook, TimeDeltaHook]


class JSONDecoder(json.JSONDecoder):
    def decode(self, s):
        o = super(JSONDecoder, self).decode(s)
        o = self.traverse(o)
        return o

    def traverse(self, o):
        if isinstance(o, dict):
            return dict(map(lambda (k, v): (self.traverse(k), self.traverse(v)), o.iteritems()))

        if isinstance(o, list):
            return map(self.traverse, o)

        if isinstance(o, unicode):
            return self.unicode_hook(o)

        return o

    @staticmethod
    def unicode_hook(s):
        m = re.match("(?P<class_name>%s)\((?P<s>.*)\)$" % "|".join([re.escape(hook.class_name) for hook in hooks]), s)
        if m:
            for hook in hooks:
                if hook.class_name == m.group("class_name"):
                    try:
                        return hook.decode(m.group("s"))
                    except ValueError:
                        pass

        return s


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        for hook in hooks:
            if isinstance(o, hook.hook_for):
                return '%s(%s)' % (hook.class_name, hook.encode(o))

        try:
            return super(JSONEncoder, self).default(o)
        except TypeError:
            return repr(o)


def dumps(o):
    return JSONEncoder().encode(o)


def loads(s):
    return JSONDecoder().decode(s)
