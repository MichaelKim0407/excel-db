import typing
from dataclasses import dataclass
from functools import cached_property

from returns import returns

from excel_models.typing import TColumnDef, CellContext, ColumnCell
from excel_models.utils.assignable_property import assignable_cached_property
from ._base import BaseColumnDefinition
from ._std import Column


class BaseContainer(BaseColumnDefinition):
    inner_column_class: typing.Type[TColumnDef] = Column

    @assignable_cached_property
    def inner(self) -> TColumnDef:
        return self.inner_column_class()

    @dataclass
    class InnerContext(CellContext):
        parent: CellContext

        @classmethod
        def from_parent(cls, parent: CellContext, **kwargs):
            return cls(
                row=parent.row,
                column=parent.column,
                parent=parent,
                **kwargs,  # noqa: pycharm
            )


class BaseArrayContainer(BaseContainer):
    @dataclass
    class InnerContext(BaseContainer.InnerContext):
        index: int

        @cached_property
        def cell(self) -> ColumnCell:
            return self.parent.cell[self.index]

    @returns(tuple)
    def to_python(self, raw: typing.Sequence, context: CellContext) -> typing.Sequence:
        for i, v in enumerate(raw):
            yield self.inner.to_python(v, self.InnerContext.from_parent(context, index=i))

    @returns(tuple)
    def from_python(self, value: typing.Sequence, context: CellContext) -> typing.Sequence:
        for i, v in enumerate(value):
            yield self.inner.from_python(v, self.InnerContext.from_parent(context, index=i))


class BaseMapContainer(BaseContainer):
    omit_none: bool = False

    @dataclass
    class InnerContext(BaseContainer.InnerContext):
        key: str

        @cached_property
        def cell(self) -> ColumnCell:
            return self.parent.cell[self.key]

    @returns(dict)
    def to_python(self, raw: typing.Mapping, context: CellContext) -> typing.Mapping:
        for k, v in raw.items():
            v2 = self.inner.to_python(v, self.InnerContext.from_parent(context, key=k))
            if v2 is None and self.omit_none:
                continue
            yield k, v2

    @returns(dict)
    def from_python(self, value: typing.Mapping, context: CellContext) -> typing.Mapping:
        for k, v in value.items():
            yield k, self.inner.from_python(v, self.InnerContext.from_parent(context, key=k))
