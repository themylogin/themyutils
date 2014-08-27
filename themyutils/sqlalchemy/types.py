# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from sqlalchemy.dialects.mysql import LONGBLOB
import sqlalchemy.types

__all__ = [b"MySqlPickleType"]


class MySqlPickleType(sqlalchemy.types.PickleType):
    impl = LONGBLOB
