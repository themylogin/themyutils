# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from themyutils.string import underscore_to_camelcase


def Observable(observer_name, observer_methods):
    class ObservableMixin(object):
        pass

    def verify(observer):
        for method in observer_methods:
            if not hasattr(observer, "on_%s" % method):
                raise AttributeError("%s %r does not have on_%s method" % (observer_name, observer, method))

        return observer

    observers_storage = "%ss" % observer_name
    d = {"notify_%s" % method: (lambda method: (lambda self, *args, **kwargs:
                                                    [getattr(observer, "on_%s" % method)(*args, **kwargs)
                                                     for observer in getattr(self, observers_storage, [])]))(method)
         for method in observer_methods}
    d["add_%s" % observer_name] = lambda self, observer: (getattr(self, observers_storage).append(verify(observer))
                                                          if hasattr(self, observers_storage)
                                                          else setattr(self, observers_storage, [verify(observer)]))

    return type(b"ObservableMixin_%s" % str(underscore_to_camelcase(observer_name, lower_first=False)),
                (ObservableMixin,), d)
