#!/usr/bin/env python
# -*- coding: utf-8 -*-

from newsfeed.utils.newsfeed_helper import fetch_feed
from newsfeed.utils.data_utils import data_filter, data_cleaner, data_hasher, githash
from newsfeed.utils.pprint_helper import pprint_color

import unittest


class TestDataUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_data_cleaner(self):
        items = [{'foo1': "bar1\nbaz", 'foo2': "bar2\nbaz"}]
        predict = [{'foo1': "bar1\nbaz", 'foo2': "bar2baz"}]
        key = "foo2"
        self.assertEqual(data_cleaner(key, items), predict)
        items = [{'foo1': "bar1\nbaz", 'foo2': " bar2 baz "}]
        predict = [{'foo1': "bar1\nbaz", 'foo2': "bar2 baz"}]
        key = "foo2"
        self.assertEqual(data_cleaner(key, items), predict)

    def test_data_filter(self):
        items = [{'bar': "1", 'foo': "2"}, {'bar': "3", 'foo': "4"}]
        predict = [{'bar': "3", 'foo': "4"}]
        key = ["foo"]
        text = "4"
        self.assertEqual(data_filter(text, key, items), predict)

    def test_data_hasher(self):
        items = [{'foo': "測試1", 'bar': "測試2"}]
        items = data_hasher("hash", ["foo", "bar"], items)
        self.assertEqual(items[0]["hash"], githash("測試1測試2", hexdigest=True))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()