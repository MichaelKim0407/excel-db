import pytest

from excel_models.columns.basic_types import StringColumn
from excel_models.columns.collection_types import ArrayColumn
from excel_models.db import ExcelDB
from excel_models.exceptions import OverlapColumn
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'name', 'John\nDoe', None, 'Bob, C.', 1.5)


class User(ExcelModel):
    name = ArrayColumn(inner=StringColumn())
    name2 = ArrayColumn(name='name', delimiter=',', strip=True)


class User2(ExcelModel):
    name = ArrayColumn(inner=StringColumn())
    name2 = ArrayColumn(alias=name, delimiter=',', strip=True)


class MyDB(ExcelDB):
    users = User.as_table()
    users2 = User2.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_duplicate_column(db):
    with pytest.raises(OverlapColumn):
        _ = db.users


def test_init_table(db):
    _ = db.users2
    assert [cell.value for cell in db.users2.row(1)] == ['name']
