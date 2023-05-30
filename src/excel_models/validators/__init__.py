import typing

from openpyxl.cell import Cell

from ..typing import TModel, ColumnValue

TValidator = typing.Callable[[TModel, ColumnValue, Cell], None]


class AbstractValidator:
    def __call__(self, row: TModel, value: ColumnValue, cell: Cell) -> None:
        raise NotImplementedError  # pragma: no cover


class AbstractValueValidator(AbstractValidator):

    def _validate(self, value: ColumnValue) -> None:
        raise NotImplementedError  # pragma: no cover

    def __call__(self, row: TModel, value: ColumnValue, cell: Cell) -> None:
        self._validate(value)
