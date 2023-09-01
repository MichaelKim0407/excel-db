import json
import typing
from dataclasses import dataclass

from returns import returns

from excel_models.typing import CellContext
from ._container import BaseContainer
from ._std import Column
from .basic_types import BaseTypedColumn


class ArrayColumn(BaseContainer, Column):
    delimiter: str = '\n'
    strip: bool = False
    skip_empty: bool = False
    omit_none: bool = False
    empty_as_none: bool = True

    @dataclass
    class InnerContext(BaseContainer.InnerContext):
        index: int

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
            yield self.inner.to_python(raw, self.InnerContext.from_parent(context, index=0))
            return

        for i, item in enumerate(self.split(raw)):
            if self.strip:
                item = item.strip()
            if (not item) and self.skip_empty:
                continue
            v = self.inner.to_python(item, self.InnerContext.from_parent(context, index=i))
            if v is None and self.omit_none:
                continue
            yield v

    def join(self, value: typing.Iterable[str]) -> str:
        return self.delimiter.join(value)

    def from_python(self, value, context: CellContext):
        if not value:
            return None

        return self.join(
            self.inner.from_python(item, self.InnerContext.from_parent(context, index=i))
            for i, item in enumerate(value)
        )


class JsonColumn(BaseTypedColumn):
    def _convert_to_python(self, raw):
        if not isinstance(raw, str):
            return raw

        return json.loads(raw)

    def _convert_from_python(self, value):
        return json.dumps(value)
