# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from collections import OrderedDict
import json
from sqlalchemy.dialects.mysql import LONGBLOB
import sqlalchemy.types
import sys

__all__ = [b"MySqlPickleType",
           b"create_pickler", b"JsonOrderedDictPickler"]


class MySqlPickleType(sqlalchemy.types.PickleType):
    impl = LONGBLOB if not sys.argv[0].endswith("nosetests") else sqlalchemy.types.LargeBinary


def create_pickler(dumps, loads):
    class Pickler(object):
        @classmethod
        def dumps(cls, obj, protocol):
            return dumps(obj)

        @classmethod
        def loads(cls, string):
            return loads(string)

    return Pickler


JsonOrderedDictPickler = create_pickler(json.dumps, lambda string: json.loads(string, object_pairs_hook=OrderedDict))
