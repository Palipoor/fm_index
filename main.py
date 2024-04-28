import argparse
import bitarray
from index import FMIndex

def read_file(file_path):
    with open(file_path, 'r') as file:
        sequence = file.read().strip()
        if len(sequence) == 0:
            raise ValueError('Empty sequence')
        return sequence

def main(args):
    input_file = args.input
    sequence = read_file(input_file)
    index = FMIndex(sequence)
    print(index.bwt)
    print(index.sentinel_index)
    print(index.sampled_sa)
    print(index.rank('0', 3))
    print(index.rank('1', 3))
    print(index.rank('0', 260))
    print(index.rank('0', 300))
    print(index._get_lf(10))
          
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FM Index')
    parser.add_argument('--input', '-i', type=str, help='File with the sequence')
    args = parser.parse_args()
    main(args)