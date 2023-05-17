import pytest

from excel_models.columns import Column
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


class User(ExcelModel):
    id = Column()
    name = Column()


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(tmp_excel_file):
    return MyDB(tmp_excel_file)


def test_delete_sheet(db):
    del db.users
    assert set(db.wb.sheetnames) == set()
    _ = db.users
    assert db.wb['users'].max_row == 1
