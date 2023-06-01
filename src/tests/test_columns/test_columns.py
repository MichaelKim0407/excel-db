import pytest

from excel_models.column_inst.array import ExcelColumnArray
from excel_models.columns.basic_types import IntColumn
from excel_models.columns.multi import Columns
from excel_models.db import ExcelDB
from excel_models.exceptions import OverlapColumn
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('numbers', ['numbers', 'x', ''], [1, 2, 3], [4, 5, '6'], ['7', 8, 9])


class Numbers(ExcelModel):
    numbers = Columns(inner=IntColumn(), width=3)

    @property
    def sum(self) -> int:
        return sum(self.numbers)


class ErrNumbers(ExcelModel):
    numbers = Columns(inner=IntColumn(), width=3)
    x = IntColumn()


class MyDB(ExcelDB):
    numbers = Numbers.as_table()
    numbers2 = Numbers.as_table()
    err_numbers = ErrNumbers.as_table(name='numbers')


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_read(db):
    column = db.numbers.numbers
    assert isinstance(column, ExcelColumnArray)
    assert column.col_num == 1
    assert column.width == 3

    n0 = db.numbers[0]
    assert n0.numbers == (1, 2, 3)
    assert n0.sum == 6

    n1 = db.numbers[1]
    assert n1.numbers == (4, 5, 6)
    assert n1.sum == 15

    n2 = db.numbers[2]
    assert n2.numbers == (7, 8, 9)
    assert n2.sum == 24


def test_write(db):
    column = db.numbers2.numbers
    assert isinstance(column, ExcelColumnArray)
    assert column.col_num == 1
    assert column.width == 3
    assert db.numbers2.cell(1, 1).value == 'numbers'
    assert db.numbers2.cell(1, 2).value is None
    assert db.numbers2.cell(1, 3).value is None

    new = db.numbers2.new()
    new.numbers = (1, 2, 3)
    assert db.numbers2.cell(2, 1).value == 1
    assert db.numbers2.cell(2, 2).value == 2
    assert db.numbers2.cell(2, 3).value == 3


def test_column_overlap(db):
    with pytest.raises(OverlapColumn):
        _ = db.err_numbers
