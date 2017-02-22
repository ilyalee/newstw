#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawler.utils.crawlerhelper import fetchNewsAll
from crawler.utils.pprinthelper import pprint_color

import unittest
class TestAsyncs(unittest.TestCase):
    def setUp(self):
        pass

    def test_fetchNewsAll(self):
        url = ["https://goo.gl/rXe5sV", "https://goo.gl/bQMi1B", "https://goo.gl/IRJ7Pb"]
        collect = fetchNewsAll(url)
        pprint_color(collect)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
