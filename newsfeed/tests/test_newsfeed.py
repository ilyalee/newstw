#!/usr/bin/env python
# -*- coding: utf-8 -*-

from newsfeed.filter import NewsFeedFilter
from utils.pprint_helper import pprint_color
import unittest
import warnings


class TestNewsFeed(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    def test_fetch_feed(self):
        url = "http://news.ltn.com.tw/rss/focus.xml"
        feed = NewsFeedFilter(url).output()
        self.assertIn("title", feed[0])
        self.assertIn("summary", feed[0])
        self.assertIn("published", feed[0])
        self.assertIn("link", feed[0])
        self.assertIn("hash", feed[0])
        self.assertIn("source", feed[0])
        self.assertNotIn("keyword", feed[0])
        feed = NewsFeedFilter(url, full_text=True).output()
        self.assertIn("summary", feed[0])
        # pprint_color(feed[0])
        feed = NewsFeedFilter(url, "台灣").output()
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
        warnings.filterwarnings(action="default", message="unclosed", category=ResourceWarning)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
