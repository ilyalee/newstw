#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.pprint_helper import pprint_color
from utils.data_utils import data_updater, datetime_encapsulator
from db import models
from db.database import scoped_session, Session
from db.models.archives import Archive
from db.providers.archive_provider import ArchiveProvider
import unittest
import settings


class TestArchiveProvider(unittest.TestCase):

    def setUp(self):
        self.ap = ArchiveProvider()
        self.data = {
            'published': "2017-01-23 12:34:56+08:00",
            'title': "title test",
            'summary': "summary test",
            'link': "https://foo.bar.baz",
            'hash': "hash test",
            'source': "abc"
        }
        self.items = [
            {'title': "title test1", 'hash': "test1", 'published': "2017-01-01 01:02:03+08:00",
                'summary': "test1", 'link': "http://foo.bar.baz", 'source': "any"},
            {'title': "title test2", 'hash': "test2", 'published': "2017-12-12 12:12:12+08:00",
                'summary': "test2", 'link': "http://foo.bar.baz", 'source': "any"}
        ]

    def test_reload(self):
        objs = self.ap.reload(self.items)
        for obj in objs:
            self.assertIsInstance(obj, Archive)

    def test_find_distinct_items_by(self):
        items = self.ap.find_distinct_items_by("hash", self.items)
        self.assertEqual(self.items, items)

    def test_save_all(self):
        items = self.ap.save_all(self.items)
        self.assertEqual(len(items), 2)
        items = self.ap.save_all(self.items)
        self.assertEqual(len(items), 0)
        items = self.ap.find_all("published")
        self.assertEqual(len(items), len(self.items))

    def test_sqlite_datetime_compatibility(self):
        items = data_updater("published", "published", datetime_encapsulator, True, self.items)
        self.assertEqual(self.items, items)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
