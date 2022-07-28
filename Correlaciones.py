# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 08:44:56 2022

@author: 52551

Este archivo muestra la grafica de dispersion entre dos activos
"""
import matplotlib.pyplot as plt
from Datasets import historical
import pandas as pd 

def correlacion(cliente,simbolo1, simbolo2, tipo=0):
    '''
    Parameters
    ----------
    cliente : TYPE: 
        DESCRIPTION.es el cliente de binance, lea el readme para mas info
    simbolo1 : TYPE str
        DESCRIPTION. Simbolo de criptomoneda
    simbolo2 : TYPE str
        DESCRIPTION. Simbolo de criptomoneda
    tipo : TYPE, optional int
        DESCRIPTION. The default is 0. 0 return correlacion pearson.
                     1 devuelve correlacion de spearman.
                     2 correlacion de Kendall

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    
    intervalo = '5m'
    lim = 1000
    df1 = historical(cliente, simbolo1, intervalo, lim)
    df2 = historical(cliente, simbolo2, intervalo, lim)
    df = pd.DataFrame(data={simbolo2:df2.close.values, simbolo1:df1.close.values})
    # 'kendall', 'spearman', 'pearson'
    if tipo==0:
        df_cor = df.corr('pearson')
    elif tipo==1:
        df_cor = df.corr('spearman')
    elif tipo==2:
        df_cor = df.corr('kendall')
    else:
        print('tipo invlaido')
        return None
    plt.scatter(df[[simbolo1]], df[[simbolo2]])
    plt.xlabel(simbolo1)
    plt.ylabel(simbolo2)
    plt.title('Grafico de dispersión')
    
    return df_cor.iloc[1,0]

def top(cliente, simbolo= 'BTCUSDT', top=3, positivo = True, market='Future'):
    '''
    
    Parameters
    ----------
    cliente : TYPE
        DESCRIPTION.
    simbolo : TYPE, optional str
        DESCRIPTION. The default is 'BTCUSDT'.
    top : TYPE, optional int
        DESCRIPTION. The default is 3.
    positivo : TYPE, optional bool
        DESCRIPTION. The default is True. Para mostrar los mas correlacionados positivamente.
    market : TYPE, optional
        DESCRIPTION. The default is 'Future'. tambien puedes usar Spot, pero usar Spot
                     es muy costoso, por lo que puede tardar mas de 30 min en ejecutarse. 

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    if market == 'Spot':
        info = cliente.get_all_tickers()
        df = pd.DataFrame(info )
        simbolos = df.symbol.values
        df_close = pd.DataFrame()
        
        c = 0
        for s in simbolos:
            c+=1
            df_kl = historical(cliente, s, '1h' )
            close = df_kl.close
            close.name= s
        
            df_close = pd.concat([df_close, close], axis=1)
         
            
        df_corr = df_close.corr()
        if positivo:
            return df_corr[[simbolo]].sort_values(by=simbolo ,ascending=False).iloc[1:top+1]
        else:
            return df_corr[[simbolo]].sort_values(by=simbolo ,ascending=True).iloc[1:top+1]
        
    elif market == 'Future':
        info = cliente.futures_symbol_ticker()
        df = pd.DataFrame(info)
        simbolos = df.symbol.values
        df_close = pd.DataFrame()
        
        c = 0
        for s in simbolos:
            c+=1
            df_kl = historical(cliente, s, '1h', market='Future' )
            close = df_kl.close
            close.name= s
       
            df_close = pd.concat([df_close, close], axis=1)
         
        df_corr = df_close.corr()
        if positivo:
            return df_corr[[simbolo]].sort_values(by=simbolo ,ascending=False).iloc[1:top+1]
        else:
            return df_corr[[simbolo]].sort_values(by=simbolo ,ascending=True).iloc[1:top+1]
    
    else:
        print('Market invalido')
        return None

