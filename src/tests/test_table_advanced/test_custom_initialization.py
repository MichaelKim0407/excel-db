from excel_models.columns import Column
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel
from excel_models.tables import ExcelTable


class User(ExcelModel):
    id = Column()
    name = Column()


class MyDB(ExcelDB):
    users = User.as_table(title_row=2)

    @users.initializer
    def users(self, table: ExcelTable):
        table.ws.cell(1, 1, 'hello world')


def test_custom_init(tmp_path):
    tmp_excel_file = str(tmp_path / 'db.xlsx')
    db = MyDB(tmp_excel_file)
    _ = db.users
    assert db.wb['users'].cell(1, 1).value == 'hello world'
    assert db.wb['users'].cell(2, 1).value == 'id'
    assert db.wb['users'].cell(2, 2).value == 'name'
