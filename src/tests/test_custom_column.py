import pytest

from excel_models.columns import Column
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'name', 'John\nDoe', None, 'Bob', 1.5)


class User(ExcelModel):
    @Column()
    def name(self):
        raw = self.raw_name
        if raw is None or raw == '':
            return []
        return raw.split('\n')

    raw_name = name.raw_value_accessor

    @name.setter
    def name(self, value):
        if not value:
            self.raw_name = ''
            return
        self.raw_name = '\n'.join(value)

    @name.deleter
    def name(self):
        self.raw_name = ''

    @name.error_handler  # noqa: pycharm
    def name(self, ex: Exception):
        return [str(self.raw_name)]


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_get(db):
    assert db.users.name[:] == [['John', 'Doe'], [], ['Bob'], ['1.5']]


def test_set(db):
    db.users[1].name = ['Chris']
    assert db.users.cell(3, 1).value == 'Chris'


def test_del(db):
    del db.users[2].name
    assert db.users.cell(4, 1).value == ''
