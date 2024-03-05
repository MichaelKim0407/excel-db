import typing
from datetime import datetime, date

from .basic_types import BaseTypedColumn


class BaseDateTimeColumn(BaseTypedColumn):
    format: str | typing.Sequence[str]  # must be set in kwargs, unless you are certain there are no strings
    datetime_types = (datetime, date)

    def _strptime(self, value: str) -> datetime:
        if isinstance(self.format, str):
            return datetime.strptime(value, self.format)

        for fmt in self.format:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass

        raise ValueError(f"Cannot parse '{value}' with any of the given time formats.")

    @staticmethod
    def convert_datetime_type(value):
        raise NotImplementedError  # pragma: no cover

    def _convert_from_python(self, value) -> datetime:  # always store into Excel as datetime
        if isinstance(value, self.datetime_types):
            return DateTimeColumn.convert_datetime_type(value)

        if isinstance(value, str) and hasattr(self, 'format'):
            return self._strptime(value)

        raise ValueError(f'Column {self.name} cannot convert value {value} of type {type(value)}')

    def _convert_to_python(self, raw):
        if isinstance(raw, self.datetime_types):
            return self.convert_datetime_type(raw)

        if isinstance(raw, str) and hasattr(self, 'format'):
            return self.convert_datetime_type(self._strptime(raw))

        raise ValueError(f'Column {self.name} cannot convert value {raw} of type {type(raw)}')


class DateTimeColumn(BaseDateTimeColumn):
    @staticmethod
    def convert_datetime_type(value) -> datetime:
        if isinstance(value, datetime):
            return value

        if isinstance(value, date):
            return datetime(year=value.year, month=value.month, day=value.day)

        raise ValueError(value)


class DateColumn(BaseDateTimeColumn):
    @staticmethod
    def convert_datetime_type(value) -> date:
        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        raise ValueError(value)
