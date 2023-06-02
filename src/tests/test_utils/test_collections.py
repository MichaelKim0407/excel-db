from excel_models.utils.collections import rstrip_none


def test_rstrip_none():
    assert list(rstrip_none([1, 2, None, 3, None, None])) == [1, 2, None, 3]
