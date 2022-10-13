# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 22:53:54 2022

@author: 52551
La funcion que regresa los precios es:
---    get_historical_klines(symbol, interval, start)
---       return "lista de precios"
pero puedes usar mejor la funcion siguiente para crear un archivo separado por comas (.csv)
---    historic_binancesymbol,start,interval, end=None )
---       return "nombre de archivo"
El nombre de las columnas en el archivo son:
    ['Open_Time','Open','High','Low','Close','Volumne','Close_Time','Quote_asset_vol',
     'Number_trades','Taker_buy_base','Taker_buy_quote','Ignore']
Siendo la numeracio correspondiente:
    [1,2,3,4,5,6,7,8,9,10,11,12]
    Siendo la de mas interes: low(4)
    Debe saber que 0 contiene la lista donde se enumeran las observaciones (la posicion 0 de esta lista 
                                                                            contiene al registro mas viejo).

En ambas fn sus parametros son:
    symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    
    interval: Biannce Kline interval; e.g 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str
    
    start: Start date string in UTC format; e.g "1 day ago UTC", "1 hours ago UTC", "dd-mm-aaaa"
    :type start: str
    
     end: optional - end date string in UTC format
    :type end: str
    
   
"""

import time
import dateparser
import pytz
import json
import csv
from datetime import datetime
from binance.client import Client
import pandas as pd


def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds
    :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str
    :return:
         None if unit not one of m, h, d or w
         None if string not in correct format
         int value of interval in milliseconds
    """
    ms = None
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    return ms


def get_historical_klines(symbol, interval, start_str, end_str=None):
    """Get Historical Klines from Binance
    See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/
    If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Biannce Kline interval
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str
    :return: list of OHLCV values
    """
    # create the Binance client, no need for api key
    client = Client("", "")

    # init our list
    output_data = []

    # setup the max limit
    limit = 1000

    # convert interval to useful value in seconds
    timeframe = interval_to_milliseconds(interval)

    # convert our date strings to milliseconds
    start_ts = date_to_milliseconds(start_str)

    # if an end time was passed convert it
    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(1)

    return output_data

def historic_binance(symbol,start,interval, end=None ):
    klines = get_historical_klines(symbol, interval, start,end)
    #print(klines)
    doc_columns = ['Open_Time','Open','High','Low','Close','Volumne',
                   'Close_Time','Quote_asset_vol','Number_trades','Taker_buy_base',
                   'Taker_buy_quote','Ignore']
    df = pd.DataFrame(klines,columns=doc_columns)
    df['Open_Time'] = pd.to_datetime(df['Open_Time'],unit = 'ms' )
    df['Close_Time'] = pd.to_datetime(df['Close_Time'],unit = 'ms' )
    filename = symbol + '_' + interval + '.csv'
    #print(f'Saving {symbol} csv file')
    #print(df.head(10))
    return df
    #df.to_csv(filename)
    #return filename
symbol = "TRXUSDT"
#         11 hours ago UTC
start = "1 day ago UTC"
end = "01-05-2022"
interval = '1h'   #Client.KLINE_INTERVAL_30MINUTE
historic_binance(symbol, start, interval)
