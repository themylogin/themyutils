# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from themyutils.string import *

import unittest


class CommonPrefixTestCase(unittest.TestCase):
    def test_trivial(self):
        self.assertEqual(common_prefix(["lala", "lola", "lila"]), "l")

    def test_none(self):
        self.assertEqual(common_prefix(["lala", "pola", "nila"]), "")

    def test_empty(self):
        self.assertEqual(common_prefix(["lala", "", "lola"]), "")

    def test_fizruk(self):
        self.assertEqual(common_prefix(["Fizruk-2.Seriya.01.SATRip.avi",
                                        "Fizruk-2.Seriya.02.SATRip.avi",
                                        "Fizruk-2.Seriya.03.SATRip.avi"]), "Fizruk-2.Seriya.0")

    def test_fizruk_unicode(self):
        self.assertEqual(common_prefix(["Физрук 2 - 01 серия.mkv",
                                        "Физрук 2 - 02 серия.mkv",
                                        "Физрук 2 - 03 серия.mkv"]), "Физрук 2 - 0")


class CommonSufixTestCase(unittest.TestCase):
    def test_fizruk(self):
        self.assertEqual(common_suffix(["Fizruk-2.Seriya.01.SATRip.avi",
                                        "Fizruk-2.Seriya.02.SATRip.avi",
                                        "Fizruk-2.Seriya.03.SATRip.avi"]), ".SATRip.avi")

    def test_fizruk_unicode(self):
        self.assertEqual(common_suffix(["Физрук 2 - 01 серия.mkv",
                                        "Физрук 2 - 02 серия.mkv",
                                        "Физрук 2 - 03 серия.mkv"]), " серия.mkv")
