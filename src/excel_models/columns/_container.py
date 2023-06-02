import typing

from excel_models.typing import TColumnDef
from excel_models.utils.assignable_property import assignable_cached_property
from ._base import BaseColumnDefinition
from ._std import Column


class BaseContainer(BaseColumnDefinition):
    inner_column_class: typing.Type[TColumnDef] = Column

    @assignable_cached_property
    def inner(self) -> TColumnDef:
        return self.inner_column_class()
