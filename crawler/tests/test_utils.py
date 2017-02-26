#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.data_utils import del_key, trim_data_val

import unittest


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_trim_data_val(self):
        data = {}
        data['foo'] = "foo_bar"
        trim_data_val("foo", "_bar", data)
        self.assertEqual(data, {'foo': "foo"})

    def test_delKey(self):
        data = {}
        data['foo'] = "foo"
        data['bar'] = "bar"
        del_key("foo", True, data)
        self.assertEqual(data, {'bar': "bar"})

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
