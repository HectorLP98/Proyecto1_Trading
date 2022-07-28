# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 09:29:13 2022

@author: 52551
"""

import pandas as pd
from datetime import datetime, time, timedelta

def historical(cliente, simbolo, intervalo, limite = 500, market='Spot'):
    '''
    simbolo = 'TRXUSDT'
    intervalo = '30m', '1h'
    limite = 8 # Default = 500, max = 1000
    market = 'Spot' or 'Future'
    
    '''
    if market == 'Spot':
        data = cliente.get_klines(symbol=simbolo, interval=intervalo,
                               limit = limite ) 
        df = pd.DataFrame(data, columns=['open_time',
                    'open',
                    'high',
                    'low' ,
                    'close',
                    'volumen' ,
                    'close_time' ,
                    'quote_asset_v' ,
                    'num_trades', 
                    'taker_buy_base_asset_v',
                    'taker_buy_quote_asset_v',
                    'ignore'])
        df.open_time = pd.to_datetime(df.open_time,unit = 'ms' ) -  timedelta(hours=5)
       
        df.close_time = pd.to_datetime(df.close_time, unit='ms') - timedelta(hours = 5)
    
        df = df.astype({'low': 'float64', 'open': 'float', 'close':'float', 'quote_asset_v': 'float',
                   'high':'float', 'volumen':float, 'num_trades':int, 
                   'taker_buy_base_asset_v':float
                   , 'taker_buy_quote_asset_v':float})
        return df 
    elif market == 'Future':
        info = cliente.futures_klines(symbol = 'TRXUSDT', interval = '30m', limit = 2)

        df = pd.DataFrame(data=info, columns=['open_time',
                            'open',
                            'high',
                            'low' ,
                            'close',
                            'volumen' ,
                            'close_time' ,
                            'quote_asset_v' ,
                            'num_trades', 
                            'taker_buy_base_asset_v',
                            'taker_buy_quote_asset_v',
                            'ignore'])
        df.open_time = pd.to_datetime(df.open_time,unit = 'ms' ) -  timedelta(hours=5)
        
        df.close_time = pd.to_datetime(df.close_time, unit='ms') - timedelta(hours = 5)
        
        df = df.astype({'low': 'float64', 'open': 'float', 'close':'float', 'quote_asset_v': 'float',
                   'high':'float', 'volumen':float, 'num_trades':int, 
                   'taker_buy_base_asset_v':float
                   , 'taker_buy_quote_asset_v':float})
        return df
        
# PRofundidad de mercado
def depth(cliente,simbolo,limite):
# from perfil_binance import cuenta_binance as cb
# client = Client('', '')
# cliente = cb('demo')
# simbolo = 'TRXUSDT'
# limite = 100 hasta 5,000
# return un df con la cantidad de dolares y el precio del activo.

    
    depth = cliente.get_order_book(symbol=simbolo, limit=limite)
    lp_c = []
    lp_v = []
    l_c = []
    l_v = []
    for key, val in depth.items():
        if key == 'bids': # Compras
            for j in val:
                lp_c.append(float(j[0]))
                l_c.append(round(float(j[1]),2))
           # print(key,len(val))
        elif key == 'asks': # Ventas
           # print(key,len(val))
            for j in val:
               # print(j)
                lp_v.append(float(j[0]))
                l_v.append(round(float(j[1]),2))
    df = pd.DataFrame({'Q_venta': l_v,
                       'P_venta': lp_v,
                       'Q_compra':l_c,
                       'P_compra':lp_c})
    df.tail()
    return df



# isBuyerMaker: true => la operación fue iniciada por el lado de la venta; el lado de la compra ya era el libro de pedidos. es compra
# isBuyerMaker: false => la operación fue iniciada por el lado comprador; el lado de la venta ya era el libro de pedidos     es venta                                                                          False = orden de mercado. no pasa por el libro.
# qty: cantidad de cripto 
# quoteQty: Total de compra en USDT
def historical_trades(cliente,simbolo, ago, limite=1000,fromid=None):
# Esta funcion retorna un df que contiene el historial de trades
# from perfil_binance import cuenta_binance as cb
# client = Client('', '')
# cliente = cb('demo')
# simolo = 'TRXUSDT'
# ago = 5 ; los ultimos trades de hace 5 minutos, este parametro es entero y representa minutos unicamente
# limite = 1 hasta 1000
# fromid = probar cualquier id.
# # isBuyerMaker: true => es compra
# isBuyerMaker: false => es venta
    '''
    trades = cliente.get_historical_trades(symbol=simbolo, limit=limite, fromid=fromid)
    df = pd.DataFrame(trades)
    df['price'] = df['price'].astype('float16')
    df['qty'] = df['qty'].astype('float64')
    df['time'] = pd.to_datetime(df['time'],unit = 'ms' )
    df['quoteQty'] = df['quoteQty'].astype('float64')
    df.drop(columns='isBestMatch', axis = 1, inplace=True)
    df = df.round({ 'qty':1, 'quoteQty':3})
'''  
    
    trades = cliente.get_historical_trades(symbol='BTCUSDT', limit=1000 )# , fromId =dfp.id.min()-1000)
    dfp = pd.DataFrame(trades)
    dfp['time'] = pd.to_datetime(dfp['time'],unit = 'ms' )

    
    ahora = datetime.now()
    tb = ahora - timedelta(minutes = ago) + timedelta(hours=5)
    date_min = dfp.time.min()


   # print(dfp.shape, '*********')
    #print('Time buscado ', tb)
    while date_min>tb:
        trades = cliente.get_historical_trades(symbol='BTCUSDT', limit=1000 , fromId =dfp.id.min()-1000)
        dfpp = pd.DataFrame(trades)
        dfpp['time'] = pd.to_datetime(dfpp['time'],unit = 'ms' )
        #dfp.time = df.time - timedelta(hours=5)
        date_min = dfpp.time.min()
        #print(dfpp.time.min())
        dfp = dfp.append(dfpp, ignore_index = True)
    dfp['price'] = dfp['price'].astype('float16')
    dfp['qty'] = dfp['qty'].astype('float64')
    dfp['quoteQty'] = dfp['quoteQty'].astype('float64')
    dfp.drop(columns='isBestMatch', axis = 1, inplace=True)
    dfp = dfp.round({ 'qty':1, 'quoteQty':3})
    
    return dfp