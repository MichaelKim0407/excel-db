from excel_models.tables import ExcelTableDefinition
from ._base import BaseExcelModel


class ExcelModel(BaseExcelModel):
    table_def_class = ExcelTableDefinition
