from ._base import BaseExcelTableDefinition
from ._inst import ExcelTable


class ExcelTableDefinition(BaseExcelTableDefinition):
    table_class = ExcelTable
