import pytest
from openpyxl.cell import Cell

from excel_models.columns.basic_types import IntColumn, StringColumn
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


class User(ExcelModel):
    id = IntColumn()
    name = StringColumn()

    raw_id = id.raw_value_accessor
    name_cell = name.cell_accessor


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(tmp_excel_file):
    return MyDB(tmp_excel_file)


def test_cell_accessor(db, tmp_excel_data):
    cell = db.users[0].name_cell
    assert isinstance(cell, Cell)
    assert cell.row == 2
    assert cell.column == 2


def test_raw_accessor_get(db, tmp_excel_data):
    raw_id = db.users[0].raw_id
    assert isinstance(raw_id, str)
    assert raw_id == tmp_excel_data[0][0]


def test_raw_accessor_set(db):
    db.users[0].raw_id = 'abc'
    assert db.users.ws.cell(2, 1).value == 'abc'


def test_raw_accessor_del(db):
    del db.users[0].raw_id
    assert db.users.ws.cell(2, 1).value is None
