import pytest

from excel_models.columns.basic_types import FloatColumn
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'age', 1, 3.1415926, '5.3', 'x')


class User(ExcelModel):
    age = FloatColumn()


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_get(db):
    assert db.users.age[:3] == [1, 3.1415926, 5.3]


def test_error(db):
    with pytest.raises(ValueError):
        _ = db.users[3].age


def test_set(db):
    db.users.age[3] = '10'
    assert db.users.cell(5, 1).value == 10.0
    db.users.age[4] = 9.9
    assert db.users.cell(6, 1).value == 9.9
