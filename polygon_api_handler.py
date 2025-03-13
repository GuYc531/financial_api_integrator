import requests
import os
from  datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class PolygonApiHandler:
    def __init__(self, log, ticker, date_to_fetch_from, date_to_fetch_till, number_of_time_frames, time_frame, adjusted,
                 sort, api_key,date_column_name, latest):
        self.log = log
        self.date_column_name = date_column_name
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
        if not api_key:
            self.log.error("API key not found! Make sure it's set in your .env file")
            raise ValueError("API key not found! Make sure it's set in your .env file")
        self.polygon_url = f'{self.polygon_base_url}/{self.polygon_api_version}/aggs/ticker/{self.ticker}/range/{self.number_of_time_frames}/{time_frame}/{date_to_fetch_from}/{date_to_fetch_till}?adjusted={self.adjusted}&sort={self.sort}&apiKey={api_key}' \
        if  not self.latest else f'{self.polygon_base_url}/{self.polygon_api_version}/aggs/ticker/{self.ticker}/range/1/{self.time_frame}/{datetime.now().date() - timedelta(days=1)}/{datetime.now().date()}?adjusted={self.adjusted}&sort={self.sort}&apiKey={api_key}'


    def get_polygon_data(self):
        polygon_response = requests.get(self.polygon_url)
        adjusted_data = None

        if polygon_response.status_code == 200:
            data = polygon_response.json()['results']

            adjusted_data = pd.DataFrame(data)
            adjusted_data['timestamp'] = adjusted_data['t'].apply(lambda epoch: datetime.fromtimestamp(epoch / 1000))
            adjusted_data[self.date_column_name] = adjusted_data['timestamp'].apply(lambda x: str(x.date()))
            self.log.info(f"successfully got data for ticker {self.ticker}:")
        else:
            self.log.error(f"Error {polygon_response.status_code}: {polygon_response.text}")

        return adjusted_data