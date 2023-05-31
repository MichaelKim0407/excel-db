import typing
from functools import cached_property

from openpyxl.cell import Cell
from openpyxl.utils import get_column_letter

from ._base import BaseExcelColumn
from ..typing import TTable, TColumnDef, CellValue


class ExcelColumn(BaseExcelColumn):
    def __init__(
            self,
            table: TTable,
            column_def: TColumnDef,
            col_num: int,
            *,
            concrete: bool,
    ):
        super().__init__(table, column_def)
        self.col_num = col_num
        self.concrete = concrete

    @cached_property
    def col_letter(self) -> str:
        return get_column_letter(self.col_num)

    @cached_property
    def occupied_col_nums(self) -> list[int]:
        if not self.concrete:
            return []
        return [self.col_num]

    def __eq__(self, other: typing.Self) -> bool:
        if other is None or not isinstance(other, ExcelColumn):
            return False

        return (
                self.table == other.table
                and self.column_def == other.column_def
                and self.col_num == other.col_num
                and self.concrete == other.concrete
        )

    def cell(self, row_num: int) -> Cell:
        return self.table.cell(row_num, self.col_num)

    @property
    def cells(self) -> typing.Sequence[Cell]:
        return self.table.ws[self.col_letter][self.table.get_row_num(-1):]

    def get_raw(self, row_num: int) -> CellValue:
        return self.cell(row_num).value

    def set_raw(self, row_num: int, raw: CellValue) -> None:
        self.cell(row_num).value = raw

    def delete_raw(self, row_num: int) -> None:
        self.cell(row_num).value = None
