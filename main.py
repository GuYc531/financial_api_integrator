from datetime import datetime

import requests
import os
import pandas as pd
import datetime
import logging
from logger import Logger
from frankfurter_api_handler import FrankfurterApiHandler
from polygon_api_handler import PolygonApiHandler
from currency_convertor import convert_currency_in_stock_price_df
from dotenv import load_dotenv

load_dotenv()

# האם זה צריך לרוץ כיחידה אחת? משמע בסוף יוזר מתשאל את הפייפליין ומקבל תשובה או שליפה בכל פעם שיש שימוש
log = Logger(name=__name__, log_file="logs/app.log", level=logging.DEBUG).get_logger()

api_key = os.getenv('POLYGON_API_KEY')

date_column_name = os.getenv('date_column_name')
ticker = os.getenv('ticker')
date_to_fetch_from = os.getenv('date_to_fetch_from')
date_to_fetch_till = os.getenv('date_to_fetch_till')
sort = os.getenv('sort')
time_frame = os.getenv('time_frame')
number_of_time_frames = os.getenv('number_of_time_frames')
adjusted = os.getenv('adjusted')
polygon_api_version = os.getenv('polygon_api_version')
base_currency = os.getenv('base_currency')
currency_to_convert_to = os.getenv('currency_to_convert_to')
stock_price_column_to_convert = [i for i in list(os.getenv('stock_price_column_to_convert')) if i != ',']
log.info("all env vars initialized correctly")

latest = False if int(os.getenv('latest')) == 0 else True
# if latest not in ['True', 'False']:
#     log.error(f"env var 'latest' = {latest} must be one of 'True' or 'False' ")
#     raise ValueError(f"env var 'latest' = {latest} must be one of 'True' or 'False' ")

frankfurter_handler = FrankfurterApiHandler(log=log,
                                            base_currency=base_currency,
                                            date_to_fetch_from=date_to_fetch_from,
                                            date_to_fetch_till=date_to_fetch_till,
                                            ticker=ticker,
                                            date_column_name=date_column_name,
                                            latest=latest)

currency_data = frankfurter_handler.get_frankfurter_data()

polygon_api_handler = PolygonApiHandler(log=log,
                                        date_to_fetch_from=date_to_fetch_from,
                                        date_to_fetch_till=date_to_fetch_till,
                                        ticker=ticker,
                                        time_frame=time_frame,
                                        adjusted=adjusted,
                                        number_of_time_frames=number_of_time_frames,
                                        date_column_name=date_column_name,
                                        sort=sort, api_key=api_key, latest=latest)

stock_price_data = polygon_api_handler.get_polygon_data()

# after API checks
if currency_to_convert_to not in currency_data.columns:
    log.debug(f"currency to convert {currency_to_convert_to} is invalid leaving the currency as {base_currency}")
for col in stock_price_column_to_convert:
    if col not in stock_price_data.columns:
        log.error(
            f"column {col} not in stock_price_data columns to convert based on selected currency please select one of"
            f"{str(stock_price_data.columns)}")

if stock_price_data is not None and currency_data is None:
    log.debug(f"only have stock price data and not currency data so will save currency base on {base_currency}")

final_stock_price_data = convert_currency_in_stock_price_df(stock_price_data=stock_price_data,
                                                            latest=latest,
                                                            currency_data=currency_data,
                                                            currency_to_convert_to=currency_to_convert_to,
                                                            date_column_name=date_column_name,
                                                            stock_price_column_to_convert=stock_price_column_to_convert)

# final_stock_price_data(['v', 'vw', 'o', 'c', 'h', 'l', 't', 'n', 'timestamp'], dtype='object')

# currency_data(['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP',
#        'HKD', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR',
#        'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'SEK', 'SGD', 'THB', 'TRY', 'ZAR',
#        'Date'],
#       dtype='object')

print(0)
