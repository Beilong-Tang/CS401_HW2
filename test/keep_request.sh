#!/bin/bash
cur_path=$(pwd)

cd ../rest_client

# Define the log file
LOGFILE=$1

> "$cur_path/$LOGFILE"

# Define the interval (in seconds) between each execution
INTERVAL=1

while true; do
    # Get the current timestamp
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    # Run the kubectl command and capture the output
    OUTPUT=$(python client_cli.py --songs 'Portland' --hostname 10.109.101.236)

    # Append the timestamp and output to the log file
    echo "[$TIMESTAMP]" >> "$cur_path/$LOGFILE"
    echo "$OUTPUT" >> "$cur_path/$LOGFILE"

    # Wait for the specified interval before running again
    sleep "$INTERVAL"
done
