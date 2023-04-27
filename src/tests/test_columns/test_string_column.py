import pytest

from excel_db.columns.basic_types import StringColumn
from excel_db.db import ExcelDB
from excel_db.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'name', 'John', 'William', None, 3.1415926)


class User(ExcelModel):
    name = StringColumn()


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_get(db):
    assert db.users.name[:] == ['John', 'William', None, '3.1415926']


def test_set(db):
    db.users.name[3] = 'Chris'
    assert db.wb['users'].cell(5, 1).value == 'Chris'
    db.users.name[4] = 10
    assert db.wb['users'].cell(6, 1).value == '10'
    db.users.name[0] = None
    assert db.wb['users'].cell(2, 1).value is None
