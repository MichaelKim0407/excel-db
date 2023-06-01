import pytest

from excel_models.columns import Column
from excel_models.db import ExcelDB
from excel_models.exceptions import DuplicateColumn
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', ['id', 'name', 'name'])


class User(ExcelModel):
    id = Column()
    name = Column()


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_duplicate(db):
    with pytest.raises(DuplicateColumn) as ex:
        _ = db.users
    assert 'name' in str(ex.value)
