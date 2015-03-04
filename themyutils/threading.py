# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import ctypes
import inspect
import threading

__all__ = [b"TerminateableThread", b"start_daemon_thread"]


def _async_raise(tid, exctype):
    # Raises the exception, performs cleanup if needed
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("Invalid thread id")
    elif res != 1:
        # If it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class TerminateableThread(threading.Thread):
    def _get_my_tid(self):
        # Determines this (self's) thread id
        if not self.isAlive():
            raise threading.ThreadError("Thread is not active")

        # Do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # No, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        raise AssertionError("Could not determine thread's id")

    def raise_exc(self, exctype):
        # Raises the given exception type in the context of this thread"""
        _async_raise(self._get_my_tid(), exctype)

    def terminate(self):
        # Raises SystemExit in the context of the given thread, which should
        # cause the thread to exit silently (unless caught)
        self.raise_exc(SystemExit)


def start_daemon_thread(target, *args, **kwargs):
    thread = threading.Thread(target=target, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread
