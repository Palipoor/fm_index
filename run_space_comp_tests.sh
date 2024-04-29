#!/bin/bash

# List of arguments
lengths=(1000 10000 100000 1000000 10000000 100000000)

space_complexity="space_complexity.py"

echo "Running tests for space complexity" > out.txt
for arg in "${lengths[@]}"
do
    python "$space_complexity" --input ~/Downloads/fib41_b.txt --length $arg >> out.txt
    echo "Done with $arg"
    echo "-----------------------------------" >> out.txt
done