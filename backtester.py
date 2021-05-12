#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Contact:

import os
import sys
import time
import numpy as np

from dataloader import MarketLoader
from broker import Broker
from strategy import Strategy

class Backtester:
    '''
    '''

    def __init__(self, time_sep: int, decision_sep: int, mkter: MarketLoader, broker: Broker, strategy: Strategy):
        self.time_sep = time_sep if isinstance(time_sep, int) else None                 # 每次决策需要多久时间片的数据（单位为个数）
        self.decision_sep = decision_sep if isinstance(decision_sep, int) else None     # 两次决策间隔时间（单位为个数）
        #self.mkter = mkter if isinstance(mkter, MarketLoader) else None                # 市场信息，需根据策略决定
        self.mkter = 1
        self.broker = broker if isinstance(broker, Broker) else None                    # 股票经理人
        self.strategy = strategy if isinstance(strategy, Strategy) else None            # 策略类
        if None in (self.time_sep, self.decision_sep, self.mkter, self.broker, self.strategy):
            print("Input parameters were wrong", file=sys.stderr)
            sys.exit(1)
        ''' 暂时不用
        # 将时间换算为个数
        if self.mkter.period == 'min':
            self.tick = 4 * 60      # 四个小时的交易时间，9:30-11:30，13:00-15:00，意味着240条数据为一天
        elif self.mkter.period == 'day':
            self.tick = 1           # 每天的数据只有一条
        '''

    def backtest(self):
        #dict_code_as_key, dict_date_as_key = self.mkter.load_k_history() # 三维np.array, dataloader提供转换成三维np.array和字典的方法比较好
        #all_time = len(dict_date_as_key)
        # 导入数据
        d = np.load('dict_date_as_key.npy', allow_pickle=True).item()
        sorted_date = sorted(list(d.keys()))
        # 回测主循环, 根据决策时间，决策所需过往多少时间的数据这两个值来切片
        for t in range(self.time_sep, len(sorted_date), self.decision_sep):
            # 切片: [决策时间-时间片长度: 决策时间)
            stocks = {sorted_date[i]: d[sorted_date[i]] for i in range(t - self.time_sep, t)}
            # 将tm1和t1的数据转换为二维字典
            tm1 = {d[sorted_date[t-1]][0][i]: i for i in range(len(d[sorted_date[t-1]][0]))}
            t1 = {d[sorted_date[t]][0][i]: i for i in range(len(d[sorted_date[t]][0]))}
            # 根据时间片长度内数据执行策略，获取T日订单
            self.strategy(stocks)
            # 将股票转换为输入格式的字典
            self.broker.run(tm1, t1, {'t1': d[sorted_date[t]][1], 'tm1': d[sorted_date[t-1]][1]}, self.strategy.orders, show=True)
            # 清空订单
            self.strategy.zero_orders()
        self.broker.show()
