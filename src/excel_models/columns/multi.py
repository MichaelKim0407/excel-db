import typing

from returns import returns

from excel_models.exceptions import DuplicateColumn
from excel_models.typing import TTable, TColumn
from ._container import BaseContainer


class Columns(BaseContainer):
    width: int

    def __post_init__(self):
        super().__post_init__()
        if self.column_class is None:
            from excel_models.column_inst.array import ExcelColumnArray
            self.column_class = ExcelColumnArray

    def match_column(self, table: TTable, col_num: int) -> TColumn | None:
        title = table.get_title(col_num)
        if title != self.name:
            return None

        return self.column_class(table, self, col_num, self.width)

    def init_column(self, table: TTable, col_num: int) -> tuple[TColumn, int]:
        table.set_title(col_num, self.name)
        return self.column_class(table, self, col_num, self.width), self.width

    @returns(tuple)
    def to_python(self, raw: typing.Sequence) -> typing.Sequence:
        for v in raw:
            yield self.inner.to_python(v)

    @returns(tuple)
    def from_python(self, value: typing.Sequence) -> typing.Sequence:
        for v in value:
            yield self.inner.from_python(v)


class ColumnsStartWith(BaseContainer):
    create_keys: typing.Collection[str]

    def __post_init__(self):
        super().__post_init__()
        if self.column_class is None:
            from excel_models.column_inst.map import ExcelColumnMap
            self.column_class = ExcelColumnMap

    def match_column(self, table: TTable, col_num: int) -> TColumn | None:
        title = table.get_title(col_num)
        if not title.startswith(self.name):
            return None

        key = title[len(self.name):]

        if self.attr in table.columns_cache:
            column = table.columns_cache[self.attr]
            if key in column.col_map:
                raise DuplicateColumn(f'Multiple columns matching definition {self.attr}[{key}]')
            column.col_map[key] = col_num
        else:
            return self.column_class(table, self, {key: col_num})

    def init_column(self, table: TTable, col_num: int) -> tuple[TColumn, int]:
        col_map = {
            k: c
            for c, k in enumerate(self.create_keys, start=col_num)
        }
        for k, c in col_map.items():
            table.set_title(c, f'{self.name}{k}')
        return self.column_class(table, self, col_map), len(col_map)

    @returns(dict)
    def to_python(self, raw: typing.Mapping) -> typing.Mapping:
        for k, v in raw.items():
            yield k, self.inner.to_python(v)

    @returns(dict)
    def from_python(self, value: typing.Mapping) -> typing.Mapping:
        for k, v in value.items():
            yield k, self.inner.from_python(v)