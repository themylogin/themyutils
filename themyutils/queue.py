# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import Queue
import threading


class QueueDemux(threading.Thread):
    def __init__(self, queue):
        super(QueueDemux, self).__init__()
        self.daemon = True

        self.in_queue = queue
        self.output_queues = []

        self.start()

    def run(self):
        while True:
            v = self.in_queue.get()
            for q in self.output_queues:
                q.put(v)

    def clone(self):
        q = Queue.Queue()
        self.output_queues.append(q)
        return q
