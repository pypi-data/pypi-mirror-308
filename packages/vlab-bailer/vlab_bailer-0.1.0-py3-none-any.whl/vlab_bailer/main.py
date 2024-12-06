import argparse
import os
from time import sleep
from typing import Optional

import pandas as pd
import requests
from tqdm import tqdm

BOTSERVER_URL = os.getenv("VLAB_BOTSERVER_URL", "https://fly-botserver.vlab.digital")


def bailout(user, page, form):
    dat = {
        "event": {"type": "bailout", "value": {"form": form}},
        "user": str(user),
        "page": str(page),
    }

    return dat


def post_bail(dat):
    sleep(1)
    res = requests.post(f"{BOTSERVER_URL}/synthetic", json=dat)
    return res


def main(path: str, limit: Optional[int], start: Optional[int]):
    df = pd.read_csv(
        path, dtype={"user": "string", "page": "string", "shortcode": "string"}
    )

    try:
        bails = [bailout(r.user, r.page, r.shortcode) for _, r in df.iterrows()]
    except AttributeError:
        print(
            "Error: Your csv is not the right format. "
            "Please use the headers: user,page,shortcode"
        )
        return

    bails = bails[start:limit]

    for b in tqdm(bails):
        try:
            post_bail(b)
        except Exception as e:
            print(e)


# ended at 2722
def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, required=True)
    parser.add_argument("-l", "--limit", type=int)
    parser.add_argument("-s", "--start", type=int)
    args = parser.parse_args()
    main(args.path, args.limit, args.start)
