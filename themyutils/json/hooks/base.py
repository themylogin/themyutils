# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals


class BaseHook(object):
    pass


class EncodeHook(BaseHook):
    hook_for = object

    def can_encode(self, o):
        return isinstance(o, self.hook_for)

    def encode(self, o):
        raise NotImplementedError


class EncodeDecodeHook(EncodeHook):
    class_name = "object"

    def decode(self, s):
        raise NotImplementedError
