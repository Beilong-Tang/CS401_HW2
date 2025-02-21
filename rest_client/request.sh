#!/bin/bash

## Test the server is working or not
# wget --server-response \
#    --output-document response.out \
#    --header='Content-Type: application/json' \
#    --post-data '{"songs": ["Yesterday", "Bohemian Rhapsody", "Watch Out"]}' \
#    http://localhost:52006/api/recommender

## Test the client_cli
python3 client_cli.py --songs "Watch Out" "Black Beatles"
