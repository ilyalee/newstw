#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fbfeed.utils.fbfeed_helper import fetch_feed
from utils.data_utils import data_filter
from utils.pprint_helper import pprint_color

import unittest


class TestFBFeed(unittest.TestCase):

    def setUp(self):
        pass

    def test_fetch_feed(self):
        fbid = "SeeZhubei"
        num = 40
        feed = fetch_feed(fbid, num)
        predict = ['failed']
        # pprint_color(feed[0])
        #self.assertIn("message", feed[0])
        self.assertIn("from", feed[0])
        self.assertIn("permalink_url", feed[0])
        self.assertIn("hash", feed[0])
        self.assertEqual(len(feed), num)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
