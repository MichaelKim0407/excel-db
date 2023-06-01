import typing

from excel_models.typing import TColumnDef
from ._base import BaseColumnDefinition
from ._std import Column


class BaseContainer(BaseColumnDefinition):
    inner_column_class: typing.Type[TColumnDef] = Column
    inner: TColumnDef = None

    def __post_init__(self):
        super().__post_init__()
        if self.inner is None:
            self.inner = self.inner_column_class()
