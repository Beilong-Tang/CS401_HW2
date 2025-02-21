import os
import pickle
import random
import itertools
import datetime
from typing import List

from flask import Flask, request, jsonify

class Model:
    def __init__(self, rules_ckpt:str):
        self.model = pickle.load(open(rules_ckpt, "rb"))
    
    def _check_exist(self, data):
        for _e in self.model:
            if _e[0] == set(data):
                return list(_e[1])
        return None
    
    def __call__(self, data: List[str]):
        """
        data: List of songs
        """
        ret_val = []
        ## Iterate through the data 
        for r in range(len(data), 0, -1):
            combinations = list(itertools.combinations(data, r))
            for comb in combinations:
                for _e in self.model:
                    if all(elem in list(_e[0]) for elem in list(comb)):
                        # return list(_e[1])
                        for e in list(_e[1]):
                            if e not in ret_val:
                                ret_val.append(e)
        if len(ret_val) != 0:
            return ret_val
        return list(random.choice(self.model)[1])

app = Flask(__name__)

MODEL_CKPT = "/ml_data/model.ckpt"

app.model = Model(MODEL_CKPT)
app.modified = os.path.getmtime(MODEL_CKPT)
app.version = os.getenv("APP_VERSION", "unknown")

@app.route("/api/recommender", methods=["POST"])
def recommend():
    value = request.get_json()
    res = app.model(value['songs'])
    modified = os.path.getmtime(MODEL_CKPT)
    if modified != app.modified:
        ## Reload the model
        app.model = Model(MODEL_CKPT)
        app.modified = modified
    modified_str = datetime.datetime.fromtimestamp(app.modified).strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"songs": res, "version": app.version, 'model_date': modified_str})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=52006)
    pass
