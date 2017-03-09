#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.utils.db_utils import load_as_objs, decoded_hashid, encode_hashid_list
from sqlalchemy import exc, desc
import settings
import asyncio
import functools


class BaseProvider():

    def __init__(self, cls):
        self.cls = cls

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

    def find_all(self, orderby, limit=None):
        items = []
        if not orderby:
            return items
        with query_session() as session:
            result_set = session.query(self.cls).order_by(desc(getattr(self.cls, orderby))).limit(limit).all()
            items = [item.to_dict() for item in result_set]
        return items

    def find_items_by_datetime_between(self, name, start, end):
        items = []
        if not name:
            return items
        with query_session() as session:
            result_set = session.query(self.cls).filter(getattr(self.cls, name).between(
                start, end)).order_by(desc(getattr(self.cls, name))).all()
            items = [item.to_dict() for item in result_set]
        return items

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
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, functools.partial(self.find_distinct_items_by, name, items))
        return await asyncio.ensure_future(future)

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
                    if __debug__ and not settings.TESTING: print(err)

        return encode_hashid_list(ids)
