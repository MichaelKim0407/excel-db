import typing

from openpyxl.cell import Cell

from excel_models.typing import AbstractColumn, TTable, TColumnDef, ColumnValue


class BaseExcelColumn(AbstractColumn):
    def __init__(
            self,
            table: TTable,
            column_def: TColumnDef,
    ):
        self.table = table
        self.column_def = column_def

    def check(self) -> None:
        pass

    def __eq__(self, other: typing.Self) -> bool:
        if other is None or not isinstance(other, BaseExcelColumn):
            return False

        return (
                self.table == other.table
                and self.column_def == other.column_def
        )

    def __getitem__(self, idx: int | slice) -> ColumnValue | list[ColumnValue]:
        if isinstance(idx, slice):
            return [
                self.column_def.__get__(row)
                for row in self.table[idx]
            ]

        return self.column_def.__get__(self.table[idx])

    def __iter__(self) -> typing.Iterator[ColumnValue]:
        for row in self.table:
            yield self.column_def.__get__(row)

    def __setitem__(self, idx: int | slice, value: ColumnValue) -> None:
        if isinstance(idx, slice):
            for row, v in zip(self.table[idx], value, strict=True):
                self.column_def.__set__(row, v)
            return

        self.column_def.__set__(self.table[idx], value)

    def __delitem__(self, idx: int | slice) -> None:
        if isinstance(idx, slice):
            for row in self.table[idx]:
                self.column_def.__delete__(row)
            return

        self.column_def.__delete__(self.table[idx])

    def cell0(self, idx: int) -> Cell:
        return self.cell(self.table.get_row_num(idx))
