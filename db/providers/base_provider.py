#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.utils.db_utils import load_as_objs, decoded_hashid, encode_hashid_list
from sqlalchemy import exc, desc, or_
import settings
import asyncio
import functools
import os
from utils.async_utils import as_run_pro


class BaseProvider():

    def __init__(self, cls):
        self.cls = cls
        self.search_columns = ["title", "summary"]

    def reload(self, items):
        return load_as_objs(self.cls, items)

    @decoded_hashid
    def load(self, id):
        item = ""
        if not id or not isinstance(id, int):
            return item
        with query_session() as session:
            result = session.query(self.cls).get(id)
        if result:
            item = result.to_dict()
        return item

    def find_all(self, orderby, limit=None, offset=None, columns=None, keyword=None):
        collect = []

        if not orderby:
            return collect

        with query_session() as session:
            do = session.query(self.cls)
            if keyword:
                targets = [getattr(self.cls, column).contains(keyword)
                           for column in self.search_columns]
                do = do.filter(or_(*targets))

            result_set = do.order_by(desc(getattr(self.cls, orderby))
                                     ).limit(limit).offset(offset).all()
            items = [item.to_dict() for item in result_set]
            collect = items
        return collect

    def find_items_by_datetime_between(self, datetime_column, start, end, limit=None, offset=None, keyword=None):
        collect = []
        if not datetime_column:
            return collect

        with query_session() as session:
            do = session.query(self.cls)
            if keyword:
                targets = [getattr(self.cls, column).contains(keyword)
                           for column in self.search_columns]
                do = do.filter(or_(*targets))

            result_set = do.filter(getattr(self.cls, datetime_column).between(
                start, end)).order_by(desc(getattr(self.cls, datetime_column))).limit(limit).offset(offset).all()

            items = [item.to_dict() for item in result_set]
            collect = items
        return collect

    def find_distinct_items_by(self, name, items):
        if not name or not items:
            return items
        with query_session() as session:
            existed = [item[name] for item in items]
            result_set = session.query(self.cls).filter(getattr(self.cls, name).in_(existed)).all()
            dups = [dup.to_dict() for dup in result_set]
            items = [item for item in items if item[name] not in dups]
        return items

    async def as_find_distinct_items_by(self, name, items):
        return await as_run_pro(self.find_distinct_items_by, name, items)

    def save_all(self, items):
        objs = self.reload(items)
        ids = []
        with scoped_session() as session:
            for obj in objs:
                try:
                    with session.begin_nested():
                        session.add(obj)
                        session.flush()
                        ids.append(obj.id)
                except exc.IntegrityError as err:
                    if __debug__ and not settings.TESTING:
                        print(err)

        return encode_hashid_list(ids)
