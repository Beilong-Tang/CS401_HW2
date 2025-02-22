from flask import Flask, request, jsonify, render_template

import argparse
p = argparse.ArgumentParser()
p.add_argument("--hostname", type = str, default = "localhost", help="rest server hostname")
p.add_argument("--web_port", type = int, default = 53000, help="port that this client runs on")
args = p.parse_args()

app = Flask("client web app")

@app.route("/")
def main():
    return render_template()
    pass


app.run(port = args.port)

