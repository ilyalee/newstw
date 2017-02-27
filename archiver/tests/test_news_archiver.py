#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.pprint_helper import pprint_color

import unittest


class TestNewsArchive(unittest.TestCase):

    def setUp(self):
        self.data = {
            'published': "2017-01-23 12:34:56+08:00",
            'title': "title test",
            'summary': "summary test",
            'link': "https://foo.bar.baz",
            'hash': "hash test",
            'source': "abc"
        }

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
