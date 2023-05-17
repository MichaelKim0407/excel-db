import json

import pytest

from excel_db.columns.collection_types import JsonColumn
from excel_db.db import ExcelDB
from excel_db.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'data', None, 1, json.dumps([1, 3]), json.dumps({'x': 5}))


class User(ExcelModel):
    data = JsonColumn()


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_get(db):
    assert db.users.data[:] == [None, 1, [1, 3], {'x': 5}]


def test_set(db):
    db.users[0].data = 'hello world'
    assert db.wb['users'].cell(2, 1).value == '"hello world"'
