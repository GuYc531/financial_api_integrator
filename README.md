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