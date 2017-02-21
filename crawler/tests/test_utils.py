#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawler.utils.datautils import delKey, trimDataVal

import unittest
class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_trimDataVal(self):
        data = {}
        data['foo'] = "foo_bar"
        trimDataVal("foo", "_bar", data)
        self.assertEqual(data, {'foo': "foo"})

    def test_delKey(self):
        data = {}
        data['foo'] = "foo"
        data['bar'] = "bar"
        delKey("foo", True, data)
        self.assertEqual(data, {'bar': "bar"})

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
