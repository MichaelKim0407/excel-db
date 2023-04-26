from openpyxl.cell import Cell

from .utils.descriptors import BasePropertyDescriptor


class Column(BasePropertyDescriptor['ExcelModel']):
    def _add_to_class(self):
        if not hasattr(self.obj_type, 'columns'):
            self.obj_type.columns = []
        self.obj_type.columns.append(self)

    def _get_col_num(self, row: 'ExcelModel') -> int:
        return getattr(row.table, self.attr).col_num

    def _get_cell(self, row: 'ExcelModel') -> Cell:
        return row.table.ws.cell(row.row_num, self._get_col_num(row))

    def _get_default(self, row: 'ExcelModel', cell: Cell):
        return cell.value

    def _get(self, row: 'ExcelModel'):
        return self._get_method(row, self._get_cell(row))

    def _set_default(self, row: 'ExcelModel', value, cell: Cell):
        cell.value = value

    def _set(self, row: 'ExcelModel', value):
        self._set_method(row, value, self._get_cell(row))

    def _delete_default(self, row: 'ExcelModel', cell: Cell):
        cell.value = None

    def _delete(self, row: 'ExcelModel'):
        self._delete_method(row, self._get_cell(row))


class ExcelColumn:
    def __init__(
            self,
            table: 'ExcelTable',
            column_def: Column,
            col_num: int,
    ):
        self.table = table
        self.column_def = column_def
        self.col_num = col_num

    def __getitem__(self, idx: int):
        return self.column_def.__get__(self.table[idx])

    def __setitem__(self, idx: int, value):
        self.column_def.__set__(self.table[idx], value)

    def __delitem__(self, idx: int):
        self.column_def.__delete__(self.table[idx])


from .tables import ExcelTable  # noqa: E402
from .models import ExcelModel  # noqa: E402
