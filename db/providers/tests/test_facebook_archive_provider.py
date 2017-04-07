#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.pprint_helper import pprint_color
from db.providers import FacebookArchiveProvider
import unittest


class TestFacebookArchiveProvider(unittest.TestCase):

    def setUp(self):
        self.ap = FacebookArchiveProvider()
        self.data = {
            'fbid': '1234567890',
            'updated_time': "2017-01-23 12:34:56+08:00",
            'created_time': "2017-01-23 12:34:56+08:00",
            'from_id': "0987654321",
            'from_name': "from_name test",
            'message': "message test",
            'permalink_url': "https://foo.bar.baz",
            'hash': "hash test",
            'source': "abc",
        }
        self.items = [
            {'fbid': '1234567890', 'from_id': "0987654321", 'from_name': "from_name test1", 'hash': "test1", 'updated_time': "2017-01-01 01:02:03+08:00", 'created_time': "2017-01-23 12:34:56+08:00",
                'message': "test1", 'permalink_url': "http://foo.bar.baz", 'source': "any"},
            {'fbid': '1234567890', 'from_id': "0987654321", 'from_name': "from_name test2", 'hash': "test2", 'updated_time': "2017-12-12 12:12:12+08:00", 'created_time': "2017-01-23 12:34:56+08:00",
                'message': "test2", 'permalink_url': "http://foo.bar.baz", 'source': "any"}
        ]

    def test_save_all(self):
        items = self.ap.save_all(self.items)
        self.assertEqual(len(list(items)), 2)
        items = self.ap.save_all(self.items)
        self.assertEqual(len(list(items)), 0)
        items = self.ap.find_all()
        self.assertEqual(len(list(items)), len(self.items))
        total = self.ap.count()
        self.assertEqual(total, len(self.items))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
