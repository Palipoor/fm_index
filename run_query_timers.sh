#!/bin/bash

# List of arguments
lengths=(10000 100000)
queries=(100 1000 10000)

query_complexity="queries_time.py"

echo "Running tests for queries' time" > out_queries.txt
for length in "${lengths[@]}"
do
    for query in "${queries[@]}"
    do
        python "$query_complexity" --length $length --queries $query >> out_queries.txt
        echo "Done with $length and $query"
        echo "-----------------------------------" >> out_queries.txt
    done
done