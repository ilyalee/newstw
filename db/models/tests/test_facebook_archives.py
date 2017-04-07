#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.pprint_helper import pprint_color
from db.database import scoped_session, Session
from db.models import FacebookArchive
import arrow
import unittest


class TestFacebookArchive(unittest.TestCase):

    def setUp(self):
        self.data = {
            'published': arrow.get("2017-01-23 12:34:56+08:00").datetime,
            'fbid': "1234567890",
            'from_id': "from_id test",
            'from_name': "from_name test",
            'message': "message test",
            'link': "https://foo.bar.baz",
            'hash': "hash test",
            'source': "abc"
        }

    def test_crud(self):

        # Create archive.
        with scoped_session() as session:
            archive = FacebookArchive(**self.data)
            session.add(archive)

        # Read archive.
        with scoped_session() as session:
            archive = session.merge(archive)
            self.assertEqual(archive.from_id, self.data['from_id'])
            self.assertEqual(archive.from_name, self.data['from_name'])
            self.assertEqual(archive.message, self.data['message'])
            self.assertEqual(archive.link, self.data['link'])
            self.assertEqual(archive.hash, self.data['hash'])
            self.assertEqual(archive.source, self.data['source'])
        # Update archive.
        with scoped_session() as session:
            archive = session.merge(archive)
            archive.message = "new message"

        with scoped_session() as session:
            archive = session.merge(archive)
            archive_id = archive.id
            self.assertEqual(archive.message, "new message")

        # Delete archive
        with scoped_session() as session:
            archive = session.merge(archive)
            session.delete(archive)

        with scoped_session() as session:
            archive = session.query(FacebookArchive).filter_by(id=archive_id).all()
            self.assertEqual(archive, [])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
