import requests
import os
from datetime import date, datetime
from logger import Logger
import logging
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class FrankfurterApiHandler:
    def __init__(self, log, ticker, date_to_fetch_from, date_to_fetch_till,
                 base_currency,date_column_name, latest):
        self.date_column_name = date_column_name
        self.frankfurter_base_url = os.getenv('frankfurter_base_url')
        self.frankfurter_api_version = os.getenv('frankfurter_api_version')
        self.date_to_fetch_from = date_to_fetch_from
        self.date_to_fetch_till = date_to_fetch_till
        self.base_currency = base_currency
        self.latest = latest
        self.frankfurter_url = f"{self.frankfurter_base_url}/{self.frankfurter_api_version}/{self.date_to_fetch_from}..{self.date_to_fetch_till}?base={self.base_currency}" \
        if not latest else f"{self.frankfurter_base_url}/{self.frankfurter_api_version}/latest?base={self.base_currency}"
        self.ticker = ticker
        self.log = log

    def get_frankfurter_data(self):
        frankfurter_response = requests.get(self.frankfurter_url)
        adjusted_data = None

        if frankfurter_response.status_code == 200:
            data = frankfurter_response.json()['rates']
            if isinstance(list(data.values())[0], float):
                adjusted_data = pd.DataFrame({str(datetime.now().date()): data}).transpose()

            else:
                adjusted_data = pd.DataFrame(data).transpose()

            adjusted_data[self.date_column_name] = adjusted_data.index

            self.log.info(f"successfully got data for ticker {self.ticker}:")
        else:
            self.log.error(f"Error {frankfurter_response.status_code}: {frankfurter_response.text}")

        return adjusted_data