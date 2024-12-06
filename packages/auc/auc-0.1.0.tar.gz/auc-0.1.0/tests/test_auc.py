import pytest
from auc import Auc


def test_add():
    assert Auc.add(2, 3) == 5
    assert Auc.add(-1, 1) == 0


def test_subtract():
    assert Auc.subtract(5, 3) == 2
    assert Auc.subtract(1, 1) == 0


def test_multiply():
    assert Auc.multiply(2, 3) == 6
    assert Auc.multiply(-2, 3) == -6


def test_divide():
    assert Auc.divide(6, 2) == 3
    assert Auc.divide(5, 2) == 2.5
    with pytest.raises(ValueError):
        Auc.divide(1, 0)
