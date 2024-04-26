import pydivsufsort as sa
import bitarray as ba
from math import log2, floor

class FMIndex():
    def __init__(self, seq):
        self.sequence = seq
        self.n = len(self.sequence)
        self.c_array = [0, self.sequence.count('0')]
        self.log_n = floor(log2(self.n))
        self._build_suffix_array()
        self._build_bwt()
        self._sample_sa()

    def _build_suffix_array(self):
        self.sa = sa.divsufsort(self.sequence)

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

    def get_sa(self, i):
        pass

    def invert_bwt(self):
        pass

    def get_occurrences(self, pattern):
        pass


    
    
        
