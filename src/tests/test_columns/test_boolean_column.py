import pytest

from excel_models.columns.basic_types import BooleanColumn
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'active', True, False, 'Yes', 10)


class User(ExcelModel):
    active = BooleanColumn()
    active2 = BooleanColumn(alias=active, truthy=('yes', 'true'))


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_get(db):
    assert db.users.active[:3] == [True, False, False]


def test_get_error(db):
    with pytest.raises(ValueError):
        _ = db.users[3].active


def test_set(db):
    db.users.active[4] = True
    assert db.users.cell(6, 1).value is True
    db.users.active[5] = False
    assert db.users.cell(7, 1).value is False


def test_truthy_strings(db):
    assert db.users.active2[2] is True
