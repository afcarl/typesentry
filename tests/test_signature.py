#!/usr/bin/env python
# Copyright 2017 H2O.ai; Apache License Version 2.0;  -*- encoding: utf-8 -*-
import pytest
import time
from tests import typed, TypeError


def test_func_0args0kws():
    @typed()
    def foo():
        return True

    assert foo()

    with pytest.raises(TypeError) as e:
        foo(1)
    assert str(e.value) == "`foo()` doesn't take any arguments"

    with pytest.raises(TypeError) as e:
        foo(1, 2, 3)
    assert str(e.value) == "`foo()` doesn't take any arguments"

    with pytest.raises(TypeError) as e:
        foo(w=1)
    assert str(e.value) == "`foo()` got an unexpected keyword argument `w`"

    with pytest.raises(TypeError) as e:
        foo(1, q=2)
    assert str(e.value) == "`foo()` doesn't take any arguments"



def test_method_noargs():
    class Foo(object):
        @typed()
        def bar(self):
            return True

    foo = Foo()
    assert foo.bar()

    with pytest.raises(TypeError) as e:
        foo.bar(1)
    assert str(e.value) == "`bar()` doesn't take any arguments"

    with pytest.raises(TypeError) as e:
        foo.bar(ww=1)
    assert str(e.value) == "`bar()` got an unexpected keyword argument `ww`"




def test_func_1arg0kws():
    @typed(x=int)
    def foo(x):
        return True

    assert foo(1)
    assert foo(x=15)

    with pytest.raises(TypeError) as e:
        foo()
    assert str(e.value) == "`foo()` missing 1 required positional argument `x`"

    with pytest.raises(TypeError) as e:
        foo(1, 2, 3)
    assert str(e.value) == "`foo()` takes 1 positional argument but 3 were " \
                           "given"

    with pytest.raises(TypeError) as e:
        foo("bar")
    assert str(e.value) == "Incorrect type for argument `x`: expected " \
                           "integer got string"

    with pytest.raises(TypeError) as e:
        foo(1, x=2)
    assert str(e.value) == "`foo()` got multiple values for argument `x`"



def test_func_3args0kws():
    @typed(x=int, y=float, z=str)
    def foo(x, y, z):
        return "%d %.3f %s" % (x, y, z)

    assert foo(1, 2, "bar")
    assert foo(z="reverse", x=7, y=0.001)

    with pytest.raises(TypeError) as e:
        foo()
    assert str(e.value) == "`foo()` missing 3 required positional arguments: "\
                           "`x`, `y` and `z`"

    with pytest.raises(TypeError) as e:
        foo(y=0)
    assert str(e.value) == "`foo()` missing 2 required positional arguments: "\
                           "`x` and `z`"

    with pytest.raises(TypeError) as e:
        foo(x=[3], y=4, z="")
    assert str(e.value) == "Incorrect type for argument `x`: expected integer "\
                           "got list"


def test_func_varargs():
    @typed(args=int)
    def foo(*args):
        return sum(args)

    assert foo() == 0
    assert foo(1) == 1
    assert foo(1, 2, 3, 4, 5) == 15

    with pytest.raises(TypeError) as e:
        foo(1, 3, "bar")
    assert str(e.value) == "Incorrect type for argument `*args`: expected " \
                           "integer got string"


def test_func_varkws():
    @typed(kws=float)
    def foo(**kws):
        return sum(kws.values())

    assert foo() == 0
    assert foo(x=1) == 1
    assert foo(x=1, y=3.3, z=0.7) == 5

    with pytest.raises(TypeError) as e:
        foo(x=1, xx=3, xxx="bar")
    assert str(e.value) == "Incorrect type for argument `xxx`: expected " \
                           "numeric got string"

    with pytest.raises(TypeError) as e:
        foo(1, 2, x=10)
    assert str(e.value) == "`foo()` accepts only keyword arguments"


def test_return_value():
    @typed(_return=float)
    def foo():
        return time.time()

    @typed(_return=int)
    def bar(x):
        return x

    assert foo() > 0
    assert bar(1) == 1

    with pytest.raises(TypeError) as e:
        bar("test")
    assert str(e.value) == "Incorrect return type in `bar()`: " \
                           "expected integer got string"



def test_kwless():
    @typed(_kwless=0)
    def foo(x, y):
        return (x, y)

    @typed(_kwless=1)
    def bar(x, y):
        return (x, y)

    assert foo(x=1, y=2)
    assert foo(y="spam", x="ham")
    assert bar(x=3, y=4)
    assert bar(3, y=7)

    with pytest.raises(TypeError) as e:
        foo(1, 2)
    assert str(e.value) == "`foo()` accepts only keyword arguments"

    with pytest.raises(TypeError) as e:
        foo(1, y=2)
    assert str(e.value) == "`foo()` accepts only keyword arguments"

    with pytest.raises(TypeError) as e:
        bar(1, x=2)
    assert str(e.value) == "`bar()` missing 1 required positional argument `y`"

    with pytest.raises(TypeError) as e:
        bar(1, smth=2)
    assert str(e.value) == "`bar()` missing 1 required positional argument `y`"

    with pytest.raises(TypeError) as e:
        bar(1, 2)
    assert str(e.value) == "`bar()` takes 1 positional argument but 2 " \
                           "were given"




def test_bad_declaration():
    with pytest.raises(AssertionError):
        @typed(z=int)
        def foo1():
            pass

    with pytest.raises(AssertionError):
        @typed(_kwless=1)
        def foo2():
            pass