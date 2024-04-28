import pytest
from index import FMIndex


@pytest.fixture
def fm_index():
    return FMIndex('00101101010010110101')


def test_occ1(fm_index):
    # occs = fm_index.get_occurrences('1')
    # assert occs == [2, 4,5,7, 9, 12,14,15,17,19]
    # occs = fm_index.get_occurrences('0')
    # assert occs == [0, 1, 3, 6, 8, 10, 11, 13, 16, 18]
    # occs = fm_index.get_occurrences('01')
    # assert occs == [1,3,6,8,11,13,16,18]
    # occs = fm_index.get_occurrences('11')
    # assert occs == [4,14]
    occs = fm_index.get_occurrences('1010011')
    assert occs == []
