from ._base import BaseColumnDefinition
from ..typing import TTable, TColumnDef, TColumn


class Column(BaseColumnDefinition):
    """
    alias: Alias to another column. `name` attribute is ignored and will be overwritten.
    """
    alias: TColumnDef = None

    def __post_init__(self):
        super().__post_init__()
        if self.column_class is None:
            from excel_models.column_inst import ExcelColumn
            self.column_class = ExcelColumn

    def _add_to_class(self):
        super()._add_to_class()
        if self.alias is not None:
            self.name = self.alias.name

    def make_column(self, table: TTable, col_num: int) -> TColumn:
        return self.column_class(
            table,
            self,
            col_num,
            concrete=self.alias is None,
        )

    def _make_alias(self, table: TTable) -> TColumn | None:
        column = getattr(table, self.alias.attr)
        return self.make_column(table, column.col_num)

    def match_column(self, table: TTable, col_num: int) -> TColumn | None:
        title = table.get_title(col_num)
        if title != self.name:
            return None

        if self.alias is not None:
            return self._make_alias(table)

        return self.make_column(table, col_num)

    def init_column(self, table: TTable, col_num: int) -> tuple[TColumn, int]:
        if self.alias is not None:
            return self._make_alias(table), 0

        table.set_title(col_num, self.name)
        return self.make_column(table, col_num), 1
