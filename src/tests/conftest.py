import pytest
from openpyxl.workbook import Workbook


@pytest.fixture(scope='session')
def tmp_excel_sheet_name():
    return 'users'


@pytest.fixture(scope='session')
def tmp_excel_columns():
    return 'id', 'name'


@pytest.fixture(scope='session')
def tmp_excel_data():
    return (
        ('1', 'John'),
        ('2', 'David'),
        ('3', 'Sarah'),
    )


@pytest.fixture()
def tmp_excel_file(
        tmp_path,
        tmp_excel_sheet_name,
        tmp_excel_columns,
        tmp_excel_data,
):
    path = str(tmp_path / 'db.xlsx')
    wb = Workbook()
    ws = wb.active
    ws.title = tmp_excel_sheet_name
    ws.append(tmp_excel_columns)
    for row in tmp_excel_data:
        ws.append(row)
    wb.save(path)
    return path
