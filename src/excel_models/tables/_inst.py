import typing

from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from ..exceptions import ColumnNotFound
from ..typing import AbstractTable, TDB, TModel, TTableDef, TColumn


class ExcelTable(AbstractTable):
    def __init__(
            self,
            db: TDB,
            table_def: TTableDef,
            ws: Worksheet,
    ):
        self.db = db
        self.table_def = table_def
        self.ws = ws

        self.columns_cache = {}
        self.not_found = {}
        self.not_defined = []

    @property
    def model(self) -> typing.Type[TModel]:
        return self.table_def.model

    @property
    def title_row(self) -> int:
        return self.table_def.title_row

    @property
    def columns(self) -> typing.Sequence[TColumn]:
        return tuple(self.columns_cache.values())

    def _clear_cache(self):
        self.columns_cache.clear()
        self.not_found.clear()
        self.not_defined.clear()

    def find_columns(self):
        self._clear_cache()

        for cell in self.ws[self.title_row]:
            if cell.value is None:
                continue
            defined = False
            for column in self.model.columns:
                if column.name != cell.value:
                    continue
                from ..columns import ExcelColumn
                self.columns_cache[column.attr] = ExcelColumn(self, column, cell.column)
                defined = True
                # There may be multiple column accessors to the same Excel column, so we keep going.
            if not defined:
                self.not_defined.append(cell.value)

        for column in self.model.columns:
            if column.attr in self.columns_cache:
                continue
            self.not_found[column.attr] = column

    def init_columns(self):
        self._clear_cache()

        for col_num, column in enumerate(self.model.columns, start=1):
            self.ws.cell(self.title_row, col_num, column.name)
            from ..columns import ExcelColumn
            self.columns_cache[column.attr] = ExcelColumn(self, column, col_num)

    def __eq__(self, other: typing.Self) -> bool:
        if other is None or not isinstance(other, ExcelTable):
            return False

        return (
                self.db == other.db
                and self.table_def == other.table_def
                and self.ws == other.ws
        )

    @property
    def _max_row(self) -> int:
        return self.ws.max_row

    def __len__(self) -> int:
        return self._max_row - self.title_row

    def get_row_num(self, idx: int) -> int:
        return self.title_row + idx + 1

    def get_idx(self, row_num: int) -> int:
        return row_num - self.title_row - 1

    def _get_range(
            self,
            s: slice = None,
            *,
            start=None,
            stop=None,
            step=None,
    ) -> list[int]:
        if s is not None:
            start = s.start
            stop = s.stop
            step = s.step

        return list(range(len(self)))[start:stop:step]

    def __getitem__(self, idx: int | slice) -> TModel | list[TModel]:
        if isinstance(idx, slice):
            return [
                self[i]
                for i in self._get_range(idx)
            ]
        return self.model(self, idx, self.get_row_num(idx))

    def __iter__(self) -> typing.Iterator[TModel]:
        for i in self._get_range():
            yield self[i]

    def __getattr__(self, attr: str) -> TColumn:
        if attr in self.not_found:
            raise ColumnNotFound(self.not_found[attr].name)
        elif attr in self.columns_cache:
            return self.columns_cache[attr]
        else:
            raise AttributeError(attr)

    def cell(self, row_num: int, col_num: int) -> Cell:
        return self.ws.cell(row_num, col_num)

    def new(self) -> TModel:
        self.ws.append([])
        row_num = self.ws._current_row  # noqa: pycharm
        return self[self.get_idx(row_num)]

    @property
    def _max_column_letter(self) -> str:
        return getattr(self, self.model.columns[-1].attr).col_letter

    @property
    def _filter_ref_str(self) -> str:
        return f'A{self.title_row}:{self._max_column_letter}{self._max_row}'

    def add_filter(self):
        self.ws.auto_filter.ref = self._filter_ref_str
