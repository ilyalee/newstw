#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.pprint_helper import pprint_color
from db import models
from db.database import scoped_session, Session
from db.models.archives import Archive
from db.providers.archive_provider import ArchiveProvider
from sqlalchemy import create_engine
import unittest
import settings
from unittest import mock


class TestArchiveProvider(unittest.TestCase):

    def setUp(self):
        self.data = {
            'published': "2017-01-23 12:34:56+08:00",
            'title': "title test",
            'summary': "summary test",
            'link': "https://foo.bar.baz",
            'hash': "hash test",
            'source': "abc"
        }
        self.items = [{'title': 'title test', 'hash': 'test'}]

    def test_reload(self):
        ap = ArchiveProvider()
        (obj,) = ap.reload(self.items)
        self.assertIsInstance(obj, Archive)

    def test_find_distinct_items_by(self):
        ap = ArchiveProvider()
        items = ap.find_distinct_items_by("hash", self.items)
        self.assertEqual(self.items, items)

    def test_save_all(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
