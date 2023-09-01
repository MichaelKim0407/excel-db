import pytest
from openpyxl.workbook import Workbook

from excel_models.columns import Column
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


class User(ExcelModel):
    id = Column()
    name = Column()


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(tmp_path):
    path = str(tmp_path / 'db.xlsx')
    wb = Workbook()
    wb.save(path)
    return MyDB(path)


def test_delete_default(db):
    assert 'Sheet' in db.wb
    db.delete_default()
    assert 'Sheet' not in db.wb
