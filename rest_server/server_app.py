import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from flask import Flask, request, jsonify
from rules_generate.model_wrapper import Model




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
