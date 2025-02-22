#!/bin/bash

# Define the log file
LOGFILE="test_replicas_num_change.log"

# Define the interval (in seconds) between each execution
INTERVAL=1

# Infinite loop to keep running the command
while true; do
    # Get the current timestamp
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    # Run the kubectl command and capture the output
    OUTPUT=$(kubectl get deployment playlist-recommender-deployment)

    # Append the timestamp and output to the log file
    echo "[$TIMESTAMP]" >> "$LOGFILE"
    echo "$OUTPUT" >> "$LOGFILE"
    echo "-------------------" >> "$LOGFILE"

    # Wait for the specified interval before running again
    sleep "$INTERVAL"
done
