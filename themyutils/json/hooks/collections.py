# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from themyutils.json.hooks.base import EncodeHook


class NamedTupleHook(EncodeHook):
    hook_for = tuple

    def can_encode(self, o):
        return super(NamedTupleHook, self).can_encode(o) and hasattr(o, "_asdict")

    def encode(self, o):
        return o._asdict()
