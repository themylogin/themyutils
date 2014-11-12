# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

bytes_suffixes = ["B", "KB", "MB", "GB", "TB"]


def human_bytes(size, precision=2):
    suffix_index = 0
    while size > 1024 and suffix_index < len(bytes_suffixes) - 1:
        suffix_index += 1
        size = size / 1024.0
    return "%.*f %s" % (precision if suffix_index > 1 else 0, size, bytes_suffixes[suffix_index])


def machine_bytes(size):
    value, suffix = size.split(" ")
    return int(float(value) * 1024 ** bytes_suffixes.index(suffix))
