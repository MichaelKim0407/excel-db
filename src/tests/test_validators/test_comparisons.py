import pytest

from excel_models.columns.basic_types import FloatColumn
from excel_models.db import ExcelDB
from excel_models.exceptions import ValidationError
from excel_models.models import ExcelModel
from excel_models.validators.comparisons import (
    Is, IsNot,
    EqualTo, NotEqualTo,
    GreaterThan, GreaterThanOrEqualTo,
    LessThan, LessThanOrEqualTo,
)


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'age', 1, 3.1415926, '18', 21, 44, None)


class User(ExcelModel):
    age = FloatColumn(validators=(GreaterThan(3), LessThanOrEqualTo(21), NotEqualTo(18)))
    age2 = FloatColumn(alias=age, validators=(IsNot(None),))
    age3 = FloatColumn(alias=age)

    @age3.validator
    def age3(self, value, cell):
        try:
            LessThan(3)(self, value, cell)
            return
        except ValidationError:
            pass
        try:
            GreaterThanOrEqualTo(21)(self, value, cell)
            return
        except ValidationError:
            pass
        try:
            EqualTo(18)(self, value, cell)
            return
        except ValidationError:
            pass
        try:
            Is(None)(self, value, cell)
            return
        except ValidationError:
            pass
        raise ValidationError(value)


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_get(db):
    with pytest.raises(ValidationError):
        _ = db.users[0].age
    assert db.users[0].age2 == 1
    assert db.users[0].age3 == 1

    assert db.users[1].age == 3.1415926
    with pytest.raises(ValidationError):
        _ = db.users[1].age3

    with pytest.raises(ValidationError):
        _ = db.users[2].age
    assert db.users[2].age3 == 18

    assert db.users[3].age == 21
    assert db.users[3].age3 == 21

    with pytest.raises(ValidationError):
        _ = db.users[4].age
    assert db.users[4].age3 == 44

    assert db.users[5].age is None
    with pytest.raises(ValidationError):
        _ = db.users[5].age2
    assert db.users[5].age is None
