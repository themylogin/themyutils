# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import argparse
import logging


def LoggingLevelType(val):
    LEVELS = ("debug", "info", "warning", "error", "critical")

    val = val.lower()
    if val in LEVELS:
        return getattr(logging, val.upper())
    else:
        msg = "%r is not allowed logging level. Logging levels are: %r" % (val, ", ".join(LEVELS))
        raise argparse.ArgumentTypeError(msg)
