#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from archiver.utils.archiver_utils import
#from archiver.utils.archiver_helper import fetch_news
from archiver.utils.pprint_helper import pprint_color
from db.database import scoped_session, Session
from db.models.archives import Archive
from db.providers.archive_provider import ArchiveProvider

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

    def test_archive_provider(self):
        ap = ArchiveProvider()
        (obj,) = ap.load([{'title': 'title test'}])
        self.assertIsInstance(obj, Archive)

    def test_crud(self):

        # Create archive.
        with scoped_session() as session:
            archive = Archive(**self.data)
            session.add(archive)

        # Read archive.
        with scoped_session() as session:
            archive = session.merge(archive)
            self.assertEqual(archive.title, self.data['title'])
            self.assertEqual(archive.summary, self.data['summary'])
            self.assertEqual(archive.link, self.data['link'])
            self.assertEqual(archive.hash, self.data['hash'])
            self.assertEqual(archive.source, self.data['source'])
        # Update archive.
        with scoped_session() as session:
            archive = session.merge(archive)
            archive.title = "new title"

        with scoped_session() as session:
            archive = session.merge(archive)
            archive_id = archive.id
            self.assertEqual(archive.title, "new title")

        # Delete archive
        with scoped_session() as session:
            archive = session.merge(archive)
            session.delete(archive)

        with scoped_session() as session:
            archive = session.query(Archive).filter_by(id=archive_id).all()
            self.assertEqual(archive, [])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
