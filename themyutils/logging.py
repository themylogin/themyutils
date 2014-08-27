# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import logging 
import os


def simple_logging(__file__, suffix=None, level=logging.DEBUG,
                   format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%b %d %H:%M:%S"):
    filename = os.path.join(os.path.dirname(__file__),
                            os.path.splitext(os.path.basename(__file__))[0] + (".%s" % suffix if suffix else "") + ".log")
    logging.basicConfig(filename=filename, level=level, format=format, datefmt=datefmt)
