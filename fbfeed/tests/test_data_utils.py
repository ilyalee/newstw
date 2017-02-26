#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.data_utils import data_filter, githash
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
        hexstr = "df65291e1b9c75dde1a6066fe2cbfb66c4d8ee055daf60f6e5f3e648"
        hashed = githash(title.encode('utf-8'), hexdigest=True)
        self.assertEqual(hashed, hexstr)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
