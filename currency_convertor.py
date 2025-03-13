from typing import List

import pandas as pd


def convert_currency_in_stock_price_df(stock_price_data: pd.DataFrame, latest: int, currency_data: pd.DataFrame,
                                       date_column_name:str,
                                       stock_price_column_to_convert:List[str], currency_to_convert_to:str):
    if stock_price_data is not None and currency_data is not None:
        if latest:
            stock_price_data = stock_price_data.merge(currency_data[[date_column_name, currency_to_convert_to]],
                                                      how='cross')
            stock_price_data[stock_price_column_to_convert] = stock_price_data[stock_price_column_to_convert].apply(
                lambda x: x * stock_price_data[currency_to_convert_to])
            stock_price_data.drop(
                columns=[date_column_name + '_x', date_column_name + '_y', currency_to_convert_to],
                inplace=True, axis=1)
            pass
        else:
            stock_price_data = stock_price_data.merge(currency_data[[date_column_name, currency_to_convert_to]],
                                                      on=date_column_name, how='left')
            if stock_price_data[currency_to_convert_to].isna().sum() > 0:
                stock_price_data[currency_to_convert_to].interpolate()

            stock_price_data[stock_price_column_to_convert] = stock_price_data[stock_price_column_to_convert].apply(
                lambda x: x * stock_price_data[currency_to_convert_to])
            stock_price_data.drop(currency_to_convert_to, inplace=True, axis=1)
            stock_price_data.drop(date_column_name, inplace=True, axis=1)

    return stock_price_data
