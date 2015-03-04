# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import itertools
import re

__all__ = [b"common_prefix", b"common_suffix", b"underscore_to_camelcase"]


def common_prefix(strings):
    return "".join(c[0] for c in itertools.takewhile(lambda x: all(x[0] == y for y in x), itertools.izip(*strings)))


def common_suffix(strings):
    return "".join(reversed(common_prefix(map(reversed, strings))))


def underscore_to_camelcase(s, lower_first=True):
    s = re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)

    if not lower_first:
        if len(s):
            s = s[0].upper() + s[1:]

    return s
