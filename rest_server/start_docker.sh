#!/bin/bash


## To build the image
docker build -t beilongtang/playlists-recommender-system . 
## To run docker image do 
# docker run -p 52006:52006 -d rest_server_bl
docker run -v /home/beilong/project2-pv2:/ml_data -p 52006:52006 -d  beilongtang/playlists-recommender-system
