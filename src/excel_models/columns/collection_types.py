import json
import typing

from returns import returns

from ._container import BaseContainer
from .basic_types import BaseTypedColumn


class ArrayColumn(BaseContainer, BaseTypedColumn):
    delimiter: str = '\n'
    strip: bool = False

    def split(self, value: str) -> list[str]:
        return value.split(self.delimiter)

    @returns(tuple)
    def _convert_to_python(self, raw):
        if not isinstance(raw, str):
            yield self.inner.to_python(raw)
            return

        for item in self.split(raw):
            if self.strip:
                item = item.strip()
            yield self.inner.to_python(item)

    def join(self, value: typing.Iterable[str]) -> str:
        return self.delimiter.join(value)

    def _convert_from_python(self, value):
        return self.join(
            self.inner.from_python(item)
            for item in value
        )


class JsonColumn(BaseTypedColumn):
    def _convert_to_python(self, raw):
        if not isinstance(raw, str):
            return raw

        return json.loads(raw)

    def _convert_from_python(self, value):
        return json.dumps(value)
