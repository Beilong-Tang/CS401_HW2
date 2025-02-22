# This module trains the model of recommendation system 
import pandas as pd
from fpgrowth_py import fpgrowth
import pickle ## Used for saving objects
import time
from datetime import timedelta
import os 


DATA_PATH= os.getenv("DATA_PATH", "/home/datasets/spotify/2023_spotify_ds1.csv")
MIN_SUP_RATIO=0.06
MIN_CONF=0.3

csv = pd.read_csv(DATA_PATH)
## Consult ChatGPT 
## This combines all the tracks corresponding to the
itemSetList = csv.groupby('pid')['track_name'].apply(lambda x: list(set(x))).tolist()
print(f"len playlist: {len(itemSetList)}")

print(f"Running FP Growth Algorithm using Min Sup Ratio {MIN_SUP_RATIO} and Min Conf {MIN_CONF}")
time_start = time.time()
freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=MIN_SUP_RATIO, minConf=MIN_CONF)
time_finish = time.time() - time_start
print(f"Finished FP Growth with time {str(timedelta(seconds=int(time_finish)))}")


with open(f"/ml_data/model.ckpt", "wb") as file: 
    pickle.dump(rules, file)
