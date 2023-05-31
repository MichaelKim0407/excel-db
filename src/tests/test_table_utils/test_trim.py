import pytest

from excel_models.columns.basic_types import IntColumn
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', ['id', 'name', ''], 1, 2, 3, 4, '', '')


class User(ExcelModel):
    id = IntColumn()


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_trim_cols(db):
    assert db.users.max_col == 3
    assert db.users.max_row == 7
    assert db.users.trim_cols() == 2
    assert db.users.max_col == 2
    assert db.users.max_row == 7


def test_trim_rows(db):
    assert db.users.max_col == 3
    assert db.users.max_row == 7
    assert db.users.trim_rows() == 5
    assert db.users.max_col == 3
    assert db.users.max_row == 5


def test_trim(db):
    assert db.users.max_col == 3
    assert db.users.max_row == 7
    assert db.users.trim() == (2, 5)
    assert db.users.max_col == 2
    assert db.users.max_row == 5
