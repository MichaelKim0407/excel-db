import typing

from excel_models.typing import TModel, ColumnValue

TValidator = typing.Callable[[TModel, ColumnValue], None]


class AbstractValidator:
    def __call__(self, row: TModel, value: ColumnValue) -> None:
        raise NotImplementedError  # pragma: no cover


class AbstractValueValidator(AbstractValidator):

    def _validate(self, value: ColumnValue) -> None:
        raise NotImplementedError  # pragma: no cover

    def __call__(self, row: TModel, value: ColumnValue) -> None:
        self._validate(value)
