#!/bin/bash

# Function to check if the input is a positive integer
is_positive_integer() {
    [[ $1 =~ ^[0-9]+$ ]] && (( $1 > 0 ))
}

# Function to kill all background processes upon exit
cleanup() {
    echo "Stopping all background jobs..."
    kill $(jobs -p)
}

# Trap SIGINT (CTRL+C) and call cleanup function
trap cleanup SIGINT

# Check if exactly one argument is provided and it's a positive integer
if [ "$#" -ne 1 ] || ! is_positive_integer "$1"; then
    echo "Usage: $0 <threads>"
    echo "       <threads> must be a positive integer."
    exit 1
fi

# Pip install deps
/usr/bin/python -m pip install -r /etc/scraper/requirements.txt

threads=$1

# Starting Python scripts in the specified number of threads
for i in $(seq 1 $threads); do
    python /etc/scraper/get_ids.py &
    # python /etc/scraper/get_listings_clean.py &
    python /etc/scraper/get_listings_raw.py &
    python /etc/scraper/get_urls.py &
done

# Wait for all background jobs to finish
wait
