import typing

from returns import returns

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
