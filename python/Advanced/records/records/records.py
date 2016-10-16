#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from code import interact
from datetime import datetime
from collections import OrderedDict

import tablib
from docopt import docopt
from sqlalchemy import text, create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ.get('DATABASE_URL')


class Record(object):
    __slots__ = ('_keys', '_values')
    def __init__(self, keys, values):
        super(Record, self).__init__()
        self._keys = keys
        self._values = values

        assert len(self._keys) == len(self._values)

    def keys(self):
        return self._keys

    def values(self):
        return self._values

    def __repr__(self):
        return '<Record {}>'.format(self.export('json')[1:-1])

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.values()[keys]

        if key in self.keys():
            return self.values()[self.keys().index(key)]

        raise KeyError("Record contains no '{}' field.".format(key))

    @property
    def dataset(self):
        """A Tablib Dataset containing the row."""
        data = tablib.Dataset()
        data.headers = self.keys()

        row = _reduce_datetimes(self.values())
        data.append(row)

        return data

    def export(self, format, **kwargs):
        """Exports the row to the given format."""
        return self.dataset.export(format, **kwargs)

class RecordCollection(object):
    """
    records result
    """
    def __init__(self, rows):
        super(RecordCollection, self).__init__()
        self._rows = rows
        self._all_rows = []

    def __iter__(self):
        i = 0
        while True:
            if i < len(self):
                yield self[i]
            else:
                yield next(self)
            i += 1

    def __len__(self):
        return len(self._all_rows)

    def __getitem__(self, key):
        is_int = isinstance(key, int)
        if is_int:
            key = slice(key, key+1)

        while len(self) < key.stop or key.stop is None:
            try:
                next(self)
            except StopIteration:
                break

        rows = self._all_rows[key] #return array result
        if is_int:
            return rows[0]
        else:
            return RecordCollection(iter(rows))

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(e)

    def __dir__(self):
        standard = [
            # Would love to do this programatically, but couldn't figure out how.
            '__class__', '__ddir__', '__delattr__', '__doc__', '__format__',
            '__getattr__', '__getattribute__', '__getitem__', '__hash__',
            '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__',
            '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__',
            '__subclasshook__', '_keys', '_values', 'as_dict', 'dataset',
            'export', 'get', 'keys', 'values'
        ]

        # Merge standard attrs with generated ones (from column names).
        return sorted(standard + [str(k) for k in self.keys()])

    def get(self, key, default=None):
        """Returns the value for a given key, or default."""
        try:
            return self[key]
        except KeyError:
            return default

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            nextrow = next(self._rows)
            self._all_rows.append(nextrow)
            return nextrow
        except StopIteration:
            raise StopIteration('RecordCollection contains no more rows.')

    @property
    def dataset(self):
        data = tablib.Dataset()

        data.headers = self[0].keys()
        for row in self.all():
            row = _reduce_datetimes(row.values())
            data.append(row)

        return data

    def all(self, as_dict=False, as_ordereddict=False):
        rows = list(self)
        print "all"
        return rows

    def export(self, format, **kwargs):
        return elf.dataset.export(format, **kwargs)

class Database(object):
    def __init__(self, db_url=None, **kwargs):
        super(Database, self).__init__()
        self.db_url = db_url or DATABASE_URL

        if not self.db_url:
            raise ValueError("You must provide a db_url.")

        self.db = create_engine(db_url, **kwargs).connect()
        self.open = True

    def close(self):
        self.db.close()
        self.open = False

    def __enter__(self):
        return self

    def __exit__(self, exc, val, traceback):
        self.close()

    def __repr__(self):
        return ""

    def query(self, query, fetch_all=False, **params):
        """
        查询
        """
        cursor = self.db.execute(text(query), **params)
        rows_gen = (Record(cursor.keys(), row) for row in cursor)

        result = RecordCollection(rows_gen)

        if fetch_all:
            result.all()

        return result

def _reduce_datetimes(row):
    """Receives a row, converts datetimes to strings."""
    # receive the values of one row

    row = list(row)

    for i in range(len(row)):
        if hasattr(row[i], 'isoformat'):
            # 看当前字段是不是时间类型，有没有格式化时间的方法
            row[i] = row[i].isoformat()
    return tuple(row)

if __name__ == '__main__':
    # db = Database("mysql://root:123456@localhost:3306/SQLearn")
    # rows = db.query("select * from Orders")
    # print "rows --> ", rows
    # print rows.all()
    
    with Database("mysql://root:123456@localhost:3306/SQLearn") as db:
        rows = db.query("select * from Orders")
        print rows.all()
