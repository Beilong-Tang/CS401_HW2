import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from flask import Flask, request, jsonify
import pickle
import random
import itertools
from typing import List

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
app.model = Model("../rules_generate/ckpt/sup_0.025_conf_0.7_rules.ckpt")

@app.route("/api/recommender", methods=["POST"])
def recommend():
    print(request)
    value = request.get_json()
    print(value)
    res = app.model(value['songs'])
    return jsonify({"recommend": res})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=52006)
    pass
