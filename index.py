import pydivsufsort as sa
import bitarray as ba
import time
from math import log2, floor
from tqdm import tqdm


class FMIndex():
    """
    FMIndex class for binary sequences. 
    NOTE: Every array in this structure is 0-indexed.

    Attributes:
        sequence (str): The input sequence. This sequence will eventually be cleaned by the garbage collector.
        n (int): The length of the input sequence.
        c_array (dict): The character count array. 
        sa (list): The suffix array. This is built using the pydivsufsort library. It will eventually be cleaned by the garbage collector and replaced with the sampled suffix array.
        rank_array (RankDS): The rank data structure. This structure takes O(n) bits of space and supports rank queries in O(1) time.
        bwt (bitarray): The Burrows-Wheeler Transform. The BWT is stored as a bitarray to save space.
        sentinel_index (int): The index of the sentinel character in the BWT. Stored separately to save space.
        sampled_sa (dict): The sampled suffix array. Every log(n)th element of the suffix array is stored in this dictionary.

    Methods:
        __init__(self, seq): Initializes the FMIndex object.
        _build_suffix_array(self): Internally used. Builds the suffix array. 
        _build_rank_array(self): Internally used. Builds the rank data structure in O(n) time.
        _build_bwt(self): Internally used. Builds the Burrows-Wheeler Transform.
        _get_bwt(self, i): Internally used. Returns the character at position i in the BWT.
        _sample_sa(self): Internally used. Samples the suffix array to reduce space.
        _get_lf(self, i): Returns the LF mapping at position i. LF mapping is computed on-the-fly, so it doesn't take extra space.
        rank(self, c, i): Returns the rank of character c at position i of the BWT in O(1) time.
        get_sa(self, i): Returns the original position of the suffix at position i in the BWT.
        invert_bwt(self): Inverts the Burrows-Wheeler Transform to retrieve the original sequence.
        get_occurrences(self, pattern): Returns the positions of occurrences of a pattern in the original sequence.
    """
    def __init__(self, seq):
        self.sequence = seq
        self.n = len(self.sequence)
        if self.n < 4:
            raise ValueError('Sequence must be at least 4 characters long')
        self.c_array = {'$': 0, 0: 1, 1: self.sequence.count('0') + 1}
        t = time.time()
        self.log_n = floor(log2(self.n))
        self._build_suffix_array()
        print('Suffix array built in', time.time() - t)
        t = time.time()
        self._build_bwt()
        print('BWT built in', time.time() - t)
        t = time.time()
        self._build_rank_array()
        print('Rank array built in', time.time() - t)
        t = time.time()
        self._sample_sa()
        print('Sampled SA built in', time.time() - t)


    def _build_suffix_array(self):
        self.sa = sa.divsufsort(self.sequence + '$')

    def _build_rank_array(self):
        self.rank_array = RankDS(self.bwt, self.sentinel_index)
        
    def rank(self, c, i):
        """
        args:
            c (str): The character whose rank is to be computed.
            i (int): The position in the BWT.
        """
        if i < 0:
            return 0
        if i >= self.n:
            i = self.n-1
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
            
        
    def _get_bwt(self, i):
        """
        args:
            i (int): The position in the BWT.
        """
        if i == self.sentinel_index:
            return '$'
        return self.bwt[i]

    def _sample_sa(self):
        self.sampled_sa = {}
        for i in range(0, self.n):
            s = self.sa[i]
            if s % self.log_n == 0:
                self.sampled_sa[i] = s

    def _get_lf(self, i):
        x = self._get_bwt(i)
        r = self.rank(str(x), i) -1 
        return self.c_array[x] + r
    
    def get_sa(self, i):
        """
        args:
            i (int): The index for suffix array.
        """
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
        """
        args:
            pattern (str): The pattern to search for.
        """
        m = len(pattern)
        s = 0
        e = len(self.bwt) -1
        for i in range(m - 1, -1, -1):
            c = pattern[i]
            if s <=0:
                s = self.c_array[int(c)]
            else:
                s = self.c_array[int(c)] + self.rank(c,s-1)
            e = self.c_array[int(c)] + self.rank(c,e) -1 
            if s > e:
                print('pattern not found')
                return []
        print(f'found {e-s+1} occurrences')
        occ = [self.get_sa(i) for i in range(s, e + 1)]
        return sorted(occ)

class RankDS():
    """
    Rank Data Structure

    Attributes:
        sequence (bitarray): The input sequence (BWT of the original sequence from fm index). This sequence will eventually be cleaned by the garbage collector.
        sentinel_index (int): The index of the sentinel character in the BWT.
        small_block_size (int): The size of the small block. Equals to log(n) // 2.
        large_block_size (int): The size of the large block. Equals to log(n) ** 2.
        small_per_large (int): The number of small blocks per large block.
        num_large_blocks (int): The number of large blocks.
        num_small_blocks (int): The number of small blocks.
        large_cum_ranks (list): The cumulative ranks of large blocks.
        small_cum_ranks (list): The cumulative ranks of small blocks.
        lookup_table (list): The lookup table. This is used to compute the rank of a character in a small block in O(1) time.
    """
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
        self.n = 2 ** (self.n.bit_length())
        self.sequence = self.sequence + ba.bitarray('0' * (self.n - len(self.sequence)))
        self.log_n = floor(log2(self.n))
        self.small_block_size = self.log_n // 2
        self.large_block_size = min(self.n,self.log_n ** 2)
        self.small_per_large = self.large_block_size // self.small_block_size
        self.num_large_blocks = self.n // self.large_block_size
        self.num_small_blocks = self.small_per_large * self.num_large_blocks

        cum_rank = 0
        self.large_cum_ranks = []
        self.small_cum_ranks = []
        for i in range(0,self.large_block_size * self.num_large_blocks, self.large_block_size):
            self.large_cum_ranks.append(cum_rank)
            rel_cum_rank = 0
            for j in range(0, self.small_block_size * self.small_per_large, self.small_block_size):
                self.small_cum_ranks.append(rel_cum_rank)
                rel_cum_rank = rel_cum_rank + self.sequence[i+j:i+j + self.small_block_size].count(ba.bitarray('1') )
            cum_rank = cum_rank + self.sequence[i:i+self.large_block_size].count(ba.bitarray('1'))

        self.lookup_table = []
        for i in range(0, self.large_block_size * self.num_large_blocks, self.large_block_size):
            for j in range(0, self.large_block_size, self.small_block_size):
                small_block = self.sequence[i+j:i+j+self.small_block_size]
                self.lookup_table.append([small_block[:k].count(ba.bitarray('1')) for k in range(1, self.small_block_size+1)])

    def rank(self, c, i):
        """
        Performs rank queries in O(1) time.

        args:
            c (str): The character whose rank is to be computed.
            i (int): The position in the BWT.
        """
        if c == '$':
            if i >= self.sentinel_index:
                return 1
            else:
                return 0
        if i == 0:
            rank = self.lookup_table[0][0] 
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
