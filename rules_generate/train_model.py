# This module trains the model of recommendation system 
import pandas as pd
from fpgrowth_py import fpgrowth
import pickle ## Used for saving objects
import time
from datetime import timedelta


DATA_PATH="/home/datasets/spotify/2023_spotify_ds1.csv"
MIN_SUP_RATIO=0.025
MIN_CONF=0.7

csv = pd.read_csv(DATA_PATH)
## Consult ChatGPT 
## This combines all the tracks corresponding to the
itemSetList = csv.groupby('pid')['track_name'].apply(lambda x: list(set(x))).tolist()

print(f"Running FP Growth Algorithm using Min Sup Ratio {MIN_SUP_RATIO} and Min Conf {MIN_CONF}")
time_start = time.time()
freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=0.1, minConf=0.5)
time_finish = time.time() - time_start
print(f"Finished FP Growth with time {str(timedelta(seconds=int(time_finish)))}")


## Save them to the ckpt
with open(f"ckpt/sup_{MIN_SUP_RATIO}_conf_{MIN_CONF}_freq.ckpt", "wb") as file: 
    pickle.dump(freqItemSet, file)


with open(f"ckpt/sup_{MIN_SUP_RATIO}_conf_{MIN_CONF}_rules.ckpt", "wb") as file: 
    pickle.dump(rules, file)
