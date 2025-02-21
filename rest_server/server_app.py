
from flask import Flask, request, jsonify
from rules_generate.model_wrapper import Model

app = Flask(__name__)
app.model = Model("rules_generate/ckpt/sup_0.025_conf_0.7_rules.ckpt")

@app.route("/api/recommend", method=["POST"])
def recommend():
    value = request.get_json()
    res = app.model(value['songs'])
    return jsonify({"recommend": res})

if __name__ == "__main__":
    app.run(port=52006)
    pass
