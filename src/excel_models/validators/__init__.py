import typing

from openpyxl.cell import Cell

from ..typing import TModel, CellValue

TValidator = typing.Callable[[TModel, CellValue, Cell], None]


class AbstractValidator:
    def __call__(self, row: TModel, value: CellValue, cell: Cell) -> None:
        raise NotImplementedError  # pragma: no cover


class AbstractValueValidator(AbstractValidator):

    def _validate(self, value: CellValue) -> None:
        raise NotImplementedError  # pragma: no cover

    def __call__(self, row: TModel, value: CellValue, cell: Cell) -> None:
        self._validate(value)
