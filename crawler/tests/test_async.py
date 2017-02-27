#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawler.utils.crawler_helper import fetch_news_all
from utils.pprint_helper import pprint_color

import unittest


class TestAsyncs(unittest.TestCase):

    def setUp(self):
        pass

    def test_fetch_news_all(self):
        url = ["https://goo.gl/rXe5sV", "https://goo.gl/bQMi1B", "https://goo.gl/IRJ7Pb"]
        collect = fetch_news_all(url)
        #pprint_color(collect)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(warnings='ignore')
