# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 09:21:55 2022

@author: 52551

Esta archivo contiene funciones que dependen del archivo datos. Sin ese archivo 
no sera util este.

"""
from datetime import timedelta, datetime
import pandas as pd
#from Datasets import historical
from Proyecciones_estocasticas import movimiento_browniano, movimiento_geometrico
import numpy as np
from math import log




def depth_decision(df, interval):
    # df: dataframe que devuelve depth(cliente,simbolo,limite) function. columnas que debe tener: Q_venta, P_venta, Q_compra  P_compra.
    # interval: [xa, xb] // list or tupla con el valor inferior y superior para e criterio
    # return: 'long' or 'short'; como criterio  suma el total que hay para ordenes de compra y venta respectivamente.
     
    print('--------- Depth Decision ----------')
    df = df.round({'P_venta':4,'P_compra':4, 'T_venta':2, 'T_compra':2})
    df['T_venta'] = df.Q_venta*df.P_venta
    df['T_compra'] = df.Q_compra*df.P_compra
    #print(df)

    
    v = df[['Q_venta','P_venta','T_venta']][df.P_venta<interval[1]].T_venta.sum().round(2)
    c = df[['Q_compra','P_compra','T_compra']][df.P_compra>interval[0]].T_compra.sum().round(2)
    total = v+c
    pc =round( c/total, 3)
    pv =round( v/total,3)
    print('    Compra', '|', 'Venta')
    print(c, '|', v)
    print(pc, '|',pv)
    if v>c:
        print('short')
        return 'short'
    elif c>v:
        print('long')
        return 'long'
    else:
        print('neutro')
        return 'neutro'
    
    
    
def trades_historical_decision(df):
    # Esta funcion recibe un df que sale de la fucion historical_trades(cliente,simbolo, limite=1000,fromid=None)
    # return None. 
    # Pero imprime la accion que debes tomar.
    
    
    print('---------- Historical trades Decision ----------')
    ahora = datetime.now()
    tr = ahora.replace(hour=5, minute=00, second=00, microsecond=0)
    tr
    df.time = df.time - tr
    df.tail()
    print('El trade mas antiguo registrado fue hace : ', df.time.min())
    print('El trade mas reciente registrado fue hace : ', df.time.max())
    df_c = df[df.isBuyerMaker==True]
    df_v = df[df.isBuyerMaker==False]
    ct = df_c.quoteQty.sum()
    vt = df_v.quoteQty.sum()
    # Total
    total = ct+vt
    pc = ct/total
    pv = vt/total
    print('       compras', '|', 'ventas')
    print(ct, '|', vt)
    print(pc,'|', pv)
    if pv>pc: # Hay muchas ventas el precio se cae
        print('short')
        if pv>0.5:
            print('low')
        elif pv>0.6:
            print('median low')
        elif pv>0.7:
            print('median upper')
        elif pv>0.8:
            print('Hard')
        elif pv>0.9:
            print('really hard')
        else:
            print(pv)
        return 'short'
    elif pc>pv: # Hay muchas compras, el precio sube.
        print('long')
        if pc>0.9:
            print('really hard')
        elif pc>0.8:
            print('hard')
        elif pc>0.7:
            print('median upper')
        elif pc>0.6:
            print('median low')
        elif pc>0.5:
            print('low')
        else:
            print(pv)
        return 'long'
    else:
        print('neutro')
        return 'neutro'
    return None


def geometric_movement(cliente, simbolo, intervalo, t, pf, num_simulaciones = 1000000, tipo_media = False):
    hora_actual=datetime.now()
    print(hora_actual.strftime('%d-%m-%Y  %H:%M:%S'))
    df_kl = historical(cliente, simbolo, intervalo )  
    xx = df_kl.close.values
    n = len(xx)
    
    # Rendimientos
    rend_close = []
    for i in range(1, n):
        rend_close.append(log(xx[i]/xx[i-1]))
    # Datos estadisticos para la simulacion.
    if tipo_media:
        u = (xx[-1]-xx[-2])/xx[-2]
    else:
        u=np.mean(rend_close)
        
    o = np.var(rend_close)
    #print('Media = ',round(100*media,4),'%')
    #print('Media = ',round(100*u,4),'%')
    #  Precio inicial spot
    s0 = xx[-1]
    print('Precio inicial', s0)
    print(movimiento_geometrico(10, .1, .02, 3, 12, 10))
    print(u , o , t, pf, num_simulaciones )
    # movimiento_geometrico(p_inicial,media,varianza,periodos,sp,simulaciones=1000000):
    lp,proba,minimo,avg,maximo=movimiento_geometrico(p_inicial=s0,media=u,varianza=o,
                                                     periodos=t,
                                                     sp=pf,simulaciones=num_simulaciones)
    
    print('Periodos cada ',intervalo)

    for day in range(len(lp)):
        print('Periodo ',day+1,lp[day])

    print('P(st<',pf,')= ',proba)
    print('E(min[st])= ',minimo)
    print('E(max[st])= ',maximo)

    hora_esperada=hora_actual+ timedelta(minutes=t)
    print(hora_esperada.strftime('%d-%m-%Y  %H:%M:%S'))
    return None

def browniano_movement(cliente, simbolo, intervalo, t, pf, num_simulaciones = 1000000, tipo_media = False):
    hora_actual=datetime.now()
    print(hora_actual.strftime('%d-%m-%Y  %H:%M:%S'))
    df_kl = historical(cliente, simbolo, intervalo )  
    xx = df_kl.close.values
    n = len(xx)
    
    # Rendimientos
    rend_close = []
    for i in range(1, n):
        rend_close.append(log(xx[i]/xx[i-1]))
    # Datos estadisticos para la simulacion.
    if tipo_media:
        u = (xx[-1]-xx[-2])/xx[-2]
    else:
        u=np.mean(rend_close)
        
    o = np.var(rend_close)
    #print('Media = ',round(100*media,4),'%')
    #print('Media = ',round(100*u,4),'%')
    #  Precio inicial spot
    s0 = xx[-1]
    print('Precio inicial', s0)
    print(movimiento_geometrico(10, .1, .02, 3, 12, 10))
    print(u , o , t, pf, num_simulaciones )
    # movimiento_geometrico(p_inicial,media,varianza,periodos,sp,simulaciones=1000000):
    lp,proba,minimo,avg,maximo=movimiento_browniano(p_inicial=s0,media=u,varianza=o,
                                                     periodos=t,
                                                     sp=pf,simulaciones=num_simulaciones)
    
    print('Periodos cada ',intervalo)

    for day in range(len(lp)):
        print('Periodo ',day+1,lp[day])

    print('P(st<',pf,')= ',proba)
    print('E(min[st])= ',minimo)
    print('E(max[st])= ',maximo)

    hora_esperada=hora_actual+ timedelta(minutes=t)
    print(hora_esperada.strftime('%d-%m-%Y  %H:%M:%S'))
    return None

