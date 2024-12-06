from pymongo import MongoClient
import pandas as pd
import json
import pytz
from datetime import datetime, timedelta, date
from ..utils import StatsDateTime, StatsProcessor
import yaml
from ..utils import shared_client 


class StatsFetcher:

    def __init__(self, ticker):
        self.ticker = ticker
        self.db = shared_client[
            "company"]  # Replace with your database name
        self.collection = self.db["twse_stats"]

        self.timezone = pytz.timezone("Asia/Taipei")

        self.target_metric_dict = {
            'value': ['value'],
            'value_and_percentage': ['value', 'percentage'],
            'percentage': ['percentage'],
            'grand_total': ['grand_total'],
            'grand_total_values': ['grand_total', 'grand_total_percentage'],
            'grand_total_percentage': ['grand_total_percentage'],
            'growth': [f'YoY_{i}' for i in [1, 3, 5, 10]],
            'grand_total_growth': [f"YoY_{i}" for i in [1, 3, 5, 10]]
        }


    def prepare_query(self):
        return [
            {
                "$match": {
                    "ticker": self.ticker,
                }
            },
        ]

    def collect_data(self, start_date, end_date):
        pipeline = self.prepare_query(start_date, end_date)

        fetched_data = list(self.collection.aggregate(pipeline))

        return fetched_data[0]

    def str_to_datetime(self, date_str):
        year, month, day = [int(num) for num in date_str.split("-")]

        date = datetime.strptime(date_str, "%Y-%m-%d")
        date = self.timezone.localize(date)

        season = (month - 1) // 3 + 1

        return StatsDateTime(date, year, month, day, season)
