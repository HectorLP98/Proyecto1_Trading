# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 10:07:45 2022

@author: 52551
"""
from random import choices, random, gauss
from statistics import mean, variance
from math import sqrt, log, exp
import numpy as np 

def trayectoria_mov_geo(u, o, t, p0,sp):
    '''
    Parameters
    ----------
    u : TYPE: float
        DESCRIPTION. mean of the rendimiento de criptocurency
    o : TYPE: float
        DESCRIPTION: desviation standard of the  rend criptocurrency
    t : TYPE: int
        DESCRIPTION. Cantidad de pe
    p0 : TYPE: float
        DESCRIPTION. Precio inicial del activo, se asume el precio actual del activo
    sp : TYPE: float
        DESCRIPTION: Precio al que queremos saber la probabilidad de que llegue

    Returns
    -------
    l : TYPE: list
        DESCRIPTION: lista de precios en los proximos t-periodos
    proba : TYPE: float
        DESCRIPTION. # Probabilidad que el precio esperado sea menor que Sp
    '''
    l = [p0]
    p = p0
    cuenta = 0
    for i in range(t):
        p = p*exp((u-(o**2/2))+o*gauss(0,1))   #gauss(0,1))  #normal_acot())
        if p <= sp:
            cuenta += 1
        l.append(p)
        # Proba de que el precio caiga del actual.
    proba = cuenta/t
    return l, proba

def movimiento_geometrico(p_inicial,media,varianza,periodos,sp,simulaciones=1000000):
    '''
    Parameters
    ----------
    p_inicial : TYPE: float
        DESCRIPTION: Precio inicial del activo, se asume el precio actual del activo
    media : TYPE: float
        DESCRIPTION. mean of the criptocurency
    varianza : TYPE: float 
        DESCRIPTION. Variance of the criptocurrency
    periodos : TYPE: int
        DESCRIPTION. Number of periods in the future to estimate
    sp : TYPE: float Precio al que queremos saber la probabilidad de que llegue
        DESCRIPTION.
    simulaciones : TYPE, optional int
        DESCRIPTION. The default is 1000000. Numero de simulaciones a realizar, para mayor eficiencia

    Returns
    -------
    lp : TYPE: list
        DESCRIPTION. Precio promedio esperado para el tiempo t0, si t=2, len(lp)=2, por lo tanto lp[0] contiene
                el precio esperado en el periodo t=1
    prob : TYPE: float
        DESCRIPTION. Probabilidad de que el precio esperado al tiempo t0 sea menor que sp
    minimo : TYPE: float
        DESCRIPTION. Precio minimo esperado al tiempo t
    avg : TYPE: float
        DESCRIPTION. Precio promedio esperado al tiempo t

    '''
    # Lista precio promedio
    la = []
    # Lista probabilidad bear
    lb = []
    # Lista precio minimo
    lm = []
    # Lista precio Maximo
    lM = []
    # Lista precio spot al tiempo t
    ls = []
    
    
    # Simulacion Monte Carlo
    for i in range(simulaciones):
        l,proba = trayectoria_mov_geo(u=media, o=sqrt(varianza),t= periodos, p0=p_inicial, sp=sp)
        
    # MARCADOR DE SIMULACION para saber el progreso, solo para visualizar el tiempo faltante
        if i>0 and i % 100000 == 0:
            print(i)
 
        m = np.mean(l)
        mini = min(l)
        maxi = max(l)
                   
        la.append(m)
        lb.append(proba)
        lm.append(mini)
        lM.append(maxi)
        ls.append(l)
    
    prob = mean(lb)
    avg = mean(la)
    minimo = mean(lm)
    maximo=mean(lM)
    # Lista promedio de precios por dia
    lp=[]
  #  print('len',(ls))
    for k in range(periodos):
        lt=[]
        for j in range(len(ls)):
            lt.append(ls[j][k])
        lp.append(round(mean(lt),6))
         
    return lp,prob,minimo,avg,maximo

def trayectoria_mov_brow(u, o, t, p0,sp):
    l = [p0]
    p = p0
    cuenta = 0
    for i in range(t):
        p = p*exp(u+o*gauss(0,1))   #gauss(0,1))  #normal_acot())
        if p <= sp:
            cuenta += 1
        l.append(p)
        # Proba de que el precio caiga del actual.
    proba = cuenta/t
    return l, proba

def movimiento_browniano(p_inicial,media,varianza,periodos,sp,simulaciones=2000000):
    '''
    Parameters
    ----------
    p_inicial : TYPE: float
        DESCRIPTION: Precio inicial del activo, se asume el precio actual del activo
    media : TYPE: float
        DESCRIPTION. mean of the criptocurency
    varianza : TYPE: float 
        DESCRIPTION. Variance of the criptocurrency
    periodos : TYPE: int
        DESCRIPTION. Number of periods in the future to estimate
    sp : TYPE: float Precio al que queremos saber la probabilidad de que llegue
        DESCRIPTION.
    simulaciones : TYPE, optional int
        DESCRIPTION. The default is 1000000. Numero de simulaciones a realizar, para mayor eficiencia

    Returns
    -------
    lp : TYPE: list
        DESCRIPTION. Precio promedio esperado para el tiempo t0, si t=2, len(lp)=2, por lo tanto lp[0] contiene
                el precio esperado en el periodo t=1
    prob : TYPE: float
        DESCRIPTION. Probabilidad de que el precio esperado al tiempo t0 sea menor que sp
    minimo : TYPE: float
        DESCRIPTION. Precio minimo esperado al tiempo t
    avg : TYPE: float
        DESCRIPTION. Precio promedio esperado al tiempo t

    '''
    # Lista precio promedio
    la = []
    # Lista probabilidad bear
    lb = []
    # Lista precio minimo
    lm = []
    # Lista precio Maximo
    lM = []
    # Lista precio spot al tiempo t
    ls = []
    
    
    # Simulacion MC
    for i in range(simulaciones):
        l,proba = trayectoria_mov_brow(media, sqrt(varianza), periodos, p_inicial,sp)
        
    # MARCADOR DE SIMULACION
        if i>0 and i % 100000 == 0:
            print(i)
           
 
        m = np.mean(l)
        mini = min(l)
        maxi = max(l)
                   
        la.append(m)
        lb.append(proba)
        lm.append(mini)
        lM.append(maxi)
        ls.append(l)
    
    
    prob = mean(lb)
    avg = mean(la)
    minimo = mean(lm)
    maximo=mean(lM)
    # Lista promedio de precios por dia
    lp=[]
  #  print('len',(ls))
    for k in range(periodos):
        lt=[]
        for j in range(len(ls)):
            lt.append(ls[j][k])
        lp.append(round(mean(lt),6))
         
    return lp,prob,minimo,avg,maximo