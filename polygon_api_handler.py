import requests
import os
from  datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class PolygonApiHandler:
    def __init__(self, log, ticker, date_to_fetch_from, date_to_fetch_till, number_of_time_frames, time_frame, adjusted,
                 sort, api_key, latest):
        self.log = log
        self.polygon_base_url = os.getenv('polygon_base_url')
        self.polygon_api_version = os.getenv('polygon_api_version')
        self.date_to_fetch_from = date_to_fetch_from
        self.date_to_fetch_till = date_to_fetch_till
        self.number_of_time_frames = number_of_time_frames
        self.time_frame = time_frame
        self.adjusted = adjusted
        self.sort = sort
        self.ticker = ticker
        self.latest= latest
        self.polygon_url = f'{self.polygon_base_url}/{self.polygon_api_version}/aggs/ticker/{self.ticker}/range/{self.number_of_time_frames}/{time_frame}/{date_to_fetch_from}/{date_to_fetch_till}?adjusted={self.adjusted}&sort={self.sort}&apiKey={api_key}' \
        if not self.latest else f'{self.polygon_base_url}/{self.polygon_api_version}/aggs/ticker/{self.ticker}/range/1/{self.time_frame}/{datetime.now().date() - timedelta(days=1)}/{datetime.now().date()}?adjusted={self.adjusted}&sort={self.sort}&apiKey={api_key}'


    def get_polygon_data(self):
        polygon_response = requests.get(self.polygon_url)

        if polygon_response.status_code == 200:
            data = polygon_response.json()['results']

            if self.latest:
                adjusted_data = pd.DataFrame(data, index=[datetime.now().date()])
            else:
                adjusted_data = pd.DataFrame(data)

            self.log.info(f"Latest quote for {self.ticker}:")
            # print(data)
        else:
            self.log.error(f"Error {polygon_response.status_code}: {polygon_response.text}")
