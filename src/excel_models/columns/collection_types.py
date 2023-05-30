import json
import typing

from returns import returns

from ._base import Column
from .basic_types import BaseTypedColumn


class ArrayColumn(BaseTypedColumn):
    delimiter = '\n'
    strip = False
    inner_column_class = Column

    def __init__(self, *, inner: Column = None, **kwargs):
        super().__init__(**kwargs)
        if inner is None:
            inner = self.inner_column_class()
        self.inner = inner

    def _split(self, value: str) -> list[str]:
        return value.split(self.delimiter)

    def _inner_to_python(self, raw):
        return self.inner._to_python(raw)  # noqa: pycharm

    @returns(tuple)
    def _convert_to_python(self, raw):
        if not isinstance(raw, str):
            yield self._inner_to_python(raw)
            return

        for item in self._split(raw):
            if self.strip:
                item = item.strip()
            yield self._inner_to_python(item)

    def _join(self, value: typing.Iterable[str]) -> str:
        return self.delimiter.join(value)

    def _inner_from_python(self, value):
        return self.inner._from_python(value)  # noqa: pycharm

    def _convert_from_python(self, value):
        return self._join(
            self._inner_from_python(item)
            for item in value
        )


class JsonColumn(BaseTypedColumn):
    def _convert_to_python(self, raw):
        if not isinstance(raw, str):
            return raw

        return json.loads(raw)

    def _convert_from_python(self, value):
        return json.dumps(value)
