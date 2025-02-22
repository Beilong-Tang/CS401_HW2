from flask import Flask, request, jsonify, render_template
import requests

import argparse
p = argparse.ArgumentParser()
p.add_argument("--hostname", type = str, default = "localhost", help="rest server hostname")
p.add_argument("--web_port", type = int, default = 53000, help="port that this client runs on")
args = p.parse_args()

app = Flask("client web app")

@app.route("/")
def main():
    return render_template("index.html", hostname=args.hostname)

@app.route("/get_recommendation", methods = ["POST"])
def get_recommendation():
    value = request.get_json() # the return value
    url = f"http://{args.hostname}:52006/api/recommender"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=value, headers=headers)
    return response.text


app.run('0.0.0.0', port = args.web_port)

