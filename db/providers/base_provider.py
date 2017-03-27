#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.utils.db_utils import load_as_objs, decoded_hashid, encode_hashid_list, list2str, reload_keyword, load_as_dicts
from sqlalchemy import exc, desc, or_, func
import settings
import asyncio
import functools
import os
from utils.async_utils import as_run
from utils.data_utils import isiterable, clist


class BaseProvider():

    def __init__(self, cls):
        self.cls = cls
        self.search_columns = []
        self.order_by_columns = []

    def reload(self, items):
        return load_as_objs(self.cls, items)

    @decoded_hashid
    def load(self, id):
        with query_session() as session:
            result = session.query(self.cls).get(id)
            if result:
                return result.to_dict()

    def count_all(self, columns=None, keywords=None):
        with query_session() as session:
            do = session.query(self.cls)
            do = self.do_keywords(keywords, do)
            num = do.with_entities(func.count(self.cls.id)).scalar()
            return num

    def do_keywords(self, keywords, do):
        def _and(do, keywords):
            for keyword in keywords:
                targets = [(getattr(self.cls, column).contains(keyword))
                           for column in self.search_columns]
                if targets:
                    do = do.filter(or_(*targets))
            return do

        def _or(do, keywords):
            targets = []
            for keyword in keywords:
                targets = targets + [getattr(self.cls, column).contains(keyword)
                                     for column in self.search_columns]
            if targets:
                do = do.filter(or_(*targets))
            return do

        (keywords, op) = reload_keyword(keywords)
        return {'AND': _and(do, keywords), 'OR': _or(do, keywords)}.get(op, 'OR')

    def do_values(self, values, column, do):
        targets = (getattr(self.cls, column) == value
                   for value in values)
        return do.filter(or_(*targets))

    def find_all(self, limit=None, offset=None, keywords=None):
        with query_session() as session:
            do = session.query(self.cls)
            do = self.do_keywords(keywords, do)
            orders = list2str(self.order_by_columns)
            result_set = do.order_by(desc(orders)).limit(limit).offset(offset).all()
            return load_as_dicts(result_set)

    def find_items_by_datetime_between(self, datetime_column, start, end, limit=None, offset=None, keywords=None):
        if not datetime_column:
            return []

        with query_session() as session:
            do = session.query(self.cls)
            do = self.do_keywords(keywords, do)
            result_set = do.filter(getattr(self.cls, datetime_column).between(
                start, end)).order_by(desc(getattr(self.cls, datetime_column))).limit(limit).offset(offset).all()
            return load_as_dicts(result_set)

    def find_items_by_values(self, values, column, limit=None, offset=None, keywords=None):
        if not values:
            return []

        if not isiterable(values):
            values = clist(values)

        with query_session() as session:
            do = session.query(self.cls)
            do = self.do_values(values, column, do)
            do = self.do_keywords(keywords, do)
            orders = list2str(self.order_by_columns)
            result_set = do.order_by(desc(orders)).limit(limit).offset(offset).all()
            return load_as_dicts(result_set)

    def find_distinct_items_by(self, name, items):
        if not name or not items:
            return items
        with query_session() as session:
            existed = set(item[name] for item in items)
            result_set = session.query(self.cls).filter(getattr(self.cls, name).in_(existed)).all()
            dups = load_as_dicts(result_set)
            return (item for item in items if item[name] not in dups)

    async def as_find_distinct_items_by(self, name, items):
        return await as_run()(self.find_distinct_items_by)(name, items)

    def save_all(self, items):
        with scoped_session() as session:
            ids = []
            for obj in self.reload(items):
                try:
                    with session.begin_nested():
                        session.add(obj)
                        session.flush()
                        ids.append(obj.id)
                except exc.IntegrityError as e:
                    if __debug__ and settings.TESTING:
                        print(e)
            return encode_hashid_list(ids)
