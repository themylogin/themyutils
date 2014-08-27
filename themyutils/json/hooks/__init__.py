# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from themyutils.json.hooks.collections import NamedTupleHook
from themyutils.json.hooks.datetime import DateTimeHook, TimeDeltaHook

hooks = [NamedTupleHook(), DateTimeHook(), TimeDeltaHook()]
