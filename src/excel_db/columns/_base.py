import typing
from functools import cached_property

from openpyxl.cell import Cell

from ..models import ExcelModel
from ..utils.descriptors import BasePropertyDescriptor


class Column(BasePropertyDescriptor[ExcelModel]):
    cache: bool = True

    def _add_to_class(self):
        if not hasattr(self.obj_type, 'columns'):
            self.obj_type.columns = []
        self.obj_type.columns.append(self)

    @cached_property
    def _cache_name(self) -> str:
        return f'_v_{self.attr}'

    def _get_col_num(self, row: ExcelModel) -> int:
        return getattr(row.table, self.attr).col_num

    def _get_cell(self, row: ExcelModel) -> Cell:
        return row.table.ws.cell(row.row_num, self._get_col_num(row))

    def _to_python(self, value):
        return value

    def _get_default(self, row: ExcelModel, cell: Cell):
        return self._to_python(cell.value)

    validators = ()

    def _validate(self, row: ExcelModel, value, cell: Cell):
        for validator in self.validators:
            validator(row, value, cell)

    def validator(self, f_validate):
        if isinstance(self.validators, tuple):
            self.validators = list(self.validators)
        self.validators.append(f_validate)
        return self

    _f_handle_error = None

    def _handle_error_default(self, row: ExcelModel, cell: Cell, ex: Exception):
        raise

    @property
    def _handle_error_method(self):
        if self._f_handle_error is None:
            return self._handle_error_default
        else:
            return self._f_handle_error

    def _handle_error(self, row: ExcelModel, cell: Cell, ex: Exception):
        return self._handle_error_method(row, cell, ex)  # noqa: pycharm

    def error_handler(self, f_handle_error):
        self._f_handle_error = f_handle_error
        return self

    def _get_nocache(self, row: ExcelModel):
        cell = self._get_cell(row)
        try:
            value = self._get_method(row, cell)
            self._validate(row, value, cell)
            return value
        except Exception as ex:
            return self._handle_error(row, cell, ex)

    def _get(self, row: ExcelModel):
        if self.cache:
            if self._cache_name not in row.__dict__:
                value = self._get_nocache(row)
                row.__dict__[self._cache_name] = value
            return row.__dict__[self._cache_name]
        else:
            return self._get_nocache(row)

    def _from_python(self, value):
        return value

    def _set_default(self, row: ExcelModel, value, cell: Cell):
        cell.value = self._from_python(value)

    def _set(self, row: ExcelModel, value):
        cell = self._get_cell(row)
        self._validate(row, value, cell)
        self._set_method(row, value, cell)
        if self.cache:
            row.__dict__[self._cache_name] = value

    def _delete_default(self, row: ExcelModel, cell: Cell):
        cell.value = None

    def _delete(self, row: ExcelModel):
        self._delete_method(row, self._get_cell(row))
        if self.cache:
            if self._cache_name in row.__dict__:
                del row.__dict__[self._cache_name]


TColumnDef = typing.TypeVar('TColumnDef', bound=Column)
