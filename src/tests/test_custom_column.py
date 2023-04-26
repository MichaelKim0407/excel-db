import pytest
from openpyxl.cell import Cell

from excel_db.columns import Column
from excel_db.db import ExcelDB
from excel_db.models import ExcelModel


class User(ExcelModel):
    id = Column()

    @Column()
    def name(self, cell: Cell):
        if cell.value is None or cell.value == '':
            return []
        return cell.value.split('\n')

    @name.setter
    def name(self, value, cell: Cell):
        if not value:
            cell.value = ''
            return
        cell.value = '\n'.join(value)

    @name.deleter
    def name(self, cell: Cell):
        cell.value = ''


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(tmp_excel_file):
    return MyDB(tmp_excel_file)


def test_get(db, tmp_excel_data):
    assert db.users[0].name == [tmp_excel_data[0][1]]


def test_set(db):
    db.users[1].name = ['Chris']
    assert db.wb['users'].cell(3, 2).value == 'Chris'


def test_del(db):
    del db.users[2].name
    assert db.wb['users'].cell(4, 2).value == ''
