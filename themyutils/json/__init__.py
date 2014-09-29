# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re
import simplejson

from themyutils.json.hooks import hooks


class JSONDecoder(simplejson.JSONDecoder):
    def decode(self, *args, **kwargs):
        o = super(JSONDecoder, self).decode(*args, **kwargs)
        o = self.traverse(o)
        return o

    def traverse(self, o):
        if isinstance(o, dict):
            return dict(map(lambda (k, v): (self.traverse(k), self.traverse(v)), o.iteritems()))

        if isinstance(o, list):
            return map(self.traverse, o)

        if isinstance(o, basestring):
            return self.basestring_hook(o)

        return o

    @staticmethod
    def basestring_hook(s):
        m = re.match("(?P<class_name>%s)\((?P<s>.*)\)$" % "|".join([re.escape(hook.class_name) for hook in hooks]), s)
        if m:
            for hook in hooks:
                if hook.class_name == m.group("class_name"):
                    try:
                        return hook.decode(m.group("s"))
                    except ValueError:
                        pass

        return s


class JSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)

        for hook in hooks:
            if isinstance(o, hook.hook_for):
                return '%s(%s)' % (hook.class_name, hook.encode(o))

        try:
            return super(JSONEncoder, self).default(o)
        except TypeError:
            return repr(o)


def dumps(o, *args, **kwargs):
    return JSONEncoder(*args, **kwargs).encode(o)


def loads(s, *args, **kwargs):
    return JSONDecoder(*args, **kwargs).decode(s)
