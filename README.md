# CS401_HW2

This repository serves as the HW2 to CS401:Cloud Computing at Duke Kunshan University.

[github](https://github.com/Beilong-Tang/CS401_HW2)

## Introduction

In this assignment, I created a CICD playlist recommendation system using flask, docker. k8s and argoCD. I made a 
backend rules generator to generate recommendation rules on a dataset. I then made a frontend flask application to 
load the backend model and make predictions. I also made a [web client](http://128.110.96.29:53000/) for testing. 
I built docker containers for both applications and used k8s for automation. Finally I used the argoCD to 
automatically build the k8s apps when the repository configuration changes. I tested the application and confirmed 
that CICD is doing its job and the server is never offline.

I will then give a detailed explanation and instruction for each part, following a discussion on the test cases.

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
The ArgoCD YAML file can be found at `argocd.yaml`



## Discussion of CICD test cases

Please refer `test/README.md` for more details. All the test scripts are located at `test/`. 

### 1. Test Replicas 

I tested the replicas changed from `3` to `2` running the `test_replicas_num_change.sh`
to output the replicas num every one second. _The detailed result can be found at `test_replicas_num_change.log`_.

The result is like 
```log
[2025-02-22 06:31:33]
NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
playlist-recommender-deployment   3/3     3            3           3h11m
-------------------
[2025-02-22 06:31:34]
NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
playlist-recommender-deployment   3/3     3            3           3h11m
-------------------
[2025-02-22 06:31:35]
NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
playlist-recommender-deployment   3/3     3            3           3h11m
.
.
.
[2025-02-22 06:35:01]
NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
playlist-recommender-deployment   2/2     2            2           3h14m
-------------------
[2025-02-22 06:35:02]
NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
playlist-recommender-deployment   2/2     2            2           3h14m
-------------------
[2025-02-22 06:35:04]
NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
playlist-recommender-deployment   2/2     2            2           3h14m

```

It can be estimated that the time it takes for argoCD to build the project is about __3min38s__, and the server is nerver down.


### 2. Test dataset updates

In this test, we simulated the action of updating a dataset by modifying the 
environment varialbe `DATA_PATH` in `ml-generator` in `deployment.yaml`. 
We can choose between `"/ml_data/2023_spotify_ds1.csv"` and `"/ml_data/2023_spotify_ds2.csv"`. Note that all the datasets
should be put in `/home/beilong/project2-pv2` for access because of PVC. 

After modification, I then run 

```shell
bash keep_request.sh test_dataset_update.log
```

to keep sending request to the server. And if the dataset change is triggered 
then the `ml_generate` should also be triggered, leading to an updated `model_date` in the response.

Note that, in order to let k8s rerun the rules_generator task, a specific identifier should be added at the back of `name`  
to make sure that k8s builds a new pod for this task. Otherwise, nothing is going to happen.

The result looks like:

```log
[2025-02-22 07:45:25]
{"model_date":"2025-02-22 18:49:47.660202","songs":["Tunnel Vision","Congratulations","Bad and Boujee (feat. Lil Uzi Vert)","Slippery (feat. Gucci Mane)","goosebumps","Mask Off","XO TOUR Llif3","HUMBLE."],"version":"0.2"}
[2025-02-22 07:45:26]
{"model_date":"2025-02-22 18:49:47.660202","songs":["Tunnel Vision","Congratulations","Bad and Boujee (feat. Lil Uzi Vert)","Slippery (feat. Gucci Mane)","goosebumps","Mask Off","XO TOUR Llif3","HUMBLE."],"version":"0.2"}
[2025-02-22 07:45:28]
{"model_date":"2025-02-22 18:49:47.660202","songs":["Tunnel Vision","Congratulations","Bad and Boujee (feat. Lil Uzi Vert)","Slippery (feat. Gucci Mane)","goosebumps","Mask Off","XO TOUR Llif3","HUMBLE."],"version":"0.2"}
.
.
.
[2025-02-22 07:47:28]
{"model_date":"2025-02-22 22:47:25.285238","songs":["DNA.","Congratulations","Bad and Boujee (feat. Lil Uzi Vert)","T-Shirt","Slippery (feat. Gucci Mane)","goosebumps","XO TOUR Llif3","Mask Off","HUMBLE."],"version":"0.2"}
[2025-02-22 07:47:29]
{"model_date":"2025-02-22 22:47:25.285238","songs":["DNA.","Congratulations","Bad and Boujee (feat. Lil Uzi Vert)","T-Shirt","Slippery (feat. Gucci Mane)","goosebumps","XO TOUR Llif3","Mask Off","HUMBLE."],"version":"0.2"}
[2025-02-22 07:47:30]
{"model_date":"2025-02-22 22:47:25.285238","songs":["DNA.","Congratulations","Bad and Boujee (feat. Lil Uzi Vert)","T-Shirt","Slippery (feat. Gucci Mane)","goosebumps","XO TOUR Llif3","Mask Off","HUMBLE."],"version":"0.2"}
```

We can tell that the `songs` and `model_date` changes at `[2025-02-22 07:47:28]`. My server will actually check if the model checkpoint is updated
for every request, and used the most updated version. Therefore, we can tell that the CD time is about __2min3s__, and the server is never down.

### 3. Test Container update (code update)

For this test, I did a code modification by updating the `rest_server/server_app.py` to return an extra feild `updated` for response. 
I then build a new docker image and updated it to the docker hub.

```shell
cd ../rest_server
docker build -t beilongtang/playlists-recommender-system:0.4 . 
docker push beilongtang/playlists-recommender-system:0.4
```

After that, I updated the `deployment.yaml` to use the newest docker image for the `playlist-recommender-deployment`. 
After commiting my changes, I ran 

```shell
bash keep_request.sh test_container_update.log
```

to check if the server gives me back the new model. 

The result looks like

```log
[2025-02-22 18:16:56]
{"model_date":"2025-02-22 22:47:25.285238","songs":["DNA.","Congratulations","Bad and Boujee (feat. Lil Uzi Vert)","T-Shirt","Slippery (feat. Gucci Mane)","goosebumps","XO TOUR Llif3","Mask Off","HUMBLE."],"version":"0.2"}
.
.
.
[2025-02-22 18:20:05]
{"model_date":"2025-02-22 22:47:25.285238","songs":["DNA.","Congratulations","Bad and Boujee (feat. Lil Uzi Vert)","T-Shirt","Slippery (feat. Gucci Mane)","goosebumps","XO TOUR Llif3","Mask Off","HUMBLE."],"updated":"yes","version":"0.4"}
```

We can see that at `[2025-02-22 18:20:05]`, there is an extra field `updated` in the response, which means that the k8s uses the updated container. 
The time for CD is about __3min9s__, and the server is never down.

## Conclusion

Overall, for each test cases, the CD takes about 3mins, and the application never remains offline.

