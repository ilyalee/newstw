#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.utils.db_utils import load_as_objs, decoded_hashid, encode_hashid_list, list2str, reload_keyword, load_as_dicts, auto_vacuum
from sqlalchemy import exc, desc, or_, func, text
import asyncio
import functools
import os
import itertools
from utils.async_utils import as_run
from utils.data_utils import isiterable, clist
from utils.debug_utils import debug_testing_mode


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

    def count(self, keywords=None):
        with query_session() as session:
            do = session.query(self.cls)
            do = self.do_keywords(keywords, do)
            num = do.with_entities(func.count(self.cls.id)).scalar()
            return num

    def count_items_by_values(self, values, values_column, keywords=None):
        if not values:
            return
        if not isiterable(values):
            values = clist(values)
        with query_session() as session:
            do = session.query(self.cls)
            do = self.do_values(values, values_column, do)
            do = self.do_keywords(keywords, do)
            num = do.with_entities(func.count(self.cls.id)).scalar()
            return num

    def count_by_datetime_between(self, datetime_column, start, end, keywords=None):
        if not datetime_column:
            return
        with query_session() as session:
            do = session.query(self.cls)
            do = do.filter(getattr(self.cls, datetime_column).between(
                start, end))
            do = self.do_keywords(keywords, do)
            num = do.with_entities(func.count(self.cls.id)).scalar()
            return num

    def count_items_by_values_and_datetime_between(self, values, values_column, datetime_column, start, end, keywords=None):
        if not values:
            return
        if not values_column:
            return
        if not datetime_column:
            return
        if not isiterable(values):
            values = clist(values)
        with query_session() as session:
            do = session.query(self.cls)
            do = do.filter(getattr(self.cls, datetime_column).between(
                start, end))
            do = self.do_values(values, values_column, do)
            do = self.do_keywords(keywords, do)
            num = do.with_entities(func.count(self.cls.id)).scalar()
            return num

    def sum(self, column):
        if not column:
            return
        with query_session() as session:
            do = session.query(self.cls)
            num = do.with_entities(func.sum(getattr(self.cls, column))).scalar()
            return num

    def sum_by_datetime_between(self, column, datetime_column, start, end):
        if not column:
            return
        if not datetime_column:
            return
        with query_session() as session:
            do = session.query(self.cls)
            do = do.filter(getattr(self.cls, datetime_column).between(
                start, end))
            num = do.with_entities(func.sum(getattr(self.cls, column))).scalar()
            return num

    def do_keywords(self, keywords, do):
        if not keywords:
            return do

        def _and(do, keywords):
            for keyword in keywords:
                targets = [getattr(self.cls, column).ilike(
                    f'%{keyword}%') for column in self.search_columns]
                if targets:
                    do = do.filter(or_(*targets))
            return do

        def _or(do, keywords):
            targets = []
            for keyword in keywords:
                targets = targets + \
                    [getattr(self.cls, column).ilike(f'%{keyword}%')
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

    def do_orders(self, orders, do):
        for order in orders:
            do = do.order_by(desc(getattr(self.cls, order)))
        return do

    def find_all(self, limit=None, offset=None, keywords=None):
        with query_session() as session:
            do = session.query(self.cls)
            do = self.do_keywords(keywords, do)
            if limit == 1 and offset == 1:
                do = self.do_orders(self.order_by_columns, do)
            result_set = do.limit(limit).offset(offset).all()
            return load_as_dicts(result_set)

    def find_items_by_datetime_between(self, datetime_column, start, end, limit=None, offset=None, keywords=None):
        if not datetime_column:
            return []

        with query_session() as session:
            do = session.query(self.cls)
            do = do.filter(getattr(self.cls, datetime_column).between(
                start, end)).order_by(desc(getattr(self.cls, datetime_column)))
            do = self.do_keywords(keywords, do)
            result_set = do.limit(limit).offset(offset).all()
            return load_as_dicts(result_set)

    def find_items_by_values_and_datetime_between(self, values, values_column, datetime_column, start, end, limit=None, offset=None, keywords=None):
        if not values:
            return []
        if not values_column:
            return []
        if not datetime_column:
            return []
        if not isiterable(values):
            values = clist(values)

        with query_session() as session:
            do = session.query(self.cls)
            do = do.filter(getattr(self.cls, datetime_column).between(
                start, end)).order_by(desc(getattr(self.cls, datetime_column)))
            do = self.do_values(values, values_column, do)
            do = self.do_keywords(keywords, do)
            result_set = do.limit(limit).offset(offset).all()
            return load_as_dicts(result_set)

    def find_items_by_values(self, values, values_column, limit=None, offset=None, keywords=None):
        if not values:
            return []
        if not values_column:
            return []
        if not isiterable(values):
            values = clist(values)

        with query_session() as session:
            do = session.query(self.cls)
            do = self.do_values(values, values_column, do)
            do = self.do_keywords(keywords, do)
            do = self.do_orders(self.order_by_columns, do)
            result_set = do.limit(limit).offset(offset).all()
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
                    if debug_testing_mode():
                        print(e)

            auto_vacuum()
            return encode_hashid_list(ids)

    def save(self, items):
        return self.save_all(items)

    def update(self, value, name, item):
        with scoped_session() as session:
            ids = []
            (obj,) = self.reload([item])
            do = session.query(self.cls)
            do = do.filter(getattr(self.cls, name) == value)
            do = do.update(item)

            do = session.query(self.cls)
            obj = do.filter(getattr(self.cls, name) == value).first()
            ids.append(obj.id)
            auto_vacuum()
            return encode_hashid_list(ids)

    @decoded_hashid
    def remove(self, id):
        status = False
        if isinstance(id, str):
            return status

        with scoped_session() as session:
            try:
                status = session.query(self.cls).filter(getattr(self.cls, 'id') == id).delete()
            except exc.IntegrityError as e:
                print(e)

            return status
