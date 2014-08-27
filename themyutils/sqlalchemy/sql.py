# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from datetime import datetime, date
import json
from sqlalchemy.orm.query import Query

__all__ = [b"literal_query"]


def literal_query(statement, bind=None):
    """
    Generate an SQL expression string with bound parameters rendered inline
    for the given SQLAlchemy statement.

    WARNING: This method of escaping is insecure, incomplete, and for debugging
    purposes only. Executing SQL statements with inline-rendered user values is
    extremely insecure.

    Based on http://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
    """
    if isinstance(statement, Query):
        if bind is None:
            bind = statement.session.get_bind(statement._mapper_zero_or_none())
        statement = statement.statement
    elif bind is None:
        bind = statement.bind

    class LiteralCompiler(bind.dialect.statement_compiler):
        def visit_bindparam(self, bindparam, within_columns_clause=False,
                            literal_binds=False, **kwargs):
            return self.render_literal_value(bindparam.value, bindparam.type)

        def render_literal_value(self, value, type_):
            if isinstance(value, bool):
                return str(int(value))
            elif isinstance(value, long):
                return str(value)
            elif isinstance(value, (date, datetime)):
                return "'%s'" % value
            elif isinstance(value, (list, dict)):
                return "'%s'" % json.dumps(value)
            return super(LiteralCompiler, self).render_literal_value(value, type_)

    return LiteralCompiler(bind.dialect, statement).process(statement)
