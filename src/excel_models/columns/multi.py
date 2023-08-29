import typing

from excel_models.column_inst.array import ExcelColumnArray
from excel_models.column_inst.map import ExcelColumnMap
from excel_models.column_inst.remainder import ExcelColumnRemainder
from excel_models.exceptions import DuplicateColumn
from excel_models.typing import TTable, TColumn
from ._container import BaseArrayContainer, BaseMapContainer


class Columns(BaseArrayContainer):
    column_class = ExcelColumnArray
    width: int

    def _get_title(self, table: TTable) -> str:
        return self.name

    def match_column(self, table: TTable, col_num: int) -> TColumn | None:
        title = table.get_title(col_num)
        if title != self._get_title(table):
            return None

        return self.column_class(table, self, col_num, self.width)

    def init_column(self, table: TTable, col_num: int) -> tuple[TColumn, int]:
        table.set_title(col_num, self._get_title(table))
        return self.column_class(table, self, col_num, self.width), self.width


class ColumnsStartWith(BaseMapContainer):
    column_class = ExcelColumnMap
    create_keys: typing.Sequence[str]

    def _get_create_keys(self, table: TTable) -> typing.Sequence[str]:
        return self.create_keys

    def _format_title(self, key: str, table: TTable) -> str:
        return f'{self.name}{key}'

    def _parse_title(self, title: str, table: TTable) -> str | None:
        if not title.startswith(self.name):
            return None
        return title[len(self.name):]

    def match_column(self, table: TTable, col_num: int) -> TColumn | None:
        title = table.get_title(col_num)
        key = self._parse_title(title, table)
        if key is None:
            return None

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
            for c, k in enumerate(self._get_create_keys(table), start=col_num)
        }
        for k, c in col_map.items():
            table.set_title(c, self._format_title(k, table))
        return self.column_class(table, self, col_map), len(col_map)


class Remainder(BaseArrayContainer):
    column_class = ExcelColumnRemainder

    def _get_title(self, table: TTable) -> str:
        return self.name

    def match_column(self, table: TTable, col_num: int) -> TColumn | None:
        title = table.get_title(col_num)
        if title != self._get_title(table):
            return None

        return self.column_class(table, self, col_num)

    def init_column(self, table: TTable, col_num: int) -> tuple[TColumn, int]:
        table.set_title(col_num, self._get_title(table))
        return self.column_class(table, self, col_num), 1  # use 1 here but this must be the last column
