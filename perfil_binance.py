#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 09:49:15 2022

@author: hector
"""
from binance.client import Client


def cuenta_binance(cliente):
# Esta funcion regresa el estado de la cuenta
# Uso: cliente='real' (or 'demo')
# return cliente
    #print('obj: dict')
    #print('keys:[makerCommission, takerCommission, buyerCommission,\
    #      sellerCommission, canTrade, canWithdraw, canDeposit, updateTime,\
    #          accountType, balances, permissions]')
    if cliente == 'real':
        api_key = 'ipi88s3VmD1wuQ6JcjmklTGpg9zp7a34jwk5lRMkqxC0H7DlIHCV2YhK167cLtgL'
        
        sec_k = 'yZ1uzCORm5Q1gWzbqHTor2PAXNwYyne47jv2uLpJBCbClUJTvtNy1x9UfXqL3jhY'
        
        cliente = Client(api_key,sec_k)
        
        print('---------Cuenta real----------')
        
        # Detalles de mi cuenta
        acount_real = cliente.get_account()
        
        # Balance
        #print(acount_real['balances'])
        #print(type(acount_real))
        #print(acount_real.keys())
        return cliente
    
    elif cliente == 'demo' : 
        print('------------Cuenta demo---------------')
        key_demo = 'PrDLIgZpA2DIGNfnnrMxjLBWrFiI3XRIgRcC5sgpjkXLf75qSoYfBy3mww9TMXxN'
        secret_demo = '1jEJjChiaSFTDQS9GdapNmQAhxX5plV1tF80hTwaedLN48JfLd19NQCS7gqEtAzH'
        #client_demo = Spot(base_url='https://testnet.binance.vision',key=key_demo,secret=secret_demo)
        client = Client(key_demo,secret_demo,testnet=True)
        acount_demo = client.get_account()
        #print(acount_demo['balances'])
        return client
    else:
        print('Parametro invalido, pruebe "real" or "demo"')
        return None
    