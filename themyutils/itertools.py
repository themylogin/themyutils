# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals


def unique_items(iterable, key=lambda x: x):
    items = []
    for item in iterable:
        if key(item) not in items:
            items.append(item)
    return items


def with_prev(iterable, prev_for_first=None):
    prev_v = prev_for_first
    for v in iterable:
        yield v, prev_v
        prev_v = v
