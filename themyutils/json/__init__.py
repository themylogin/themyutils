# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re
import json

from themyutils.json.hooks import hooks
from themyutils.json.hooks.base import EncodeHook, EncodeDecodeHook


class JSONDecoder(json.JSONDecoder):
    def decode(self, *args, **kwargs):
        o = super(JSONDecoder, self).decode(*args, **kwargs)
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
        m = re.match("(?P<class_name>%s)\((?P<s>.*)\)$" % "|".join([re.escape(hook.class_name)
                                                                    for hook in hooks
                                                                    if isinstance(hook, EncodeDecodeHook)]), s)
        if m:
            for hook in hooks:
                if isinstance(hook, EncodeDecodeHook):
                    if hook.class_name == m.group("class_name"):
                        try:
                            return hook.decode(m.group("s"))
                        except ValueError:
                            pass

        return s


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        for hook in hooks:
            if isinstance(hook, EncodeHook):
                print o
                if hook.can_encode(o):
                    if isinstance(hook, EncodeDecodeHook):
                        return "%s(%s)" % (hook.class_name, hook.encode(o))
                    else:
                        return hook.encode(o)

        try:
            return super(JSONEncoder, self).default(o)
        except TypeError:
            return repr(o)


def dumps(o, *args, **kwargs):
    return JSONEncoder(*args, **kwargs).encode(o)


def loads(s, *args, **kwargs):
    return JSONDecoder(*args, **kwargs).decode(s)
