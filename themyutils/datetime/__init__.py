# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import pytz.reference

__all__ = [b"russian_strftime", b"utc_to_local"]


def russian_month(date_string):
    return date_string.replace("January",      u"января").\
                       replace("February",     u"февраля").\
                       replace("March",        u"марта").\
                       replace("April",        u"апреля").\
                       replace("May",          u"мая").\
                       replace("June",         u"июня").\
                       replace("July",         u"июля").\
                       replace("August",       u"августа").\
                       replace("September",    u"сентября").\
                       replace("October",      u"октября").\
                       replace("November",     u"ноября").\
                       replace("December",     u"декабря")


def russian_strftime(datetime_object, format):
    return russian_month(datetime_object.strftime(format))


def utc_to_local(datetime_object):
    return datetime_object + pytz.reference.LocalTimezone().utcoffset(datetime_object)
