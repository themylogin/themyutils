# -*- coding=utf-8 -*-
from __future__ import absolute_import, unicode_literals

from pprint import PrettyPrinter
import sys


class UnicodePrettyPrinter(PrettyPrinter):
    def format(self, *args, **kwargs):
        repr, readable, recursive = PrettyPrinter.format(self, *args, **kwargs)
        if repr:
            if repr[0] in ('"', "'"):
                repr = repr.decode('string_escape')
            elif repr[0:2] in ("u'", 'u"'):
                repr = repr.decode('unicode_escape').encode(sys.stdout.encoding)
        return repr, readable, recursive


def pprint(obj, stream=None, indent=1, width=80, depth=None):
    printer = UnicodePrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
    printer.pprint(obj)
