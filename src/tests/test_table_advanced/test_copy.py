import pytest

from excel_models.columns import Column
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


class User(ExcelModel):
    id = Column()
    name = Column()


class MyDB(ExcelDB):
    users = User.as_table()
    accounts = User.as_table()


@pytest.fixture()
def db(tmp_excel_file):
    return MyDB(tmp_excel_file)


def test_copy_sheet(db, tmp_excel_data):
    db.accounts = db.users
    assert set(db.wb.sheetnames) == {'users', 'accounts'}
    assert db.accounts.ws.title == 'accounts'
    assert db.accounts.cell(2, 1).value == tmp_excel_data[0][0]


def test_overwrite_existing(db, tmp_excel_data):
    _ = db.accounts
    db.accounts = db.users
    assert set(db.wb.sheetnames) == {'users', 'accounts'}
    assert db.accounts.ws.title == 'accounts'
    assert db.accounts.cell(2, 1).value == tmp_excel_data[0][0]
