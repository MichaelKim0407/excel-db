from functools import cached_property


class assignable_cached_property(cached_property):  # noqa: pycharm
    def __set__(self, instance, value):
        instance.__dict__[self.attrname] = value
