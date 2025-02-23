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

For example, 

```shell
python3 client_cli.py --songs "Watch Out" "Black Beatles" --hostname <hostname to the backend server>
```

#### Rest Web Client (Extra Credit)

__For extra credits__. I made a client web app in Flask that sends request to the server at `web_app`.py
This app requires the `hostname` of the backend recommendation server and a `web_port` which the app will be run on.

My web client server is publically avaiable at [http://128.110.96.29:53000/](http://128.110.96.29:53000/). 

Note that since the backend server might not be publically avaialbe, I made a workaround by dealing the request 
to the backend server to go through the web client application server, and the client will send a request to backend 
server's internal address. The client web app backend then sends it back to the frontend. 

## Part 2 CICD

### 1. Create Docker image

For _ML container_, refer to `rules_generate/start_docker` for building the docker image as well as running it in a container. 

For _frontend container_, refer to `rest_server/start_docker.sh`. 

Note that I added a volume mounting host path `/home/beilong/project2-pv2` to `/ml_data`. This ensures both containers can write and 
read files from the same directory.


### 2. Configure k8s deployment and service

Please refer to `deployment.yaml` for deployment.
In this deployment file, I created two deployment configuration. One is for frontend playlist system, and other one is 
for ml generator. Note that for ml generator, since it only needs to run once when the dataset is updated. I make the type to 
be a Job instead of Deployment because a Job only runs once while the Deployment runs infinite times. This two 
configs use the PVC config specified below for reading and writing data. 

Please refore to `service.yaml` for service.

#### Sharing the model over a Persistent Volume

Please refer to `persist_volume_chain.yaml` for pvc config.

### 3. Configure Automatic Deployment in ArgoCD

Please refer to `argocd.sh` for the command to create argoCD that checks the update of the repository. 
The ArgoCD YAML file can be found at 


## Notes

SSH Server: `ssh beilong@apt029.apt.emulab.net`
