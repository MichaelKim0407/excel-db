import pytest

from excel_db.columns.basic_types import IntColumn
from excel_db.db import ExcelDB
from excel_db.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'id', 1, '2', 3, 4.0, 5.1, 'x')


class User(ExcelModel):
    id = IntColumn()


class MyDB(ExcelDB):
    users = User.as_table()


class TestIntColumn:
    @pytest.fixture()
    def db(self, excel):
        return MyDB(excel)

    def test_get(self, db):
        assert db.users.id[:4] == [1, 2, 3, 4]

    def test_get_error(self, db):
        with pytest.raises(ValueError):
            _ = db.users[4].id
        with pytest.raises(ValueError):
            _ = db.users.id[5]

    def test_set(self, db):
        db.users.id[4:] = (5.0, '6')
        assert db.wb['users'].cell(6, 1).value == 5
        assert db.wb['users'].cell(7, 1).value == 6


class User2(ExcelModel):
    id = IntColumn(float_strict=False)


class MyDB2(ExcelDB):
    users = User2.as_table()


class TestNonStrictFloat:
    @pytest.fixture()
    def db(self, excel):
        return MyDB2(excel)

    def test(self, db):
        assert db.users.id[4] == 5
