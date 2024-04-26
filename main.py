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

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FM Index')
    parser.add_argument('--input', '-i', type=str, help='File with the sequence')
    args = parser.parse_args()
    main(args)