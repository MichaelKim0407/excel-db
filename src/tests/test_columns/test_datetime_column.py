from datetime import datetime, date

import pytest

from excel_models.columns.datetime import DateTimeColumn, DateColumn
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


@pytest.fixture()
def excel(lazy_init_excel):
    return lazy_init_excel('users', 'last_login', '2023/1/1', datetime(2023, 2, 1), '?????', '1/1/23')


class User(ExcelModel):
    last_login = DateTimeColumn(format='%Y/%m/%d')
    last_login2 = DateTimeColumn(alias=last_login)
    last_login3 = DateTimeColumn(alias=last_login, format=('%Y/%m/%d', '%m/%d/%y'))
    last_login4 = DateColumn(alias=last_login, format=('%Y/%m/%d', '%m/%d/%y'))


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(excel):
    return MyDB(excel)


def test_get(db):
    assert db.users.last_login[:2] == [datetime(2023, 1, 1), datetime(2023, 2, 1)]


def test_error(db):
    with pytest.raises(ValueError):
        _ = db.users[2].last_login


def test_set(db):
    now = datetime.now()
    db.users[3].last_login = now
    assert db.users.cell(5, 1).value == now
    db.users[4].last_login = '2023/4/1'
    assert db.users.cell(6, 1).value == datetime(2023, 4, 1)


def test_format_not_provided(db):
    with pytest.raises(ValueError):
        _ = db.users[0].last_login2


def test_multiple_formats(db):
    assert db.users.last_login3[:2] == [datetime(2023, 1, 1), datetime(2023, 2, 1)]
    with pytest.raises(ValueError):
        _ = db.users.last_login3[2]
    assert db.users.last_login3[3] == datetime(2023, 1, 1)

    with pytest.raises(ValueError):
        _ = db.users.last_login[3]


def test_date_get(db):
    assert db.users.last_login4[:2] == [date(2023, 1, 1), date(2023, 2, 1)]
    with pytest.raises(ValueError):
        _ = db.users.last_login4[2]
    assert db.users.last_login4[3] == date(2023, 1, 1)


def test_date_set(db):
    today = date.today()
    db.users[3].last_login4 = today
    assert isinstance(db.users.cell(5, 1).value, datetime)
    assert db.users.cell(5, 1).value == datetime(today.year, today.month, today.day)
