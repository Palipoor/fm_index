import pydivsufsort as sa
import bitarray as ba
from math import log2, floor

class FMIndex():
    def __init__(self, seq):
        self.sequence = seq
        self.n = len(self.sequence)
        self.c_array = [0, self.sequence.count('0')]
        self.log_n = floor(log2(self.n))
        self._build_rank_array()
        self._build_suffix_array()
        self._build_bwt()
        self._sample_sa()

    def _build_suffix_array(self):
        self.sa = sa.divsufsort(self.sequence)

    def _build_rank_array(self):
        self.rank_array = RankDS(self.sequence)

    def rank(self, c, i):
        return self.rank_array.rank(c, i)
    
    def _build_bwt(self):
        self.bwt = ba.bitarray(self.n)
        for i in range(len(self.sa)):
            if self.sa[i] == 0:
                self.bwt[i] = int(self.sequence[self.n - 1])
            else:
                self.bwt[i] = int(self.sequence[self.sa[i] - 1])
        
    
    def _sample_sa(self):
        self.sampled_sa = {}
        for i in range(0, self.n, self.log_n):
            self.sampled_sa[i] = self.sa[i]
    
        del self.sa

    def _get_lf(self, i):
        return 0 #TODO implement this

    def get_sa(self, i):
        s = 0
        while not self.sampled_sa.get(i):
            i = self._get_lf(i)
            s += 1
        j = self.sampled_sa[i]
        return j + s

    def invert_bwt(self):
        pass

    def get_occurrences(self, pattern):
        m = len(pattern)
        s = 1
        e = self.n
        for i in range(m - 1, -1, -1):
            c = pattern[i]
            s = self.c_array[int(c)] + self.rank_array[int(c)][s - 1] + 1
            e = self.c_array[int(c)] + self.rank_array[int(c)][e]
            if s > e:
                return []
        occ = [self.get_sa(i) for i in range(s, e+1)]
        return occ


    
    
class RankDS():
    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)
        self.log_n = floor(log2(self.n))
        self.small_block_size = self.log_n // 2
        self.large_block_size = self.log_n ** 2
        self.small_per_large = self.large_block_size // self.small_block_size
        self.num_large_blocks = self.n // self.large_block_size
        self.num_small_blocks = self.n // self.small_block_size
        self._build_array()
    
    def _build_array(self):
        cum_rank = 0
        self.large_cum_ranks = []
        self.small_cum_ranks = []
        self.extra_ranks = []
        for i in range(0,self.n, self.large_block_size):
            self.large_cum_ranks.append(cum_rank)
            rel_cum_rank = 0
            for j in range(0, self.large_block_size, self.small_block_size):
                self.small_cum_ranks.append(rel_cum_rank)
                rel_cum_rank = rel_cum_rank + self.sequence[i+j:i+j + self.small_block_size].count('1') 
            cum_rank = cum_rank + self.sequence[i:i+self.large_block_size].count('1')
        
        if self.n % self.large_block_size != 0:
            self.extra_ranks = [0] * (self.n % self.large_block_size)
            self.extra_ranks[0] = cum_rank
            for i in range(1, self.n % self.large_block_size):
                self.extra_ranks[i] = self.extra_ranks[i-1] + int(self.sequence[self.n - i - 1])


        self.lookup_table = []
        for i in range(0, self.n, self.large_block_size):
            for j in range(0, self.large_block_size, self.small_block_size):
                small_block = self.sequence[i+j:i+j+self.small_block_size]
                self.lookup_table.append([small_block[:k].count('1') for k in range(1, self.small_block_size+1)])

    def rank(self, c, i):
        if i == 0:
            return 0
        if i > self.large_block_size * self.num_large_blocks:
            rank = self.extra_ranks[i % self.large_block_size]
        else:
            block_ind = i // self.large_block_size
            s_block = (i % self.large_block_size) // self.small_block_size
            s_block_ind = floor((self.small_per_large * block_ind) + s_block)
            rank = self.large_cum_ranks[block_ind] + self.small_cum_ranks[s_block_ind] + self.lookup_table[s_block_ind][i % self.small_block_size]
        if c == '0':
            return i - rank
        else:
            return rank