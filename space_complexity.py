import argparse
from index import FMIndex
from pympler import asizeof
from functools import partial
from matplotlib import pyplot as plt
import sys

def main(args):
    with open(args.input, 'r') as f:
        data = f.read().strip()
    
    data = data[:args.length]
    index = FMIndex(data)
    print('String size: ', asizeof.asizeof(data))
    print('BWT size:', asizeof.asizeof(index.bwt))
    print('C array size:', asizeof.asizeof(index.c_array))
    print('SA samples size: ' , sys.getsizeof(index.sampled_sa))
    print('SA size:', sys.getsizeof(index.sa))
    print('Rank array size:', (asizeof.asizeof(index.rank_array) - asizeof.asizeof(index.rank_array.sequence)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Space Complexity')
    parser.add_argument('--input', type=str, help='Input file')
    parser.add_argument('--length', '-l', type=int, help='Length of the string')
    args = parser.parse_args()
    main(args)
