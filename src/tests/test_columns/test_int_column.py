import pytest

from excel_models.columns.basic_types import IntColumn
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'id', 1, '2', 3, 4.0, 5.1, 'x')


class User(ExcelModel):
    id = IntColumn()
    id2 = IntColumn(name='id', float_strict=False)


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_get(db):
    assert db.users.id[:4] == [1, 2, 3, 4]


def test_get_error(db):
    with pytest.raises(ValueError):
        _ = db.users[4].id
    with pytest.raises(ValueError):
        _ = db.users.id[5]


def test_set(db):
    db.users.id[4:] = (5.0, '6')
    assert db.wb['users'].cell(6, 1).value == 5
    assert db.wb['users'].cell(7, 1).value == 6


def test_non_strict_float(db):
    assert db.users.id2[4] == 5
