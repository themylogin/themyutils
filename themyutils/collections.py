# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import collections


class KeyTransformDict(collections.Mapping):
    def __init__(self, transform):
        self.transform = transform
        self._d = {}
        self._s = {}

    def __contains__(self, k):
        return self.transform(k) in self._s

    def __len__(self):
        return len(self._s)

    def __iter__(self):
        return iter(self._s)

    def __getitem__(self, k):
        return self._d[self._s[self.transform(k)]]

    def __setitem__(self, k, v):
        self._d[k] = v
        self._s[self.transform(k)] = k

    def pop(self, k):
        k0 = self._s.pop(self.transform(k))
        return self._d.pop(k0)

    def actual_key(self, k):
        return self._s.get(self.transform(k))


class OrderedDefaultDict(collections.OrderedDict):
    def __init__(self, *args, **kwargs):
        if not args:
            self.default_factory = None
        else:
            if not (args[0] is None or callable(args[0])):
                raise TypeError("First argument must be callable or None")
            self.default_factory = args[0]
            args = args[1:]
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)

    def __missing__ (self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = default = self.default_factory()
        return default

    def __reduce__(self):
        args = (self.default_factory,) if self.default_factory else ()
        return self.__class__, args, None, None, self.iteritems()
