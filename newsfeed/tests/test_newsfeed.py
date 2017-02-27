#!/usr/bin/env python
# -*- coding: utf-8 -*-

from newsfeed.utils.newsfeed_helper import fetch_feed
from utils.pprint_helper import pprint_color
import unittest


class TestNewsFeed(unittest.TestCase):

    def setUp(self):
        pass

    def test_fetch_feed(self):
        url = "http://www.chinatimes.com/rss/realtimenews.xml"
        feed = fetch_feed(url)
        self.assertIn("title", feed[0])
        self.assertIn("summary", feed[0])
        self.assertIn("published", feed[0])
        self.assertIn("link", feed[0])
        self.assertIn("hash", feed[0])
        self.assertIn("source", feed[0])
        self.assertNotIn("keyword", feed[0])
        feed = fetch_feed(url, '', True)
        self.assertIn("summary", feed[0])
        #pprint_color(feed[0])
        feed = fetch_feed(url, "台灣")
        for item in feed:
            self.assertIn("title", item)
            self.assertIn("summary", item)
            self.assertIn("published", item)
            self.assertIn("link", item)
            self.assertIn("keyword", item)
            self.assertIn("source", item)
            self.assertEqual(item['keyword'], "台灣")
            self.assertNotEqual(item['source'], "any")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(warnings='ignore')
