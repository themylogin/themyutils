# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals


def entity_to_dict(entity):
    return {column.name: getattr(entity, column.name) for column in entity.__table__.columns}
