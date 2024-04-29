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

def test_case():
    fm = FMIndex('10111') # 111$10  
    assert fm.bwt == bitarray.bitarray('111010')
    assert fm.rank_array.rank('1',0) == 1
    assert fm.rank_array.rank('1',1) == 2
    assert fm.rank_array.rank('1',2) == 3
    assert fm.rank_array.rank('1',3) == 3
    assert fm.rank_array.rank('1',4) == 4
    assert fm.rank_array.rank('0',0) == 0
    assert fm.rank_array.rank('0',3) == 0
    assert fm.rank_array.rank('0',5) == 1
    assert fm.invert_bwt() == '10111'

def test_many_seqs():
    seqs = [bin(i)[2:] for i in range(10, 1000)]
    for s in seqs:
        fm = FMIndex(s)
        assert fm.invert_bwt() == s, f"Failed for {s}"

def test_rep_data():
    """
    This data is from Pizza&Chili. It's a very repetitive sequence.
    """
    with open('/Users/Zire/Downloads/fib41_b.txt', 'r') as f:
        data = f.read()
    data = data[:800]
    index = FMIndex(data)
    a = index.invert_bwt()
    assert a == data

def test_rep_data2():
    """
    This is the famous lorem ipsum text in morse code, converted to binary.
    """
    with open('./morse.txt', 'r') as f:
        data = f.read()
        data = data.replace(' ', '').replace('\n', '')
    index = FMIndex(data)
    a = index.invert_bwt()
    assert a == data

def test_random_data():
    """
    Testing on a random sequence
    """
    import random
    data = ''.join([str(random.randint(0,1)) for i in range(50000)])
    index = FMIndex(data)
    a = index.invert_bwt()
    assert a == data