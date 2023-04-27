class ExcelModel:
    columns: list['Column']

    @classmethod
    def as_table(cls, **kwargs) -> 'ExcelTableDefinition':
        return ExcelTableDefinition(cls, **kwargs)

    def __init__(
            self,
            table: 'ExcelTable',
            idx: int,
            row_num: int,
    ):
        self.table = table
        self.idx = idx
        self.row_num = row_num

    def __eq__(self, other: 'ExcelModel') -> bool:
        if other is None or not isinstance(other, ExcelModel):
            return False

        return (
                self.table == other.table
                and self.idx == other.idx
                and self.row_num == other.row_num
        )


from .columns import Column  # noqa: E402
from .tables import ExcelTableDefinition, ExcelTable  # noqa: E402
