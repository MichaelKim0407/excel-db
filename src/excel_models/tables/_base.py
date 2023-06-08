import typing

from openpyxl.worksheet.worksheet import Worksheet

from excel_models.typing import AbstractTableDefinition, TDB, TTable
from excel_models.utils.descriptors import BasePropertyDescriptor


class BaseExcelTableDefinition(
    BasePropertyDescriptor[TDB],
    AbstractTableDefinition,
):
    table_class: typing.Type[TTable]  # assign in subclass
    title_row: int = 1
    trim_by_title: bool = False
    trim: bool = False

    def _add_to_class(self):
        super()._add_to_class()
        self.obj_type.tables.append(self)

    def make_table(self, db: TDB, ws: Worksheet) -> TTable:
        return self.table_class(db, self, ws)

    _f_initialize = None

    def _initialize_default(self, db: TDB, table: TTable):
        pass

    @property
    def _initialize_method(self) -> typing.Callable:
        if self._f_initialize is None:
            return self._initialize_default
        else:
            return self._f_initialize

    def _initialize(self, db: TDB, table: TTable):
        self._initialize_method(db, table)

    def initializer(self, f_initialize):
        self._f_initialize = f_initialize
        return self

    def _get_default(self, db: TDB) -> TTable:
        if self.name in db.wb:
            ws = db.wb[self.name]
            table = self.make_table(db, ws)
            if self.trim_by_title:
                table.trim_cols(use_title_row=True)
            if self.trim:
                table.trim()
            table.find_columns()
        else:
            ws = db.wb.create_sheet(self.name)
            table = self.make_table(db, ws)
            table.init_columns()
            self._initialize(db, table)
        return table

    def _get(self, db: TDB) -> TTable:
        if self.attr not in db.tables_cache:
            table = self._get_method(db)
            db.tables_cache[self.attr] = table
        return db.tables_cache[self.attr]

    def _set_default(self, db: TDB, table: TTable | Worksheet) -> TTable:
        if self.name in db.wb:
            del db.wb[self.name]
        if isinstance(table, Worksheet):
            ws = table
        else:
            ws = table.ws
        copy: Worksheet = db.wb.copy_worksheet(ws)
        copy.title = self.name
        return self.make_table(db, copy)

    def _set(self, db: TDB, table: TTable | Worksheet):
        copy = self._set_method(db, table)
        db.tables_cache[self.attr] = copy

    def _delete_default(self, db: TDB):
        del db.wb[self.name]

    def _delete(self, db: TDB):
        if self.attr in db.__dict__:
            del db.tables_cache[self.attr]
        self._delete_method(db)
