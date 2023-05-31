import pytest

from excel_models.columns.basic_types import StringColumn
from excel_models.db import ExcelDB
from excel_models.exceptions import ValidationError
from excel_models.models import ExcelModel
from excel_models.validators.comparisons import required


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'name', 'John', 'William', None, 3.1415926)


class User(ExcelModel):
    name = StringColumn(validators=(required,))

    @name.validator
    def name(self, value: str):
        if not value[0].isalpha():
            raise ValidationError(value)


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_no_error(db):
    assert db.users.name[:2] == ['John', 'William']


def test_error(db):
    with pytest.raises(ValidationError):
        _ = db.users[2].name
    with pytest.raises(ValidationError):
        _ = db.users[3].name


def test_set(db):
    with pytest.raises(ValidationError):
        db.users[0].name = '0'
