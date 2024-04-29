# FM index implementation - Course project for CSE 549 - Spring 2024

Zofia Stefankovic, Pegah Alipoormolabashi

## Code Overview

### Index Creation
The main code for FM index is in `index.py`. This index is implemented for sequences with alphabet = {0,1}.
Creating an index is as simple as:
``` python
from index import FMIndex 

my_seq = '1010010001010'
my_index = FMIndex(my_seq)
```
### Inside the Index
Multiple steps are done to construct the FM index and make it ready to use: 

 1. #### Building suffix array (This is done via a third-party library)
`self.sa = sa.divsufsort(self.sequence + '$')`

 2. #### Building the Burrows–Wheeler Transform:
 The Burrows-Wheeler transform is constructed based on its relationship with suffix array. 
 A noteworthy implenetation detail: Instead of storing the transform in a common string, we store it in a `bitarray` to reduce used space. The sentinel symbol ('$') is simulated by storing its index in the BWT. This reduces the space consumed to O(n) bits + one word, and does not have more than O(1) performance overload.
When BWT is created, the main sequence is removed from the memory: 
`del  self.sequence`

3. #### Building a data structure to support rank queries:
We use Jacobson's rank (Guy Joseph Jacobson. “Succinct Static Data Structures”. PhD thesis. Carnegie Mellon University, 1988.).
The implementation is in `class RankDS`. It allows for O(n) bits space and O(1) query time. 

4. #### Reducing the space used by suffix array by only storing a sample and deleting the rest. 
The function `get_sa` computes suffix array at any index `i` in O(log n) time.


## How to use

After installing the packages in `requirements.txt`, you can follow the example in `example.ipynb` to run the code.