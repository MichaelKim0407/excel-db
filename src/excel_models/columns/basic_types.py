import typing
from datetime import datetime

from excel_models.typing import CellValue, ColumnValue, TModel
from ._std import Column


class BaseTypedColumn(Column):
    def _convert_to_python(self, raw: CellValue) -> ColumnValue:
        raise NotImplementedError  # pragma: no cover

    def to_python(self, row: TModel, raw: CellValue) -> ColumnValue:
        if raw is None:
            return None
        return self._convert_to_python(raw)

    def _convert_from_python(self, value: ColumnValue) -> CellValue:
        raise NotImplementedError  # pragma: no cover

    def from_python(self, row: TModel, value: ColumnValue) -> CellValue:
        if value is None:
            return None
        return self._convert_from_python(value)


class BaseSimpleTypeColumn(BaseTypedColumn):
    def _convert(self, value: CellValue | ColumnValue) -> ColumnValue | CellValue:
        raise NotImplementedError  # pragma: no cover

    def _convert_to_python(self, raw: CellValue) -> ColumnValue:
        return self._convert(raw)

    def _convert_from_python(self, value: ColumnValue) -> CellValue:
        return self._convert(value)


class StringColumn(BaseSimpleTypeColumn):
    _convert = str


class IntColumn(BaseSimpleTypeColumn):
    float_strict: bool = True

    def _convert(self, value) -> int:
        if isinstance(value, int):
            return value

        if isinstance(value, float):
            value_int = int(value)
            if value_int != value and self.float_strict:
                raise ValueError(value)
            return value_int

        return int(value)


class FloatColumn(BaseSimpleTypeColumn):
    _convert = float


class DateTimeColumn(BaseSimpleTypeColumn):
    format: str | typing.Sequence[str]  # must be set in kwargs, unless you are certain there are no strings

    def _strptime(self, value):
        if isinstance(self.format, str):
            return datetime.strptime(value, self.format)

        for fmt in self.format:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass

        raise ValueError(f"Cannot parse '{value}' with any of the given time formats.")

    def _convert(self, value) -> datetime:
        if isinstance(value, datetime):
            return value

        if isinstance(value, str) and hasattr(self, 'format'):
            return self._strptime(value)

        raise ValueError(value)
