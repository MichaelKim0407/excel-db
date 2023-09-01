import pytest

from excel_models.columns.basic_types import StringColumn
from excel_models.columns.collection_types import ArrayColumn
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel(
        'users',
        'name',
        'John\nDoe',
        None,
        'Bob, C.',
        1.5,
        ',,x',
    )


class User(ExcelModel):
    name = ArrayColumn(inner=StringColumn())
    name2 = ArrayColumn(
        alias=name,
        delimiter=',',
        strip=True,
        skip_empty=True,
        omit_none=True,
        empty_as_none=False,
    )


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_get(db):
    assert db.users.name[:] == [
        ('John', 'Doe'),
        None,
        ('Bob, C.',),
        ('1.5',),
        (',,x',),
    ]


def test_set(db):
    db.users[1].name = ('Chris',)
    assert db.users.cell(3, 1).value == 'Chris'


def test_options(db):
    assert db.users.name2[:] == [
        ('John\nDoe',),  # delimiter=','
        (),  # empty_as_none=False
        ('Bob', 'C.'),  # delimiter=',', strip=True
        (1.5,),  # inner use default
        ('x',),  # skip_empty=True
    ]
