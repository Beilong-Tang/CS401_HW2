# CS401_HW2

This repository serves as the HW2 to CS401:Cloud Computing at Duke Kunshan University.

[github](https://github.com/Beilong-Tang/CS401_HW2)


## Part 1 Software Components

### Playlist Rules Generator

Please refer to `rules_generate/train_model.py` for more details.

I created a rule generator using `FP-Growth`.  
For dataset, you can download from [here](https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/). 

Before running, you can specify `DATA_PATH` in your os environment. 
Please note that the model output will be saved to `/ml_data/model.ckpt`

Note that for the purpose of speed, I chose `MIN_SUP_RATIO` to be 0.06 and `MIN_CONF` to be 0.3. 

### Rest API Server

Please refer to `rest_server/server_app.py` for more details.

I created a model wrapper to wrap the model generated from the rules generator. 
For every request, I checked if the `/ml_data/model.ckpt` is updated and used the 
updated one. 

### Rest API Client

Please refer to `rest_client/` for more details. 

I made a CLI program `client_cli.py` which takes a hostname and a list of songs to send to the 
server. 

__For extra credits__. I made a client web app in Flask that sends request to the server at `web_app`.py
This 



## Notes

SSH Server: `ssh beilong@apt029.apt.emulab.net`
