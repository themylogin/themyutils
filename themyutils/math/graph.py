# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals


class CyclicDependenciesException(Exception):
    pass


def toposort(dependencies):
    extra_items_in_deps = reduce(set.union, dependencies.itervalues()) - set(dependencies.iterkeys())
    dependencies.update({item: set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in dependencies.iteritems() if not dep)
        if not ordered:
            break
        yield ordered
        dependencies = {item: (dep - ordered) for item, dep in dependencies.iteritems() if item not in ordered}
    if dependencies:
        raise CyclicDependenciesException(dependencies)
