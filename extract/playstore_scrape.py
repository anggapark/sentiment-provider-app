import os

import pandas as pd
import numpy as np

from google_play_scraper import app, Sort, reviews
from pymongo import MongoClient
from pprint import pprint


def playstore_scrape(
    id: str,
    count=100,
    lang: str = "id",
    filename="output.csv",
    country: str = "id",
):

    result, continuation_token = reviews(
        id,
        lang=lang,  # defaults to 'en'
        country=country,  # defaults to 'us'
        sort=Sort.NEWEST,  # defaults to Sort.NEWEST
        count=count,  # defaults to 100
    )

    result, _ = reviews(
        id,
        continuation_token=continuation_token,  # defaults to None(load from the beginning)
    )
    results_df = pd.json_normalize(result)
    results_df.to_csv(filename, index=False)


if __name__ == "__main__":
    ids_app = {
        "com.telkomsel.telkomselcm": "MyTelkomsel-v2",
        "com.apps.MyXL": "MyXL-v2",
        "com.pure.indosat.care": "MyIM3-v2",
        "com.smartfren": "MySF-v2",
    }
    for id, appname in ids_app.items():
        result = playstore_scrape(
            id=id,
            filename=appname,
            count=800,
        )
        print(result)
