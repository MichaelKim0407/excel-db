import pytest

from excel_db.columns import Column
from excel_db.db import ExcelDB
from excel_db.exceptions import ColumnNotFound
from excel_db.models import ExcelModel


class User(ExcelModel):
    id = Column()
    name1 = Column()


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(tmp_excel_file):
    return MyDB(tmp_excel_file)


def test_wrong_attr(db):
    with pytest.raises(AttributeError):
        _ = db.users.name2


def test_wrong_col_name(db):
    with pytest.raises(ColumnNotFound):
        _ = db.users.name1
