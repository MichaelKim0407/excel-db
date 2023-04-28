import typing


class SubclassInjectMeta(type):
    """
    Inject variables to all subclasses for a class using this meta (subclass from this).

    This can be useful e.g. when you want an empty list for each subclass:
    1. You can't declare it in the base class because all subclasses will reference the same list.
    2. You may use __subclass_init__ instead, however it happens after __set_name__ for all class members.
       For what we want to achieve with all the descriptors here, it wouldn't work.

    This injects the variables **before** __set_name__.

    To use, subclass from this meta and use it for the base class. See ExcelModel or ExcelDB for examples.
    """

    @classmethod
    def is_base_class(cls, bases) -> bool:
        for base in bases:
            if isinstance(base, cls):
                return False
        return True

    @staticmethod
    def vars() -> typing.Mapping[str, typing.Any]:
        raise NotImplementedError  # pragma: no cover

    def __new__(cls, name, bases, namespace: dict, **kwargs):
        if not cls.is_base_class(bases):
            namespace.update(cls.vars())
        return super().__new__(cls, name, bases, namespace, **kwargs)
