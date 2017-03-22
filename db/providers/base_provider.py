#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.utils.db_utils import load_as_objs, decoded_hashid, encode_hashid_list, list2str
from sqlalchemy import exc, desc, or_, func
import settings
import asyncio
import functools
import os
from utils.async_utils import as_run


class BaseProvider():

    def __init__(self, cls):
        self.cls = cls
        self.search_columns = []
        self.order_by_columns = []

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

    def count_all(self, columns=None, keywords=None):
        num = None

        if keywords:
            keywords = keywords.split("|")
        else:
            keywords = []

        with query_session() as session:
            do = session.query(self.cls)
            targets = []
            for keyword in keywords:
                targets = targets + [getattr(self.cls, column).contains(keyword)
                                     for column in self.search_columns]
            if targets:
                do = do.filter(or_(*targets))

            num = do.with_entities(func.count(self.cls.id)).scalar()
        return num

    def find_all(self, limit=None, offset=None, keywords=None):

        collect = []

        if keywords:
            keywords = keywords.split("|")
        else:
            keywords = []

        with query_session() as session:
            do = session.query(self.cls)
            targets = []
            for keyword in keywords:
                targets = targets + [getattr(self.cls, column).contains(keyword)
                                     for column in self.search_columns]
            if targets:
                do = do.filter(or_(*targets))

            orders = list2str(self.order_by_columns)
            result_set = do.order_by(desc(orders)).limit(limit).offset(offset).all()

            items = [item.to_dict() for item in result_set]
            collect = items
        return collect

    def find_items_by_datetime_between(self, datetime_column, start, end, limit=None, offset=None, keywords=None):
        collect = []

        if not datetime_column:
            return collect

        if keywords:
            keywords = keywords.split("|")
        else:
            keywords = []

        with query_session() as session:
            do = session.query(self.cls)
            targets = []
            for keyword in keywords:
                targets = targets + [getattr(self.cls, column).contains(keyword)
                                     for column in self.search_columns]
            if targets:
                do = do.filter(or_(*targets))

            result_set = do.filter(getattr(self.cls, datetime_column).between(
                start, end)).order_by(desc(getattr(self.cls, datetime_column))).limit(limit).offset(offset).all()

            items = [item.to_dict() for item in result_set]
            collect = items
        return collect

    def find_items_by_values(self, values, column, limit=None, offset=None):
        collect = []

        if not values:
            return collect

        if isinstance(values, str):
            values = [values]

        with query_session() as session:
            do = session.query(self.cls)
            targets = [getattr(self.cls, column) == value
                       for value in values]
            do = do.filter(or_(*targets))

            orders = list2str(self.order_by_columns)
            result_set = do.order_by(desc(orders)).limit(limit).offset(offset).all()

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
        return await as_run(self.find_distinct_items_by, name, items)

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
