'''
Author: your name
Date: 2021-05-10 22:35:05
LastEditTime: 2021-05-11 00:26:34
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\beyond_alpha\test_broker.py
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np

from broker import Broker
from order import Order
from dataloader import MarketLoader

def main():

    loader = MarketLoader(20210421, 20210422, 'day')
    d = {}
    f = np.load('../files/k_dict_date_as_key.npy', allow_pickle=True).item()
    tm1, t1, tp1 = 20210421, 20210422, 20210423
    l = [0, 0]
    for i in range(len(f[tm1][0])):
        if f[tm1][0][i] == 'SZ000001':
            l[0] = f[tm1][1][i].tolist()
        if f[tm1][0][i] == 'SZ000002':
            l[1] = f[tm1][1][i].tolist()
    d[tm1] = {
        'SZ000001': l[0],
        'SZ000002': l[1]
    }
    l = [0, 0]
    for i in range(len(f[t1][0])):
        if f[t1][0][i] == 'SZ000001':
            l[0] = f[t1][1][i].tolist()
        if f[t1][0][i] == 'SZ000002':
            l[1] = f[t1][1][i].tolist()
    d[t1] = {
        'SZ000001': l[0],
        'SZ000002': l[1]
    }
    l = [0, 0]
    for i in range(len(f[tp1][0])):
        if f[tp1][0][i] == 'SZ000001':
            l[0] = f[tp1][1][i].tolist()
        if f[tp1][0][i] == 'SZ000002':
            l[1] = f[tp1][1][i].tolist()
    d[tp1] = {
        'SZ000001': l[0],
        'SZ000002': l[1]
    }
    print(d)
    broker = Broker()
    orders = []
    orders.append(Order(1, 'b', 'SZ000001', 1000, 23.2, False, '20210422000000', ''))
    orders.append(Order(2, 's', 'SZ000001', 500, 23.2, False, '20210422000000', ''))
    orders.append(Order(3, 'b', 'SZ000001', 1000, 21.2, False, '20210422000000', ''))
    # orders.append(Order(1, 'b', 'SZ000002', 200, 30.1, False, '20210422000000', ''))
    # orders.append(Order(2, 's', 'SZ000002', 500, 29.0, False, '20210422000000', ''))
    # orders.append(Order(3, 'b', 'SZ000002', 900, 28.9, False, '20210422000000', ''))
    broker.run({'tm1': d[tm1], 't1': d[t1]}, orders, show=True)
    orders = []
    # broker.get_pending_orders()
    orders.append(Order(4, 'b', 'SZ000001', 1000, 23.6, False, '20210422000000', ''))
    orders.append(Order(5, 's', 'SZ000001', 500, 23.6, False, '20210422000000', ''))
    orders.append(Order(6, 'b', 'SZ000001', 1000, 23.6, False, '20210422000000', ''))
    broker.run({'tm1': d[t1], 't1': d[tp1]}, orders, show=True)
    return 0

if __name__ == '__main__':
    main()
