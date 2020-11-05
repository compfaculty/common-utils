import pytest

from data_structures import ListAttr


def test_list_with_attributes():
    l = ListAttr()
    l.append(100)
    l.a = 4
    assert len(l) == 1
    assert l.a == 4
    l.order = 'reversed'
    assert l.order == 'reversed'
    l.append(1)
    assert len(l) == 2
    assert l[0] == 100
    assert l[1] == 1
    assert l.pop() == 1
    assert l.pop() == 100
    assert len(l) == 0


