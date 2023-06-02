import pytest

from excel_models.columns import Column
from excel_models.db import ExcelDB
from excel_models.exceptions import OverlapColumn
from excel_models.models import ExcelModel


class User(ExcelModel):
    id = Column()
    name = Column()
    name2 = Column(name='name')


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(tmp_excel_file):
    return MyDB(tmp_excel_file)


def test_overlap(db):
    with pytest.raises(OverlapColumn) as ex:
        _ = db.users
    assert ': name, name2' in str(ex.value)
