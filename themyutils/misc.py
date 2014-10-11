# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import logging
import math
import time

logger = logging.getLogger(__name__)

__all__ = [b"retry"]


def retry(operation, max_tries=100, max_sleep=50, exceptions=(Exception,), logger=logger):
    exceptions_classes = tuple(exception[0] if isinstance(exception, tuple) else exception
                               for exception in exceptions)
    tries = 0
    while True:
        try:
            return operation()
        except exceptions_classes as e:
            for exception_class, is_expected_exception in filter(lambda x: isinstance(x, tuple), exceptions):
                if isinstance(e, exception_class) and not is_expected_exception(e):
                    raise

            logger.exception(e)

            tries += 1
            if tries < max_tries:
                time.sleep(math.log(tries, math.pow(max_tries, 1.0 / max_sleep)))
            else:
                raise
