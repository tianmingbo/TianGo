# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: field.py
@time: 2024/1/21  21:32
@desc: 
"""


class Field:
    def __init__(self, pydal, pydal_cursor, pydal_field):
        self._pydal = pydal
        self._pydal_cursor = pydal_cursor
        self._pydal_field = pydal_field

    def __eq__(self, other):
        if not isinstance(other, Field):
            return self._pydal_field.__eq__(other)
        return self._pydal_field.__eq__(other._pydal_field)

    def __ne__(self, other):
        return self._pydal_field.__ne__(other)

    def __gt__(self, other):
        return self._pydal_field.__gt__(other)

    def __ge__(self, other):
        return self._pydal_field.__ge__(other)

    def __lt__(self, other):
        return self._pydal_field.__lt__(other)

    def __le__(self, other):
        return self._pydal_field.__le__(other)

    def __invert__(self):
        return self._pydal_field.__invert__()

    def __str__(self):
        return self._pydal_field.__str__()

    def __repr__(self):
        return self._pydal_field.__repr__()

    def like(self, expression, case_sensitive=True, escape=None):
        query = self._pydal_field.like(expression, case_sensitive, escape)
        return query

    @property
    def requires(self):
        return self._pydal_field.requires()

    @property
    def type(self):
        return self._pydal_field.type()

    def with_alias(self, alias):
        return self._pydal_field.with_alias(alias)
