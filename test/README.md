## Test cases


### 1. Test Replicas 

I tested the replicas changed from `3` to `2` running the `test_replicas_num_change.sh`
to output the replicas num every one second. _The detailed result can be found at `test_replicas_num_change.log`_.

The result is like 
```
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

It can be estimated that the time it takes for argoCD to build the project is about `3min38s`, and the server is nerver down.


### 2. Test dataset updates

In this test, we simulated the action of updating a dataset by modifying the 
environment varialbe `DATA_PATH` in `ml-generator` in `deployment.yaml`. 
We can choose between `"/ml_data/2023_spotify_ds1.csv"` and `"/ml_data/2023_spotify_ds2.csv"`. Note that all the datasets
should be put in `/home/beilong/project2-pv2` for access because of PVC. 

After modification, I then run the `keep_request.sh` to keep sending request to the server. And if the dataset change is triggered 
then the `ml_generate` should also be triggered, leading to an updated `model_date` in the response.

Note that, in order to let k8s rerun the rules_generator task, a specific identifier should be added at the back of `name`  
to make sure that k8s builds a new pod for this task. Otherwise, nothing is going to happen.
