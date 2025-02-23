#!/bin/bash


## To build the image
docker build -t beilongtang/playlists-recommender-system:0.1 . 
## To run docker image do 
docker run -v /home/beilong/project2-pv2:/ml_data -p 52006:52006 -d  beilongtang/playlists-recommender-system:0.1
