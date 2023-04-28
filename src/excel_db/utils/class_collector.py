import types
import typing

_CLASS_ANNOTATIONS = '__annotations__'
_GENERIC_ALIAS_TYPES = (typing._GenericAlias, types.GenericAlias)  # noqa: pycharm


class _Collector:
    def merge(self, other: typing.Self):
        raise NotImplementedError  # pragma: no cover


class ListCollector(list, _Collector):
    merge = list.extend


class DictCollector(dict, _Collector):
    merge = dict.update


def get_collector_class(type_hint) -> typing.Type[_Collector] | None:
    if type_hint is None or isinstance(type_hint, str):
        return None
    if isinstance(type_hint, _GENERIC_ALIAS_TYPES):
        type_hint = type_hint.__origin__
    if not issubclass(type_hint, _Collector):
        return None
    return type_hint


def find_collectors(obj):
    for k, v in obj.__dict__.items():
        if isinstance(v, _Collector):
            yield k, v


class CollectorMeta(type):
    """
    Add collector variables to class using this meta, as well as its subclasses.

    When subclassing, variables are copied into new collector variables.
    This means subclasses will inherit values already collected, but modifications won't affect "upwards".
    Please note that copying happens when subclassing (i.e. initialization of the subclass),
    so subsequent changes to base classes will not be reflected.

    The ListCollector or DictCollector annotations should be used to indicate collectors.
    For a subclass, an annotation with the same name will **override** the collector variable and start fresh.
    Note: the classes themselves must be used, instead of strings.
    TODO this won't work for Python 4 or `from __future__ import annotations`
    """

    @classmethod
    def find_existing_collectors(cls, bases):
        result = {}
        for base in bases:
            if not isinstance(base, cls):
                continue
            for attr, collector in find_collectors(base):
                if attr not in result:
                    result[attr] = collector.__class__()
                result[attr].merge(collector)
        return result

    GENERIC_ALIAS_TYPES = (typing._GenericAlias, types.GenericAlias)  # noqa: pycharm

    @staticmethod
    def find_new_collectors(namespace: dict):
        if _CLASS_ANNOTATIONS not in namespace:
            return
        for attr, type_hint in namespace[_CLASS_ANNOTATIONS].items():
            collector_class = get_collector_class(type_hint)
            if collector_class is None:
                continue
            yield attr, collector_class()

    def __new__(cls, name, bases, namespace: dict, **kwargs):
        namespace.update(cls.find_existing_collectors(bases))
        namespace.update(cls.find_new_collectors(namespace))
        return super().__new__(cls, name, bases, namespace, **kwargs)
