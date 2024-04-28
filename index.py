import pydivsufsort as sa
import bitarray as ba
from math import log2, floor

class FMIndex():
    def __init__(self, seq):
        self.sequence = seq
        self.n = len(self.sequence)
        if self.n < 4:
            raise ValueError('Sequence must be at least 4 characters long')
        self.c_array = {'$': 0, 0: 1, 1: self.sequence.count('0') + 1}
        self.log_n = floor(log2(self.n))
        self._build_suffix_array()
        self._build_bwt()
        self._build_rank_array()
        self._sample_sa()

    def _build_suffix_array(self):
        self.sa = sa.divsufsort(self.sequence + '$')

    def _build_rank_array(self):
        self.rank_array = RankDS(self.bwt, self.sentinel_index)
        
    def rank(self, c, i):
        if i < 0:
            return 0
        if i > self.n:
            i = self.n
        return self.rank_array.rank(c, i)
    
    def _build_bwt(self):
        self.bwt = ba.bitarray(self.n + 1)
        self.sentinel_index = -1
        for i in range(len(self.sa)):
            if self.sa[i] == 0:
                self.sentinel_index = i
                self.bwt[i] = 0
            else:
                self.bwt[i] = int(self.sequence[self.sa[i] - 1])
            
        del self.sequence
        
    def _get_bwt(self, i):
        if i == self.sentinel_index:
            return '$'
        return self.bwt[i]
    
    def _get_inverse_sa(self):
        i_sa = [0]*len(self.sa) 
        for i in range(len(self.sa)):
            i_sa[self.sa[i]] = i
        return i_sa
    
    def _sample_sa(self):
        self.sampled_sa = {}
        for i in range(0, self.n):
            sa = self.sa[i]
            if sa % self.log_n == 0:
                self.sampled_sa[i] = sa
        # del self.sa

    def _get_lf(self, i):
        x = self._get_bwt(i)
        return self.c_array[x] + self.rank_array.rank(str(x), i) -1
    
    def get_sa(self, i):
        s = 0
        while self.sampled_sa.get(i, -1) == -1:
            i = self._get_lf(i)
            s += 1
        j = self.sampled_sa[i]
        return j + s

    def invert_bwt(self):
        seq = ''
        p = 0
        c = self.bwt[p]
        for i in range(self.n):
            seq = str(c) + seq
            p = self._get_lf(p)
            c = self.bwt[p]
        return seq

    def get_occurrences(self, pattern):
        m = len(pattern)
        s = 0
        e = self.n
        for i in range(m - 1, -1, -1):
            c = pattern[i]
            s = self.c_array[int(c)] + self.rank(c,s-1)
            e = self.c_array[int(c)] + self.rank(c,e)
            if s >= e:
                return []
        occ = [self.get_sa(i) for i in range(s, e)]
        return sorted(occ)

class RankDS():
    def __init__(self, sequence, sentinel_index = -1):
        self.sequence = sequence
        self.n = len(sequence)
        self.sentinel_index = sentinel_index
        self.log_n = floor(log2(self.n))
        self.small_block_size = self.log_n // 2
        self.large_block_size = min(self.n,self.log_n ** 2)
        self.small_per_large = self.large_block_size // self.small_block_size
        self.num_large_blocks = self.n // self.large_block_size
        self.num_small_blocks = self.small_per_large * self.num_large_blocks
        self._build_array()
    
    def _build_array(self):
        cum_rank = 0
        self.large_cum_ranks = []
        self.small_cum_ranks = []
        self.extra_ranks = []
        for i in range(0,self.large_block_size * self.num_large_blocks, self.large_block_size):
            self.large_cum_ranks.append(cum_rank)
            rel_cum_rank = 0
            for j in range(0, self.large_block_size, self.small_block_size):
                self.small_cum_ranks.append(rel_cum_rank)
                rel_cum_rank = rel_cum_rank + self.sequence[i+j:i+j + self.small_block_size].count(ba.bitarray('1') )
            cum_rank = cum_rank + self.sequence[i:i+self.large_block_size].count(ba.bitarray('1'))
        if self.n % self.large_block_size != 0:
            self.extra_ranks = [0] * (self.n % self.large_block_size)
            cursor = self.small_block_size * (self.num_small_blocks -1 )
            self.extra_ranks[0] = self.small_cum_ranks[-1] + self.sequence[cursor:cursor + self.small_block_size+1].count(ba.bitarray('1'))
            cursor = cursor + self.small_block_size + 1
            for i in range(1, len(self.extra_ranks)):
                self.extra_ranks[i] = self.extra_ranks[i-1] + self.sequence[cursor]
                cursor = cursor + 1
        self.lookup_table = []
        for i in range(0, self.large_block_size * self.num_large_blocks, self.large_block_size):
            for j in range(0, self.large_block_size, self.small_block_size):
                small_block = self.sequence[i+j:i+j+self.small_block_size]
                self.lookup_table.append([small_block[:k].count(ba.bitarray('1')) for k in range(1, self.small_block_size+1)])
        del self.sequence

    def rank(self, c, i):
        if c == '$':
                if i >= self.sentinel_index:
                    return 1
                else:
                    return 0
        if i == 0:
            rank = self.lookup_table[0][0] 
        else:
            if i >= self.large_block_size * self.num_large_blocks:
                rank = self.extra_ranks[i % self.large_block_size]
            else:
                block_ind = i // self.large_block_size
                s_block = (i % self.large_block_size) // self.small_block_size
                s_block_ind = floor((self.small_per_large * block_ind) + s_block)
                rank = self.large_cum_ranks[block_ind] + self.small_cum_ranks[s_block_ind] + self.lookup_table[s_block_ind][i % self.small_block_size]
        if c == '0':
            if i >= self.sentinel_index:
                return i - rank
            else:
                return i - rank + 1
        else:
            return rank