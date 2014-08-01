#!/usr/bin/python

import nose
from tmatch import tmatch

def test_tmatch_basic():
    "test tmatch.tmatch"

    assert tmatch('?a', 8) == (True, {'?a': 8})

    assert tmatch('?a', 'abc') == (True, {'?a': 'abc'})

    assert tmatch('?a', 2.3) == (True, {'?a': 2.3})

    assert tmatch('?a', 2+3j) == (True, {'?a': 2+3j})

    assert tmatch('a', 8) == (False, {})

    assert tmatch('a', 'abc') == (False, {})

    assert tmatch('a', 2.3) == (False, {})

    assert tmatch('a', 2+3j) == (False, {})

    assert tmatch('a', 'a') == (True, {})

    assert tmatch(2, 2) == (True, {})

    assert tmatch(2.3, 2.3) == (True, {})


def test_tmatch_tuples():
    """ tuples in tmatch """
    # -- tuples

    assert tmatch(('?a', '?b'), (1, 2)) == (True, {'?a': 1, '?b': 2})

    assert tmatch((1, 2), (1, 2)) == (True, {})

    assert tmatch(('?a', '?b', '?c'), (1, 2)) == (False, {})

    assert tmatch(('?a', '?b', '?c'), (1, 2, 3, 4)) == (False, {})


def test_tmatch_list():
    # -- lists
    assert tmatch(['?a', '?b'], [1 , 2]) == (True, {'?a': 1, '?b': 2})

    assert tmatch(['?head', '|tail'], [1, 2]) \
        == (True, {'?head': 1, '|tail': [2]})

    assert tmatch(['?head', '|tail'], [1, 2, 3]) \
        == (True, {'?head': 1, '|tail': [2, 3]})

    assert tmatch(['?head', '|tail'], [1, 2, 3, 4, 5, 6, 7])\
        == (True, {'?head': 1, '|tail': [2, 3, 4, 5, 6, 7]})

def test_tmatch_dict():
    assert tmatch({'a' : 'b'}, {'a' : 'b'}) == (True,{})


    assert tmatch({'a' : '?a'}, {'a' : 'b'}) == (True, {'?a': 'b'})


    assert tmatch({'a' : '?a', 'b' : '?b'},
                  {'a' : 'b', 'b': 1}) == (True, {'?b': 1, '?a': 'b'})

    assert tmatch({'?a' : 'b', '?b' : 1}, {'a' : 'b', 'b': 1}) \
        == (True, {'?b': 'b', '?a': 'a'})


class AlgebraicType(type):
    def __new__(cls, name, bases, attrs):
        try:
            structure = cls.__structure__

            for s in structure:
                attrs[s] = None
        except AttributeError:
            pass

        tp = super(AlgebraicType, cls).__new__(cls, name, bases, attrs)

        return tp

class Algebraic(object):
    __metaclass__ = AlgebraicType

    def __init__(self, *args, **kwargs):
        for s, a in zip(self.__structure__, args):
            setattr(self, s, a)

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __iter__(self):
        return (getattr(self, k) for k in self.__structure__)

    def __str__(self):
        return "%s%s" % (type(self).__name__, tuple(self))

    def __repr__(self):
        return "%s.%s%s" % (self.__module__, type(self).__name__, repr(tuple(self)))

    def __eq__(self, other):
        return   type(self) == type(other)\
            and  tuple(self) == tuple(other)


class Point(Algebraic):
    __structure__ = ('x', 'y')


def test_tmatch_object():
    assert tmatch(Point("?x", 2), Point(1,2)) == (True, {'?x': 1})

def test_tmatch_complex():
    l = [Point(1,2), Point(3,4), Point(4,5)]

    assert Point(1,2) == Point(1,2)


    print tmatch(['?x', Point(3,4), "|r"], l)
    assert tmatch(['?x', Point(3,4), "|r"], l) == \
        (True, {'|r' : [Point(4,5)], '?x' : Point(1,2)})


nose.main()
