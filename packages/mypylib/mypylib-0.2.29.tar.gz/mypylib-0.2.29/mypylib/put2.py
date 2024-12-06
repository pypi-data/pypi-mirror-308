import traceback
import sys
import pandas as pd
import plotly.graph_objects as go
from docutils.nodes import target
from mypylib import get_ticks_between, get_ticks_between_dec, parse_date_time, price_ticks_offset_dec
from enum import Enum
import json
import datetime
from datetime import datetime
from mypylib import get_ticks_between, price_ticks_offset, get_ticks_between_dec, parse_date_time
from datetime import timedelta
import os
import finlab
from finlab import data
from finlab.dataframe import FinlabDataFrame
from colorama import init
from dataclasses import dataclass
from loguru import logger
from sqlalchemy.util import symbol

def has_recent_limit_up(close_prices, days=3):
    """檢查最近幾天（不包含當天）是否有漲停。"""
    limit_up = close_prices > close_prices.shift(1) * 1.095
    return limit_up.shift(0).rolling(days).max() == 1


def calculate_turnover_rate():
    """計算股票的週轉率。"""
    try:
        volume = data.get("price:成交股數")
        basic_info = data.get("company_basic_info")
        shares_outstanding = FinlabDataFrame(
            {
                date: basic_info.set_index("stock_id")["已發行普通股數或TDR原發行股數"]
                for date in volume.index
            }
        ).T
        return volume / shares_outstanding
    except Exception as e:
        logger.error(f"計算週轉率時發生錯誤: {e}")
        return None
def has_recent_limit_up(close_prices, days=3):
    """檢查最近幾天（不包含當天）是否有漲停。"""
    limit_up = close_prices > close_prices.shift(1) * 1.095
    return limit_up.shift(0).rolling(days).max() == 1


def calculate_turnover_rate():
    """計算股票的週轉率。"""
    try:
        volume = data.get("price:成交股數")
        basic_info = data.get("company_basic_info")
        shares_outstanding = FinlabDataFrame(
            {
                date: basic_info.set_index("stock_id")["已發行普通股數或TDR原發行股數"]
                for date in volume.index
            }
        ).T
        return volume / shares_outstanding
    except Exception as e:
        logger.error(f"計算週轉率時發生錯誤: {e}")
        return None


def put2_select_targets_low_level(threshold_volume=1200 * 1000,
                                  threshold_amount=6500 * 10000,
                                  threshold_max_capital=145e8,
                                  threshold_amp=0.06,
                                  threshold_turn_over=0.003,
                                  threshold_yesterday_co_gt_rate=-0.025,
                                  shift=0
                                  ):
    """
    put2 select everyday targets
    :param threshold_volume:
    :param threshold_amount:
    :param threshold_max_capital:
    :param threshold_amp:
    :param threshold_turn_over:
    :param threshold_yesterday_co_gt_rate: open to close rate = (close / open - 1)
    :param shift:
    :return:
    """

    finlab.login("dyrZWjkJWYCrHnLrnfj3kI7BCTw/jLBDHfsAc7RI8EwcUs/+dv70ktgffV867g9v#vip_m")
    with data.universe("TSE_OTC"):
        股本s = data.get('financial_statement:股本')
        close_prices = data.get("price:收盤價")
        open_prices = data.get("price:開盤價")
        high_prices = data.get("price:最高價")
        low_prices = data.get("price:最低價")
        成交金額s = data.get('price:成交金額')
        成交股數s = data.get("price:成交股數")
        融資今日餘額s = data.get('margin_transactions:融資今日餘額')
        融券今日餘額s = data.get('margin_transactions:融券今日餘額')
        當沖s = data.get('intraday_trading:得先賣後買當沖')

    券資比s = 融券今日餘額s / 融資今日餘額s
    周轉量s = calculate_turnover_rate()
    # XQ 振幅計算公式 = (當期最高價 - 當期最低價) * 100 / 參考價%
    振幅s = (high_prices - low_prices) / close_prices.shift(1)
    Close_to_closes = round((close_prices / close_prices.shift(1)) - 1, 5)
    # 開盤趴數s = round((open_prices / close_prices.shift(1) - 1), 5)
    # 漲跌幅s = round((close_prices / close_prices.shift(1) - 1), 5)
    # 量比s = round((成交金額s / 成交金額s.shift(1)), 3).shift(1)
    最近漲停s = has_recent_limit_up(close_prices, 1)

    # ma5s = close_prices.average(5)
    # ma10s = close_prices.average(10)
    # ma20s = close_prices.average(20)

    # gt_ma5s = close_prices > ma5s
    # gt_ma10s = close_prices > ma5s
    # gt_ma20s = close_prices > ma5s
    # bool_close_highs = close_prices >= close_prices.shift(1)
    # bool_red_ks = close_prices > open_prices

    targets_volume = 成交股數s > threshold_volume
    targets_amount = 成交金額s > threshold_amount
    targets_capital = 股本s < (threshold_max_capital / 1000)
    targets_amp = 振幅s > threshold_amp
    targets_oc_rate_yesterday = Close_to_closes > threshold_yesterday_co_gt_rate
    targets_turn_over = 周轉量s > threshold_turn_over
    targets_limit_up = 最近漲停s
    targets_day_trade = pd.isna(當沖s) == False
    targets_margin_trading = 融資今日餘額s > 1

    targets = (targets_volume &
               targets_amount &
               targets_turn_over &
               targets_day_trade &
               targets_amp &
               targets_margin_trading &
               targets_oc_rate_yesterday)

    targets_and_capital = targets & targets_capital
    common_dates = targets.index.intersection(targets_and_capital.index)
    targets_filtered = targets_and_capital.loc[common_dates]

    # These are the limit up stock of the day
    targets2 = targets_limit_up & targets_volume & targets_amount & targets_margin_trading & targets_day_trade

    targets_to_trade = targets_filtered | targets2

    return targets_to_trade.shift(shift)


def _filter_targets(targets_filtered, str_start_date='', str_end_date=''):
    """
    Low level function to filter the data with start date and end date.
    Also convert the dataframe to a list
    :param targets_filtered:
    :param str_start_date:
    :param str_end_date:
    :return:
    """
    # Filter the DataFrame based on start and end dates
    if str_start_date != '':
        targets_filtered = targets_filtered[targets_filtered.index >= str_start_date]
    if str_end_date != '':
        targets_filtered = targets_filtered[targets_filtered.index <= str_end_date]

    # Convert the values with True to a list of [symbol, date]
    result = []
    for date, row in targets_filtered.iterrows():
        true_columns = row[row == True].index.tolist()
        for symbol in true_columns:
            result.append([symbol, date.strftime('%Y-%m-%d')])
    return result


def put2_select_targets_for_tomorrow(threshold_volume=1200 * 1000,
                                     threshold_amount=6500 * 10000,
                                     threshold_max_capital=145e9,
                                     threshold_amp=0.06,
                                     threshold_turn_over=0.003,
                                     threshold_yesterday_co_gt_rate=-0.025,
                                     str_start_date='',
                                     str_end_date=''):
    """
    API to select target each day

    :param threshold_volume:
    :param threshold_amount:
    :param threshold_max_capital:
    :param threshold_amp:
    :param threshold_turn_over:
    :param threshold_yesterday_co_gt_rate: open to close rate = (close / open - 1)
    :param str_start_date:
    :param str_end_date:
    :return:
    """
    targets_to_trade = put2_select_targets_low_level(threshold_volume=threshold_volume,
                                                     threshold_amount=threshold_amount,
                                                     threshold_max_capital=threshold_max_capital,
                                                     threshold_amp=threshold_amp,
                                                     threshold_turn_over=threshold_turn_over,
                                                     threshold_yesterday_co_gt_rate=threshold_yesterday_co_gt_rate,
                                                     shift=0
                                                     )
    last_row = targets_to_trade.iloc[-1]
    true_columns = last_row[last_row == True].index.tolist()
    return true_columns

def put2_select_targets(threshold_volume=1200 * 1000,
                        threshold_amount=6500 * 10000,
                        threshold_max_capital=145e9,
                        threshold_amp=0.06,
                        threshold_turn_over=0.003,
                        threshold_yesterday_co_gt_rate=-0.025,
                        str_start_date='',
                        str_end_date=''):
    """
    API to select target each day

    :param threshold_volume:
    :param threshold_amount:
    :param threshold_max_capital:
    :param threshold_amp:
    :param threshold_turn_over:
    :param threshold_yesterday_co_gt_rate: open to close rate = (close / open - 1)
    :param str_start_date:
    :param str_end_date:
    :return:
    """
    targets_to_trade = put2_select_targets_low_level(threshold_volume=threshold_volume,
                                                     threshold_amount=threshold_amount,
                                                     threshold_max_capital=threshold_max_capital,
                                                     threshold_amp=threshold_amp,
                                                     threshold_turn_over=threshold_turn_over,
                                                     threshold_yesterday_co_gt_rate=threshold_yesterday_co_gt_rate,
                                                     shift=1
                                                     )
    list_result = _filter_targets(targets_to_trade, str_start_date, str_end_date)
    return list_result


if __name__ == '__main__':
    list_targets_to_trade = put2_select_targets_for_tomorrow(threshold_volume=1200 * 1000,
                                                             threshold_amount=6500 * 10000,
                                                             threshold_max_capital=145e8,
                                                             threshold_amp=0.06,
                                                             threshold_turn_over=0.003,
                                                             threshold_yesterday_co_gt_rate=-0.025,
                                                             str_start_date='2024-01-01',
                                                             str_end_date='')
    print(list_targets_to_trade)
    with open(f'/home/william/daily_stock_data/put2_targets-{str(datetime.today().date())}.txt', 'w') as fp:
        fp.write(' '.join(list_targets_to_trade))
    with open('/home/william/daily_stock_data/put2_targets.txt', 'w') as fp:
        fp.write(' '.join(list_targets_to_trade))


