from excel_db.utils.class_collector import CollectorMeta, ListCollector, DictCollector


class A(metaclass=CollectorMeta):
    a = ListCollector()
    li = []  # a normal list used as a control


class A2(A):
    pass


A2.a.append(0)
A2.li.append(0)


class B(A2):
    b: DictCollector[str, int] = DictCollector()


B.a.append(1)
B.li.append(1)
B.b['x'] = 1


class C(B):
    a: ListCollector[int] = ListCollector()  # this should override the list and start fresh


C.a.append(100)
C.b['y'] = 2


class D(C, B):
    pass


def test_base():
    assert isinstance(A.a, ListCollector)
    assert A.a == []

    assert A.li == [0, 1]


def test_subclass_extend():
    assert isinstance(A2.a, ListCollector)
    assert A2.a == [0]

    assert A2.li == [0, 1]


def test_further_extend():
    assert isinstance(B.a, ListCollector)
    assert B.a == [0, 1]
    assert isinstance(B.b, DictCollector)
    assert B.b == {'x': 1}

    assert B.li == [0, 1]


def test_override():
    assert isinstance(C.a, ListCollector)
    assert C.a == [100]
    assert isinstance(C.b, DictCollector)
    assert C.b == {'x': 1, 'y': 2}

    assert C.li == [0, 1]


def test_merge():
    assert isinstance(D.a, ListCollector)
    assert D.a == [100, 0, 1]
