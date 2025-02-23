## Test cases


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
The time for CD is about `3min9s`, and the server is never down.