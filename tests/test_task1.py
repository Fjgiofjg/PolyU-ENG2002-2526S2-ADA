import pytest
from task1 import fixNum


def test_add():
    a = fixNum(12, 48)
    b = fixNum(2, 16)
    r = a.add(b)
    assert r.a == 14 and r.b == 64


def test_mul():
    a = fixNum(12, 48)
    b = fixNum(2, 16)
    r = a.mul(b)
    assert r.a == 26 and r.b == 95


def test_power_zero():
    a = fixNum(12, 48)
    r = a.power(0)
    assert r.a == 1 and r.b == 0


def test_power_negative_integer():
    c = fixNum(2, 16)
    r = c.power(-2)
    # Expected approximately 0.21 when rounded to 2 decimal places
    assert r.a == 0 and r.b == 21
