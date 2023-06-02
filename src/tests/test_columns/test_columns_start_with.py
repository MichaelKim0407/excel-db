import pytest

from excel_models.column_inst.map import ExcelColumnMap
from excel_models.columns.basic_types import IntColumn
from excel_models.columns.multi import ColumnsStartWith
from excel_models.db import ExcelDB
from excel_models.exceptions import DuplicateColumn
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('numbers', ['number', 'number2', 'number3'], [1, 2, 3], [4, 5, '6'], ['7', 8, 9])


class Numbers(ExcelModel):
    numbers = ColumnsStartWith(name='number', inner=IntColumn(), create_keys=('1', '2', '3'))

    @property
    def sum(self) -> int:
        return sum(self.numbers.values())


class MyDB(ExcelDB):
    numbers = Numbers.as_table()
    numbers2 = Numbers.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_read(db):
    column = db.numbers.numbers
    assert isinstance(column, ExcelColumnMap)
    assert column.col_map == {'': 1, '2': 2, '3': 3}

    n0 = db.numbers[0]
    assert n0.numbers == {'': 1, '2': 2, '3': 3}
    assert n0.sum == 6

    n1 = db.numbers[1]
    assert n1.numbers == {'': 4, '2': 5, '3': 6}
    assert n1.sum == 15

    n2 = db.numbers[2]
    assert n2.numbers == {'': 7, '2': 8, '3': 9}
    assert n2.sum == 24


def test_write(db):
    column = db.numbers2.numbers
    assert isinstance(column, ExcelColumnMap)
    assert column.col_map == {'1': 1, '2': 2, '3': 3}
    assert db.numbers2.cell(1, 1).value == 'number1'
    assert db.numbers2.cell(1, 2).value == 'number2'
    assert db.numbers2.cell(1, 3).value == 'number3'

    new = db.numbers2.new()
    new.numbers = {'1': 1, '2': 2, '3': 3}
    assert db.numbers2.cell(2, 1).value == 1
    assert db.numbers2.cell(2, 2).value == 2
    assert db.numbers2.cell(2, 3).value == 3


def test_duplicate_columns(lazy_init_excel):
    excel = lazy_init_excel('numbers', ['number1', 'number1', 'number3'], [1, 2, 3], [4, 5, '6'], ['7', 8, 9])
    db = MyDB(excel)
    with pytest.raises(DuplicateColumn) as ex:
        _ = db.numbers
    assert 'numbers[1]' in str(ex.value)
