import argparse
from index import FMIndex
import time
import sys
import random

def random_binary(length):
    return ''.join(random.choice(['0', '1']) for _ in range(length))

def main(args):
    binary_string = random_binary(args.length)
    index = FMIndex(binary_string)
    start = time.time()
    random_patterns = [random_binary(random.randint(1, 50)) for _ in range(args.queries)]
    print("length", args.length)
    print('number of queries', args.queries)
    start = time.time()
    for pattern in random_patterns:
        index.get_occurrences(pattern)
    end = time.time()
    print(f"Time taken for {len(random_patterns)} queries: ", end - start)
    print("total length of patterns", sum([len(pattern) for pattern in random_patterns]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Time Complexity')
    parser.add_argument('--length', '-l', type=int, help='Length of the string')
    parser.add_argument('--queries', '-q', type=int, help='Number of queries')
    args = parser.parse_args()
    main(args)