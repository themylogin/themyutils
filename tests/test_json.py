# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from datetime import datetime, timedelta
from mock import Mock, patch
import unittest

import json
import themyutils.json


class LoadsTestCase(unittest.TestCase):
    def test_unicode_hook_called(self):
        unicode_hook = Mock()
        with patch.object(themyutils.json.JSONDecoder, "unicode_hook", unicode_hook):
            themyutils.json.loads('{"data": {"datetime": "2014-02-02T17:32:01", "datetimes": [{"asdict": '+\
                                   '"2014-02-02T17:32:02"}, "2014-02-02T17:32:03"]}}')
            unicode_hook.assert_any_call("2014-02-02T17:32:01")
            unicode_hook.assert_any_call("2014-02-02T17:32:02")
            unicode_hook.assert_any_call("2014-02-02T17:32:03")

    def test_unicode_hook_works(self):
        hook = Mock()
        hook.class_name = "hook"
        hook.decode = Mock(return_value=42)
        with patch.object(themyutils.json, "hooks", [hook]):
            self.assertEqual(themyutils.json.JSONDecoder.unicode_hook("hook(value)"), 42)
            hook.decode.assert_called_once_with("value")

    def test_unicode_hook_handles_ValueError(self):
        hook = Mock()
        hook.class_name = "hook"
        hook.decode = Mock(side_effect=ValueError)
        with patch.object(themyutils.json, "hooks", [hook]):
            self.assertEqual(themyutils.json.JSONDecoder.unicode_hook("hook(value)"), "hook(value)")

    def test_unicode_hook_distinguishes_classes(self):
        hook1 = Mock()
        hook2 = Mock()
        hook1.class_name = "hook1"
        hook2.class_name = "hook2"
        with patch.object(themyutils.json, "hooks", [hook1, hook2]):
            themyutils.json.JSONDecoder.unicode_hook("hook1(value1)")
            themyutils.json.JSONDecoder.unicode_hook("hook2(value2)")
            hook1.decode.assert_called_once_with("value1")
            hook2.decode.assert_called_once_with("value2")


class DumpsTestCase(unittest.TestCase):
    def test_object_hook_works(self):
        class Test(object):
            pass

        hook = Mock()
        hook.class_name = "test"
        hook.hook_for = Test
        hook.encode = Mock(return_value="test_object")
        with patch.object(themyutils.json, "hooks", [hook]):
            self.assertEqual(themyutils.json.JSONEncoder().default(Test()), "test(test_object)")


class HooksTestCase(unittest.TestCase):
    def test_all_hooks_are_working(self):
        tests = [
            (datetime(2014, 2, 2, 17, 32, 1), 'datetime(2014-02-02T17:32:01)'),
            (timedelta(seconds=10), 'timedelta(PT10S)')
        ]

        for o, s in tests:
            o = [o]
            s = json.dumps([s])
            self.assertEqual(themyutils.json.dumps(o), s)
            self.assertEqual(themyutils.json.loads(s), o)
