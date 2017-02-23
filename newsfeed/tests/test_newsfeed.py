#!/usr/bin/env python
# -*- coding: utf-8 -*-

from newsfeed.utils.newsfeed_helper import fetch_feed
from newsfeed.utils.data_utils import data_cleaner, data_filter
from newsfeed.utils.pprint_helper import pprint_color

import unittest
class TestNewsFeed(unittest.TestCase):
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

    def test_fetch_feed(self):
        url = "http://www.chinatimes.com/rss/realtimenews.xml"
        feed = fetch_feed(url)
        self.assertIn("title", feed[0])
        self.assertIn("summary", feed[0])
        self.assertIn("published", feed[0])
        self.assertIn("link", feed[0])
        self.assertNotIn("keyword", feed[0])
        feed = fetch_feed(url, '', True)
        self.assertIn("summary", feed[0])
        pprint_color(feed[0])
        feed = fetch_feed(url, "台灣")
        if len(feed) > 0:
            self.assertIn("title", feed[0])
            self.assertIn("summary", feed[0])
            self.assertIn("published", feed[0])
            self.assertIn("link", feed[0])
            self.assertIn("keyword", feed[0])
            self.assertEqual(feed[0]['keyword'], "台灣")
            pprint_color(feed[0])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
