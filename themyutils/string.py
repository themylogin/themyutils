# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import itertools

__all__ = [b"common_prefix", b"common_suffix"]


def common_prefix(strings):
    return "".join(c[0] for c in itertools.takewhile(lambda x: all(x[0] == y for y in x), itertools.izip(*strings)))


def common_suffix(strings):
    return "".join(reversed(common_prefix(map(reversed, strings))))
