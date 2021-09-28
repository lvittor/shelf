from shelf.main import foo


def test_foo():
    assert foo(1) == 1
    assert foo(2) == 2
    assert foo(3) == 3
