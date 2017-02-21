#!/usr/bin/env python
# -*- coding: utf-8 -*-

from newsfeed.utils.newsfeedhelper import fetchFeed
from newsfeed.utils.datautils import dataCleaner, dataFilter
from newsfeed.utils.pprinthelper import pprint_color

import unittest
class TestNewsFeed(unittest.TestCase):
    def setUp(self):
        pass

    def test_dataCleaner(self):
        items = [{'foo1': "bar1\nbaz", 'foo2': "bar2\nbaz"}]
        predict = [{'foo1': "bar1\nbaz", 'foo2': "bar2baz"}]
        key = "foo2"
        self.assertEqual(dataCleaner(key, items), predict)

    def test_dataFilter(self):
        items = [{'bar': "1", 'foo': "2"}, {'bar': "3", 'foo': "4"}]
        predict = [{'bar': "3", 'foo': "4"}]
        key = ["foo"]
        text = "4"
        self.assertEqual(dataFilter(text, key, items), predict)

    def test_NewsFeedProcessor(self):
        url = "http://www.chinatimes.com/rss/realtimenews.xml"
        feed = fetchFeed(url)
        self.assertIn("title", feed[0])
        self.assertIn("summary", feed[0])
        self.assertIn("published", feed[0])
        self.assertIn("link", feed[0])
        pprint_color(feed[0])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
