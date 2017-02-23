#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fbfeed.utils.fbfeedhelper import fetchFeed
from fbfeed.utils.datautils import dataFilter
from fbfeed.utils.pprinthelper import pprint_color

import unittest
class TestFBFeed(unittest.TestCase):
    def setUp(self):
        pass

    def test_fetchFeed(self):
        fbid = "SeeZhubei"
        num = 40
        feed = fetchFeed(fbid, num)
        predict = ['failed']
        pprint_color(feed[0])
        self.assertEqual(len(feed), num)

    def test_dataFilter(self):
        items = [{'target': '123'}, {'target': 'test1'}, {'target': 'test2'}]
        feed = dataFilter("test", "target", items)
        self.assertEqual(len(feed), 2)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
