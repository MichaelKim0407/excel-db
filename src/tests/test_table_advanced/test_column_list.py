import pytest

from excel_models.columns import Column, ExcelColumn
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


def test_column_list(db):
    assert len(db.users.columns) == 2
    for column in db.users.columns:
        assert isinstance(column, ExcelColumn)
        assert isinstance(column.column_def, Column)
