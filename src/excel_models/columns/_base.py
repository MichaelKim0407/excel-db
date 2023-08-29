import typing
from functools import cached_property
from inspect import signature

from excel_models.typing import (
    AbstractColumnDefinition,
    TModel, TTable, TColumn,
    CellValue, ColumnValue, ColumnCell, CellContext,
)
from excel_models.utils.descriptors import BasePropertyDescriptor


class BaseColumnDefinition(
    BasePropertyDescriptor[TModel],
    AbstractColumnDefinition,
):
    cache: bool = True
    column_class: typing.Type[TColumn]  # assign in subclass

    def _add_to_class(self):
        super()._add_to_class()
        self.obj_type.column_defs.append(self)

    def get_column(self, table: TTable) -> TColumn:
        return getattr(table, self.attr)

    def get_cell_context(self, row: TModel) -> CellContext:
        column = self.get_column(row.table)
        return CellContext(row, column)

    def cell(self, row: TModel) -> ColumnCell:
        return self.get_column(row.table).cell(row.row_num)

    def to_python(self, raw: CellValue, context: CellContext) -> ColumnValue:
        return raw

    def get_raw(self, row: TModel) -> CellValue:
        return self.get_column(row.table).get_raw(row.row_num)

    def _get_default(self, row: TModel) -> ColumnValue:
        context = self.get_cell_context(row)
        return self.to_python(context.raw, context)

    def _call_method_variable_signature(self, method, row: TModel, value):
        parameters = signature(method).parameters
        match tuple(parameters):
            case 'self', :  # @formatter:off
                return method(row)
            case _, :  # @formatter:off
                return method(value)
            case _, _:
                return method(row, value)
            case _:
                context = self.get_cell_context(row)
                return method(row, value, context)

    validators = ()

    def _validate(self, row: TModel, value: ColumnValue) -> None:
        for validator in self.validators:
            self._call_method_variable_signature(validator, row, value)

    def validator(self, f_validate):
        if isinstance(self.validators, tuple):
            self.validators = list(self.validators)
        self.validators.append(f_validate)
        return self

    _f_handle_error = None

    def _handle_error_default(self, row: TModel, ex: Exception, context: CellContext) -> ColumnValue:
        raise

    @property
    def _handle_error_method(self) -> typing.Callable:
        if self._f_handle_error is None:
            return self._handle_error_default
        else:
            return self._f_handle_error

    def _handle_error(self, row: TModel, ex: Exception) -> ColumnValue:
        return self._call_method_variable_signature(self._handle_error_method, row, ex)

    def error_handler(self, f_handle_error):
        self._f_handle_error = f_handle_error
        return self

    def _get_nocache(self, row: TModel) -> ColumnValue:
        try:
            value = self._get_method(row)
            self._validate(row, value)
            return value
        except Exception as ex:
            return self._handle_error(row, ex)

    def _get(self, row: TModel) -> ColumnValue:
        if self.cache:
            if self.attr not in row.values_cache:
                value = self._get_nocache(row)
                row.values_cache[self.attr] = value
            return row.values_cache[self.attr]
        else:
            return self._get_nocache(row)

    def from_python(self, value: ColumnValue, context: CellContext) -> CellValue:
        return value

    def set_raw(self, row: TModel, raw: CellValue) -> None:
        self.get_column(row.table).set_raw(row.row_num, raw)

    def _set_default(self, row: TModel, value: ColumnValue) -> None:
        context = self.get_cell_context(row)
        context.raw = self.from_python(value, context)

    def _set(self, row: TModel, value: ColumnValue) -> None:
        self._validate(row, value)
        self._set_method(row, value)
        if self.cache:
            row.values_cache[self.attr] = value

    def delete_raw(self, row: TModel) -> None:
        self.get_column(row.table).delete_raw(row.row_num)

    def _delete_default(self, row: TModel):
        self.delete_raw(row)

    def _delete(self, row: TModel):
        self._delete_method(row)
        if self.cache:
            if self.attr in row.values_cache:
                del row.values_cache[self.attr]

    @cached_property
    def cell_accessor(self) -> property:
        return property(self.cell)

    @cached_property
    def raw_value_accessor(self) -> property:
        return property(self.get_raw, self.set_raw, self.delete_raw)
