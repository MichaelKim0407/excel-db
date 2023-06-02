from excel_models.column_inst import ExcelColumn
from excel_models.exceptions import DuplicateColumn
from excel_models.typing import TTable, TColumnDef, TColumn
from ._base import BaseColumnDefinition


class Column(BaseColumnDefinition):
    column_class = ExcelColumn
    """
    alias: Alias to another column. `name` attribute is ignored and will be overwritten.
    """
    alias: TColumnDef = None

    def _add_to_class(self):
        super()._add_to_class()
        if self.alias is not None:
            self.name = self.alias.name

    def _make_alias(self, table: TTable) -> TColumn | None:
        column = getattr(table, self.alias.attr)
        return self.column_class(table, self, column.col_num, concrete=False)

    def match_column(self, table: TTable, col_num: int) -> TColumn | None:
        title = table.get_title(col_num)
        if title != self.name:
            return None

        if self.attr in table.columns_cache:
            raise DuplicateColumn(f'Multiple columns matching definition {self.attr}')

        if self.alias is not None:
            return self._make_alias(table)

        return self.column_class(table, self, col_num)

    def init_column(self, table: TTable, col_num: int) -> tuple[TColumn, int]:
        if self.alias is not None:
            return self._make_alias(table), 0

        table.set_title(col_num, self.name)
        return self.column_class(table, self, col_num), 1
