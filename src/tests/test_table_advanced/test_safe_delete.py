import pytest

from excel_models.columns import Column
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


class User(ExcelModel):
    id = Column()
    name = Column()


class MyDB(ExcelDB):
    users = User.as_table()
    users_safe_delete = users.safe_delete
    users_reinit = users.reinit

    users2 = User.as_table()
    users2_safe_delete = users2.safe_delete
    users2_reinit = users2.reinit


@pytest.fixture()
def db(tmp_excel_file):
    return MyDB(tmp_excel_file)


def test_safe_delete_existing(db):
    db.users_safe_delete()
    assert 'users' not in db.wb


def test_safe_delete_not_existing(db):
    db.users2_safe_delete()


def test_reinit_existing(db):
    users = db.users_reinit()
    assert len(users) == 0


def test_reinit_not_existing(db):
    users = db.users2_reinit()
    assert len(users) == 0
