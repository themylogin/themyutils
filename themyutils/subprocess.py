# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import logging
import prctl
import signal

logger = logging.getLogger(__name__)

__all__ = [b"preexec_fn"]


def preexec_fn():
    prctl.set_pdeathsig(signal.SIGKILL)
