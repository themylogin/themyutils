# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import logging
import math
import time

logger = logging.getLogger(__name__)


def retry(operation, max_tries=100, max_sleep=50, exceptions=(Exception,), logger=logger):
    tries = 0
    while True:
        try:
            return operation()
        except exceptions as e:
            logger.exception(e)

            tries += 1
            if tries < max_tries:
                time.sleep(math.log(tries, math.pow(max_tries, 1.0 / max_sleep)))
            else:
                raise
