from excel_db.utils.class_collector import CollectorMeta, ListCollector, DictCollector


class A(metaclass=CollectorMeta):
    a: ListCollector


class A2(A):
    pass


A2.a.append(0)


class B(A2):
    b: DictCollector[str, int]


B.a.append(1)
B.b['x'] = 1


class C(B):
    a: ListCollector[int]  # this should override the list and start fresh


C.a.append(100)
C.b['y'] = 2


class Other(metaclass=CollectorMeta):
    a: list
    b: 'ListCollector'
    none: None


def test_base():
    assert hasattr(A, 'a')
    assert A.a == []


def test_subclass_extend():
    assert hasattr(A2, 'a')
    assert A2.a == [0]


def test_further_extend():
    assert hasattr(B, 'a')
    assert B.a == [0, 1]
    assert hasattr(B, 'b')
    assert B.b == {'x': 1}


def test_override():
    assert hasattr(C, 'a')
    assert C.a == [100]
    assert hasattr(C, 'b')
    assert C.b == {'x': 1, 'y': 2}


def test_other():
    assert not hasattr(Other, 'a')
    assert not hasattr(Other, 'b')
    assert not hasattr(Other, 'none')
