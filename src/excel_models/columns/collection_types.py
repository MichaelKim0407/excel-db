import json
import typing

from returns import returns

from excel_models.typing import CellContext
from ._container import BaseContainer
from ._std import Column
from .basic_types import BaseTypedColumn


class ArrayColumn(BaseContainer, Column):
    delimiter: str = '\n'
    strip: bool = False
    empty_as_none: bool = True

    def split(self, value: str) -> list[str]:
        return value.split(self.delimiter)

    def to_python(self, raw, context: CellContext):
        if not raw:
            if self.empty_as_none:
                return None
            else:
                return ()
        return self._to_python(raw, context)

    @returns(tuple)
    def _to_python(self, raw, context: CellContext):
        if not isinstance(raw, str):
            yield self.inner.to_python(raw, context)
            return

        for item in self.split(raw):
            if self.strip:
                item = item.strip()
            yield self.inner.to_python(item, context)

    def join(self, value: typing.Iterable[str]) -> str:
        return self.delimiter.join(value)

    def from_python(self, value, context: CellContext):
        if not value:
            return None

        return self.join(
            self.inner.from_python(item, context)
            for item in value
        )


class JsonColumn(BaseTypedColumn):
    def _convert_to_python(self, raw):
        if not isinstance(raw, str):
            return raw

        return json.loads(raw)

    def _convert_from_python(self, value):
        return json.dumps(value)
