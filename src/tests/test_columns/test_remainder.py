import pytest

from excel_models.column_inst.remainder import ExcelColumnRemainder
from excel_models.columns.basic_types import StringColumn
from excel_models.columns.multi import Remainder
from excel_models.db import ExcelDB
from excel_models.exceptions import OverlapColumn
from excel_models.models import ExcelModel
from excel_models.tables import ExcelTable


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('logs', ['message'], ['hello', 'world'], [], ['foo', 'bar', 'x'])


class LogEntryTable(ExcelTable):
    def log(self, *message):
        self.new().message = message


class LogEntry(ExcelModel):
    message = Remainder(inner=StringColumn())


class ErrLogEntry(ExcelModel):
    message = Remainder(inner=StringColumn())
    info = StringColumn()


class MyDB(ExcelDB):
    logs = LogEntry.as_table()
    logs2 = LogEntry.as_table(table_class=LogEntryTable)
    err = ErrLogEntry.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_read(db):
    column = db.logs.message
    assert isinstance(column, ExcelColumnRemainder)
    assert column.col_num == 1

    l0 = db.logs[0]
    assert l0.message == ('hello', 'world')

    l1 = db.logs[1]
    assert l1.message == ()

    l2 = db.logs[2]
    assert l2.message == ('foo', 'bar', 'x')


def test_write(db):
    column = db.logs2.message
    assert isinstance(column, ExcelColumnRemainder)
    assert column.col_num == 1
    assert db.logs2.max_col == 1
    assert db.logs2.cell(1, 1).value == 'message'

    db.logs2.log('hello', 'world')
    assert db.logs2.max_col == 2
    assert db.logs2.cell(2, 1).value == 'hello'
    assert db.logs2.cell(2, 2).value == 'world'


def test_column_overlap(db):
    with pytest.raises(OverlapColumn):
        _ = db.err
