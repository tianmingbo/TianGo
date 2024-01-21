# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: row.py
@time: 2024/1/21  21:32
@desc: 封装查询结果
"""
import json
from datetime import datetime


class Row:
    def __init__(self, field_names, raw_data):
        self._raw_data = raw_data  # 原始
        self._row_data = {}  # 行
        self._field_name = field_names
        for k, v in enumerate(field_names):
            self._row_data[v] = raw_data[k]

    @property
    def field_names(self):
        return self._field_name

    @property
    def raw_data(self):
        return self._raw_data

    @property
    def row_data(self):
        return self._row_data

    def as_dict(self):
        new_dict = {}
        for k, v in self._row_data.items():
            new_dict[k] = v if not isinstance(v, datetime) else str(v)
        return new_dict

    def set(self, key, value):
        self._row_data[key] = value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._row_data.__str__()

    def __getitem__(self, item):
        return self._row_data[item]

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __contains__(self, item):
        return self._row_data.__contains__(item)


class Rows:
    def __init__(self, description, raw_data):
        self._rows = []
        self._field_names = []
        self._raw_data = raw_data
        for f in description:
            self._field_names.append(f[0])
        for r in raw_data:
            self._rows.append(Row(self._field_names, r))

    @property
    def rows(self):
        return self._rows

    @property
    def field_names(self):
        return self._field_names

    @property
    def raw_data(self):
        return self._raw_data

    def as_list(self) -> [dict]:
        res = []
        for row in self.rows:
            res.append(row.as_dict())
        return res

    def as_json(self):
        return json.dumps(self.as_list())

    def first(self):
        return self.rows[0] if self.rows.__len__() > 0 else None

    def count(self):
        return len(self.rows)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._rows.__str__()

    def __getitem__(self, item):
        return self._rows[item]

    def __iter__(self):
        return self._rows.__iter__()

    def __len__(self):
        return self.count()
