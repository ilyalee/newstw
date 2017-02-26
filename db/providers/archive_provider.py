#!/usr/bin/env python
# -*- coding: utf-8 -*-
from db.database import scoped_session, query_session, Session
from db.models.archives import Archive
from sqlalchemy import exc


class ArchiveProvider():

    @staticmethod
    def load_as_archives(items):
        return [Archive(**item) for item in items]

    @staticmethod
    def find_distinct_items_by_hashs(hashs, items):
        with query_session() as session:
            result_set = session.query(Archive).filter(Archive.hash.in_(hashs)).all()
            dups = [dup.__dict__['hash'] for dup in result_set]
            items = [item for item in items if item['hash'] not in dups]
        return items

    @staticmethod
    def save_all(items):
        archives = ArchiveProvider.load_as_archives(items)
        acceptances = len(archives)
        with scoped_session() as session:
            for archive in archives:
                try:
                    with session.begin_nested():
                        session.add(archive)
                except exc.IntegrityError:
                    acceptances = acceptances - 1
        return acceptances
