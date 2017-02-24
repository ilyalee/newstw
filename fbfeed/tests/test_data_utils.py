#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fbfeed.utils.fbfeed_helper import fetch_feed
from fbfeed.utils.data_utils import data_filter, githash
from fbfeed.utils.pprint_helper import pprint_color

import unittest


class TestDataUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_data_filter(self):
        items = [{'target': '123'}, {'target': 'test1'}, {'target': 'test2'}]
        feed = data_filter("test", "target", items)
        self.assertEqual(len(feed), 2)

    def test_githash(self):
        title = "標題測試"
        hexstr = "77846ee3bc54633ee1b1683d8c5dc5d1bfa02a51"
        hashed = githash(title.encode('utf-8'), hexdigest=True)
        self.assertEqual(hashed, hexstr)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
