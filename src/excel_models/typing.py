import typing

from openpyxl.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

ColumnCell = Cell | typing.Any
CellValue = typing.TypeVar('CellValue')
ColumnValue = typing.TypeVar('ColumnValue')


class AbstractDB:
    tables: list['TTableDef']
    wb: Workbook

    tables_cache: dict[str, 'TTable']


TDB = typing.TypeVar('TDB', bound=AbstractDB)


class AbstractModel:
    column_defs: list['TColumnDef']

    table: 'TTable'
    idx: int
    row_num: int
    values_cache: dict[str, ColumnValue]

    @classmethod
    def as_table(cls, **table_def_kwargs) -> 'TTableDef':
        raise NotImplementedError  # pragma: no cover

    def __eq__(self, other: typing.Self) -> bool:
        raise NotImplementedError  # pragma: no cover

    def __bool__(self) -> bool:
        raise NotImplementedError  # pragma: no cover

    def as_dict(self) -> dict[str, ColumnValue]:
        raise NotImplementedError  # pragma: no cover

    def set_dict(
            self,
            mapping: typing.Mapping[str, ColumnValue] = None,
            /,
            **kwargs,
    ) -> None:
        raise NotImplementedError  # pragma: no cover

    def cell(self, col_num: int) -> Cell:
        raise NotImplementedError  # pragma: no cover

    def cell0(self, col_idx: int) -> Cell:
        raise NotImplementedError  # pragma: no cover

    def cella(self, attr: str) -> Cell:
        raise NotImplementedError  # pragma: no cover

    @property
    def cells(self) -> typing.Sequence[Cell]:
        raise NotImplementedError  # pragma: no cover


TModel = typing.TypeVar('TModel', bound=AbstractModel)


class AbstractColumnDefinition(typing.Generic[TModel]):
    attr: str
    name: str

    def __set_name__(self, model: typing.Type[TModel], attr: str):
        raise NotImplementedError  # pragma: no cover

    def make_column(self, table: 'TTable', col_num: int) -> 'TColumn':
        raise NotImplementedError  # pragma: no cover

    def match_column(self, table: 'TTable', col_num: int) -> typing.Optional['TColumn']:
        raise NotImplementedError  # pragma: no cover

    def init_column(self, table: 'TTable', col_num: int) -> tuple['TColumn', int]:
        raise NotImplementedError  # pragma: no cover

    def get_column(self, table: 'TTable') -> 'TColumn':
        raise NotImplementedError  # pragma: no cover

    def get_raw(self, row: TModel) -> CellValue:
        raise NotImplementedError  # pragma: no cover

    def __get__(self, row: TModel, model: typing.Type[TModel] = None) -> ColumnValue:
        raise NotImplementedError  # pragma: no cover

    def set_raw(self, row: TModel, raw: CellValue) -> None:
        raise NotImplementedError  # pragma: no cover

    def __set__(self, row: TModel, value: ColumnValue) -> None:
        raise NotImplementedError  # pragma: no cover

    def delete_raw(self, row: TModel) -> None:
        raise NotImplementedError  # pragma: no cover

    def __delete__(self, row: TModel) -> None:
        raise NotImplementedError  # pragma: no cover


TColumnDef = typing.TypeVar('TColumnDef', bound=AbstractColumnDefinition)


class AbstractTableDefinition(typing.Generic[TDB, TModel]):
    attr: str
    name: str
    model: typing.Type[TModel]

    def __set_name__(self, db_class: typing.Type[TDB], attr: str):
        raise NotImplementedError  # pragma: no cover

    def make_table(self, db: TDB, ws: Worksheet) -> 'TTable':
        raise NotImplementedError  # pragma: no cover

    def __get__(self, db: TDB, db_class: typing.Type[TDB] = None) -> 'TTable':
        raise NotImplementedError  # pragma: no cover

    def __set__(self, db: TDB, table: typing.Union['TTable', Worksheet]) -> None:
        raise NotImplementedError  # pragma: no cover

    def __delete__(self, db: TDB) -> None:
        raise NotImplementedError  # pragma: no cover


TTableDef = typing.TypeVar('TTableDef', bound=AbstractTableDefinition)


class AbstractTable(typing.Generic[TDB, TModel, TTableDef]):
    db: TDB
    table_def: TTableDef
    ws: Worksheet

    columns_cache: dict[str, 'TColumn']
    columns: typing.Sequence['TColumn']

    def find_columns(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def init_columns(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_title(self, col_num: int) -> str:
        raise NotImplementedError  # pragma: no cover

    def set_title(self, col_num: int, name: str) -> None:
        raise NotImplementedError  # pragma: no cover

    def __eq__(self, other: typing.Self) -> bool:
        raise NotImplementedError  # pragma: no cover

    def __len__(self) -> int:
        raise NotImplementedError  # pragma: no cover

    def get_row_num(self, idx: int) -> int:
        raise NotImplementedError  # pragma: no cover

    def get_idx(self, row_num: int) -> int:
        raise NotImplementedError  # pragma: no cover

    def __getitem__(self, idx: int | slice) -> TModel | list[TModel]:
        raise NotImplementedError  # pragma: no cover

    def __iter__(self) -> typing.Iterator[TModel]:
        raise NotImplementedError  # pragma: no cover

    def __getattr__(self, attr: str) -> 'TColumn':
        raise NotImplementedError  # pragma: no cover

    def cell(self, row_num: int, col_num: int) -> Cell:
        raise NotImplementedError  # pragma: no cover

    def new(self) -> TModel:
        raise NotImplementedError  # pragma: no cover


TTable = typing.TypeVar('TTable', bound=AbstractTable)


class AbstractColumn(typing.Generic[TTable, TColumnDef]):
    table: TTable
    column_def: TColumnDef

    occupied_col_nums: list[int]

    def __eq__(self, other: typing.Self) -> bool:
        raise NotImplementedError  # pragma: no cover

    def __getitem__(self, idx: int | slice) -> ColumnValue | list[ColumnValue]:
        raise NotImplementedError  # pragma: no cover

    def __iter__(self) -> typing.Iterator[ColumnValue]:
        raise NotImplementedError  # pragma: no cover

    def __setitem__(self, idx: int | slice, value: ColumnValue) -> None:
        raise NotImplementedError  # pragma: no cover

    def __delitem__(self, idx: int | slice) -> None:
        raise NotImplementedError  # pragma: no cover

    def cell(self, row_num: int) -> ColumnCell:
        raise NotImplementedError  # pragma: no cover

    def cell0(self, idx: int) -> ColumnCell:
        raise NotImplementedError  # pragma: no cover

    @property
    def cells(self) -> typing.Sequence[ColumnCell]:
        raise NotImplementedError  # pragma: no cover

    def get_raw(self, row_num: int) -> CellValue:
        raise NotImplementedError  # pragma: no cover

    def set_raw(self, row_num: int, raw: CellValue) -> None:
        raise NotImplementedError  # pragma: no cover

    def delete_raw(self, row_num: int) -> None:
        raise NotImplementedError  # pragma: no cover


TColumn = typing.TypeVar('TColumn', bound=AbstractColumn)
