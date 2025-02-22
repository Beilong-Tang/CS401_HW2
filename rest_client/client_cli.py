import argparse
import requests

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--songs", nargs="+", required = True, help = "List of songs to send to the recommender system. ")
    p.add_argument("--hostname", default='http://localhost:52006/api/recommender', help = "The url of the recommender system.")
    return p.parse_args()

def main(args):
    headers = {"Content-Type": "application/json"}
    data = {"songs": args.songs}
    url = f"http://{args.hostname}:52006/api/recommender"
    response = requests.post(url, json=data, headers=headers)
    print(response.text)

if __name__ == "__main__":
    args = parse_args()
    main(args)
    pass
