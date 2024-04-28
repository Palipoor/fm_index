import pytest
from index import FMIndex
import bitarray

seq = '0010110101'
# bwt = 1$110100100

@pytest.fixture
def fm_index():
    return FMIndex(seq)

def test_bwt(fm_index):
    assert fm_index.bwt == bitarray.bitarray('10110100100')

def test_rank(fm_index):
    print(fm_index.rank_array.sentinel_index)
    assert fm_index.rank('0', 3) == 0
    assert fm_index.rank('0', 9) == 4
    assert fm_index.rank('1', 3) == 3
    assert fm_index.rank('1', 9) == 5
    assert fm_index.rank('1', 10) == 5
    assert fm_index.rank('$', 10) == 1
    assert fm_index.rank('0', 0) == 0
    assert fm_index.rank('1', 0) == 1
    assert fm_index.rank('$', 0) == 0
    assert fm_index.rank('0',  1) == 0

def test_inverse(fm_index):
    assert fm_index.invert_bwt() == seq