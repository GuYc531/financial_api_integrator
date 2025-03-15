# financial_api_integrator

## Overview

This project is designed to fetch, process, and analyze stock price data along with currency conversion data. It integrates with external APIs (such as Polygon.io for stock price data and Frankfurter API for currency conversion rates) to provide analytical capabilities, particularly around the conversion of stock prices between different currencies.

The goal of this project is to provide an easy-to-use interface for fetching stock price data, applying currency conversions, and performing analytical queries to make business decisions based on accurate, up-to-date financial data.

---

## Features

- **Fetch Stock Price Data**: Fetch stock price data for a given ticker symbol, within a date range, and at various granularities (minute, hour, day).
- **Fetch Currency Conversion Rates**: Fetch daily currency conversion rates for various currencies.
- **Currency Conversion**: Automatically adjust stock prices based on the conversion rate to any target currency.
- **Data Merging**: Merge stock price data with the corresponding currency rates based on date for conversion.
- **Error Handling**: Log errors and handle potential issues with API calls, such as invalid API keys or data fetch failures.
- **Logging**: Detailed logging of all steps including API fetch status, data processing, and errors.

---

## Technologies Used

- **Python 3.x**
- **Pandas** for data manipulation
- **Requests** for API integration
- **Logging** for error tracking
- **Environment Variables** for sensitive information storage (API keys)
- **Polygon.io API** for stock price data
- **Frankfurter API** for currency conversion rates

---

## Installation

### Prerequisites

1. Python 3.6+ installed.
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt


## Architecture

```text
the pipeline constructed from:
 1. polygon_api_handler - the main data fetcher of this pipeline,
    fetches stock price data from polygon api.
 2. frankfurter_api_handler - the secondary data fetcher of this pipeline,
    fetches currency data.  
 3. currency_convertor - the transformation logic of the stock price data based on selected currency.
 4. config_handler and logger for clean structure.
 
The Env variable 'latest' is set for deciding whether we get latest data from both APIs or history data.
```
### data modelling approach

```text
In general, i think its best to save stock price data even if we dont have the selected currency so the pipeline 
is designed to save the price data even if the currency api fails.

If the stock price data API fails to respond then i wnt to fail the execution.

I chose to design the tables to currency_table and stock_prices tables:
1. currency one big table because either we can get from the API currency by date( 1 observation per day) 
    or latest (which is probably changing mid day).
2. For the stock_price_data_{time_frame}_table , i will create a table for each selected time frame selected to fetch from the API 
    `time_frame` env variable.
I chose this modeling because i think it will give a solid solution to convert stock prices and present them in analytics tool.

there may be a better complicated solution to handle the currency data, 
but based on my understanding of the API this solution is good.

across the pipeline there are error handling on the API handlers and on the user given variables (as mush as we can..)

```

## Configurations & schedualing
```textmate
I will schedule this pipeline to run in Airflow, to provide an orchastration and logging,
in addition i will sends the logs to log factory (e.g. Splunk, Grafana ..) to provide 
with more solid dashboard to monitor the pipeline.

In general, i think that we can schedule this pipline to run at every want-able way 
if provided with resources and data base, it suppose to be scalabel and seamless within
different stock, currencies and time frames selected.
 
to configure the pipeline:
1. ticker - env variable sets the ticker to fetch
2. currency_to_convert_to - env variable set the currency to convert to
3. base_currency - sets the currency to convert from to currency_to_convert_to
```
## Examples

### Stock data handler:
```python
stock_fetcher = StockPriceFetcher(
    ticker="AAPL",
    date_to_fetch_from="2025-01-01",
    date_to_fetch_till="2025-01-31",
    number_of_time_frames=1,
    time_frame="minute",
    adjusted=True,
    sort="asc",
    api_key="your_polygon_api_key",
    date_column_name="date",
    latest=False)
 stock_data = stock_fetcher.get_polygon_data()

 ```
### currency data handler:
```python
currency_fetcher = CurrencyFetcher(
    ticker="USD",
    date_to_fetch_from="2025-01-01",
    date_to_fetch_till="2025-01-31",
    base_currency="USD",
    date_column_name="date",
    latest=False
)
currency_data = currency_fetcher.get_frankfurter_data()

```

### Convert stock price based on currency:
```python
converted_data = convert_currency_in_stock_price_df(
    stock_price_data=stock_data,
    latest=False,
    currency_data=currency_data,
    date_column_name="date",
    stock_price_column_to_convert=["price"],
    currency_to_convert_to="EUR"
)

```