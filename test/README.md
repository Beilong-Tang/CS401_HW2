## Test cases


### 1. Test Replicas 

I tested the replicas changed from `3` to `2` running the `test_replicas_num_change.sh`
to output the replicas num every one second.

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


### 2. Test 



