# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import timedelta
import unittest

from themyutils.datetime.timedelta import *


class TimedeltaInWordsTestCase(unittest.TestCase):
    def test_integers(self):
        seconds = 16 * 60 * 60 + 8 * 60 + 4
        self.assertEqual(timedelta_in_words(seconds), timedelta_in_words(timedelta(seconds=seconds)))

    def test_accuracy(self):
        seconds = 32 * 24 * 60 * 60 + 16 * 60 * 60 + 8 * 60 + 4
        self.assertEqual(timedelta_in_words(seconds, 1), "32 дня")
        self.assertEqual(timedelta_in_words(seconds, 2), "32 дня 16 часов")
        self.assertEqual(timedelta_in_words(seconds, 3), "32 дня 16 часов 8 минут")
        self.assertEqual(timedelta_in_words(seconds, 100), "32 дня 16 часов 8 минут")

    def test_less_than_minute(self):
        self.assertEqual(timedelta_in_words(30, 1), "менее минуты")

    def test_less_than_hour(self):
        self.assertEqual(timedelta_in_words(30 * 60 + 15, 1), "30 минут")

    def test_less_than_day(self):
        self.assertEqual(timedelta_in_words(4 * 60 * 60 + 30 * 60 + 15, 1), "4 часа")
        self.assertEqual(timedelta_in_words(4 * 60 * 60 + 30 * 60 + 15, 2), "4 часа 30 минут")

    def test_less_than_two_days(self):
        self.assertEqual(timedelta_in_words(24 * 60 * 60 + 4 * 60 * 60 + 30 * 60 + 15, 1), "1 день")
        self.assertEqual(timedelta_in_words(24 * 60 * 60 + 4 * 60 * 60 + 30 * 60 + 15, 2), "1 день 4 часа")

    def test_less_than_three_days(self):
        self.assertEqual(timedelta_in_words(2 * 24 * 60 * 60 + 4 * 60 * 60 + 30 * 60 + 15, 1), "2 дня")
        self.assertEqual(timedelta_in_words(2 * 24 * 60 * 60 + 4 * 60 * 60 + 30 * 60 + 15, 2), "2 дня 4 часа")
