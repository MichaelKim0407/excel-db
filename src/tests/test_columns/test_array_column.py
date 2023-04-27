import pytest

from excel_db.columns.basic_types import StringColumn
from excel_db.columns.collection_types import ArrayColumn
from excel_db.db import ExcelDB
from excel_db.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'name', 'John\nDoe', None, 'Bob', 1.5)


class User(ExcelModel):
    name = ArrayColumn(inner=StringColumn())


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_get(db):
    assert db.users.name[:] == [('John', 'Doe'), None, ('Bob',), ('1.5',)]


def test_set(db):
    db.users[1].name = ('Chris',)
    assert db.wb['users'].cell(3, 1).value == 'Chris'
