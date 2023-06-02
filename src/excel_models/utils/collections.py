import typing


def rstrip_none(iterable: typing.Iterable) -> typing.Iterator:
    buffer = 0
    for item in iterable:
        if item is None:
            buffer += 1
            continue
        while buffer > 0:
            yield None
            buffer -= 1
        yield item
