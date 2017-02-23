#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fbfeed.utils.fbfeed_helper import fetch_feed
from fbfeed.utils.data_utils import data_filter
from fbfeed.utils.pprint_helper import pprint_color

import unittest


class TestFBFeed(unittest.TestCase):

    def setUp(self):
        pass

    def test_fetch_feed(self):
        fbid = "SeeZhubei"
        num = 40
        feed = fetch_feed(fbid, num)
        predict = ['failed']
        pprint_color(feed[0])
        self.assertIn("fbid", feed[0])
        self.assertEqual(len(feed), num)

    def test_data_filter(self):
        items = [{'target': '123'}, {'target': 'test1'}, {'target': 'test2'}]
        feed = data_filter("test", "target", items)
        self.assertEqual(len(feed), 2)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
