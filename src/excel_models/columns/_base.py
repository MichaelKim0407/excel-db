import typing

from openpyxl.cell import Cell

from ..typing import AbstractColumnDefinition, TModel
from ..utils.descriptors import BasePropertyDescriptor


class Column(
    BasePropertyDescriptor[TModel],
    AbstractColumnDefinition,
):
    cache: bool = True

    def _add_to_class(self):
        self.obj_type.columns.append(self)

    def _get_col_num(self, row: TModel) -> int:
        return getattr(row.table, self.attr).col_num

    def _get_cell(self, row: TModel) -> Cell:
        return row.cell(self._get_col_num(row))

    def _to_python(self, value):
        return value

    def _get_default(self, row: TModel, cell: Cell):
        return self._to_python(cell.value)

    validators = ()

    def _validate(self, row: TModel, value, cell: Cell):
        for validator in self.validators:
            validator(row, value, cell)

    def validator(self, f_validate):
        if isinstance(self.validators, tuple):
            self.validators = list(self.validators)
        self.validators.append(f_validate)
        return self

    _f_handle_error = None

    def _handle_error_default(self, row: TModel, cell: Cell, ex: Exception):
        raise

    @property
    def _handle_error_method(self) -> typing.Callable:
        if self._f_handle_error is None:
            return self._handle_error_default
        else:
            return self._f_handle_error

    def _handle_error(self, row: TModel, cell: Cell, ex: Exception):
        return self._handle_error_method(row, cell, ex)

    def error_handler(self, f_handle_error):
        self._f_handle_error = f_handle_error
        return self

    def _get_nocache(self, row: TModel):
        cell = self._get_cell(row)
        try:
            value = self._get_method(row, cell)
            self._validate(row, value, cell)
            return value
        except Exception as ex:
            return self._handle_error(row, cell, ex)

    def _get(self, row: TModel):
        if self.cache:
            if self.attr not in row.values_cache:
                value = self._get_nocache(row)
                row.values_cache[self.attr] = value
            return row.values_cache[self.attr]
        else:
            return self._get_nocache(row)

    def _from_python(self, value):
        return value

    def _set_default(self, row: TModel, value, cell: Cell):
        cell.value = self._from_python(value)

    def _set(self, row: TModel, value):
        cell = self._get_cell(row)
        self._validate(row, value, cell)
        self._set_method(row, value, cell)
        if self.cache:
            row.values_cache[self.attr] = value

    def _delete_default(self, row: TModel, cell: Cell):
        cell.value = None

    def _delete(self, row: TModel):
        self._delete_method(row, self._get_cell(row))
        if self.cache:
            if self.attr in row.values_cache:
                del row.values_cache[self.attr]
