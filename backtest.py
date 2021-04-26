#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Contact:

import os
import sys
import time
import random

'''
stocks = {
    '2020-04-25': {
                ('000002', '万科A'): [0.0, 0, 28.83, 28.09, 29.08, 28.92]
                ('300059': '东方财富'): [0.0, 0, 28.35, 31.59, 32.04, 28.13]
                }
    '2020-04-26': {
                ('000002', '万科A'): [0.0, 0, 28.00, 27.70, 28.20, 27.60]
                ('300059', '东方财富'): [0.0, 0, 32.00, 31.02, 32.20, 30.85,...]
    }
}
'''

def test_strategy(sub_stocks: dict) -> (dict, dict):
    '''
    实现一个策略

    Parameters
    ----------
    sub_stocks: 一级key为日期
                二级key为股票id+股票名（有温度一点）
                value为该股票在该日的各项指标
                包括但不限于'日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'
    
    Return
    ------
    buy_stocks: key为股票id+股票名
                value为买入股数，买入价（或买入时间，容后再议），et al
    sell_stocks: key为股票id+股票名
                 value为卖出股数，卖出价（或卖出时间，容后再议论），et al
    '''
    random.seed(int(time.time())) # 为了让每次选出股票不同，暂时如此
    t_1 = sorted(sub_stocks.keys())[-1] # T-1日的股票，但愿T日不会被退市hhh
    buy_stocks = {k: [100, -1] for k in random.sample(sub_stocks[t_1].keys(), 3)} # 随机选三只股票默认买入100股, 即A股当前最低交易股数
    sell_stocks = {} # 暂不处理
    return buy_stocks, sell_stocks

def updateHoldingPriceofBuyingOneStock(buy_price: float, buy_shares: int, had_price: float, had_shares: int) -> (float, int):
    '''
    计算买入后持仓成本价

    Parameters
    ----------
    buy_price: 买入价，应 > 0
    buy_shares：买入股数（手数 * 每手股数） 应 > 0
    had_price：持有价
    had_shares：持有股数

    Return
    ------
    更新的持仓成本价, 持仓数
    '''
    return (had_price * had_shares + buy_price * buy_shares) / (had_shares + buy_shares), had_shares + buy_shares

def updateHoldingPriceofSellingOneStock(sell_price: float, sell_shares: int, had_price: float, had_shares: int) -> (float, int):
    pass

def countEarningsofOneStock(had_price: float, had_shares: int, closing_price: float) -> (float, float):
    '''
    股票买入，以当天收盘价计算收益率

    Parameters
    ----------
    had_price: 持有价
    had_shares: 持仓数
    closing_price：收盘价/当日结算价/卖出价

    Return
    ------
    该股票总市值, 该股票收益率（保留5位小数）
    '''
    return had_shares * closing_price, round((closing_price - had_price) / had_price, 5)

def countProit(stocks: dict, sell_stocks: dict, buy_stocks: dict, date_t_1: str, date_t: str) -> dict:
    '''

    Parameters
    ----------
    stocks: 总股票池
            一级key: 日期
            二级key: 股票id + 股票名
            value[0]: 持仓价
            value[1]: 持仓股数
            value[2:]: 该股该日其它指标
    sell_stocks: key: 股票id+股票名 value: [卖出股数, 卖出价]
    buy_stocks: key: 股票id+股票名  value: [买入股数, 买入价] 买入价小于等于0则表示以开盘价买入，买入股数小于等于0时，默认以最少交易股数买入

    Return
    ------
    更新完T日stocks股票持仓后返回该字典
    '''
    for stock, [] in sell_stocks.items():
        pass
    for stock, [t_buy_shares, t_buy_price] in buy_stocks.items():
        t_1_had_price, t_1_had_shares = stocks[date_t_1][stock][:2] # 获取T-1日持仓价和持仓股数
        if stock not in stocks[date_t]:
            continue
        if t_buy_shares <= 0: t_buy_shares = 100
        if t_buy_price <= 0: t_buy_price = float(stocks[date_t][stock][2]) # 当前设计索引2中的值，表示该股当日开盘价，暂不考虑封板买入的可能性，默认均可以开盘价买入
        had_price, had_shares = updateHoldingPriceofBuyingOneStock(t_buy_price, t_buy_shares, t_1_had_price, t_1_had_shares) # 未考虑税费
        stocks[date_t][stock][0] = had_price
        stocks[date_t][stock][1] = had_shares
        print(stock, had_price, had_shares)
    return stocks

def backtest(stocks: dict, strategy) -> dict:
    '''
    回测主函数

    Parameters
    ----------
    stocks：股票池
    strategy: 策略函数
    
    Return
    ------
    无返回值
    '''
    # 目前股票池的设计和pytorch的RNN模型的默认维度输入类似，即（时间片，股票，特征），如有需要，向量化后可以方便地转置
    # 思路是将(负无穷日，T-1日]的数据切片给策略，计算出T日（即T-1日的明天）买入卖出的股票，然后根据历史的T日行情数据，计算T日的收益
    dates = list(sorted(stocks.keys()))
    i = 1 # 第T日
    while i < len(dates):
        t_1, t = dates[i - 1], dates[i]
        buy_stocks, sell_stocks = strategy({t_1: stocks[t_1]})  # 根据策略获得T日买入卖出
                                                                            # 字典切片太慢了先用一个测试，后期向量化
        stocks = countProit(stocks, sell_stocks, buy_stocks, t_1, t) # 根据T-1日策略计算更新T日收益
        i += 1
    return stocks

def main():
    random.seed(42) # 测试阶段固定全局随机数。42是宇宙终极问题的答案
    k_history = '/Users/liji/Downloads/k_history' # 存放股票历史数据的目录
    ksFiles = [os.path.join(k_history, l) for l in os.listdir(k_history) if os.path.getsize(os.path.join(k_history, l)) > 95] # 获取文件size>95B的文件列表
    stocks = {} # 存放股票
                #一级key为date
                # 二级key为股票id + 股票名（害，暂时没支持，dbq）
                # 为了方便后续改为numpy处理，value[0]固定为该股成本价，默认为0，不影响后续计算, value[1]固定为该股当日持仓股数
                # value[0]和value[1]要么同时为0，要么同时大于0，其它情况均为异常
    for stock in random.sample(ksFiles, 10): # 测试阶段，先取10支股票试试水
        stock_code = stock[:-4].split('_')[-1] # 从文件名中获取股票id，每个元素类似k_history/k_history_688202.csv
        with open(stock, 'rt') as f:
            # 每列含义：datatime,open,close,high,low,volume,amount,zhenfu,zhangdiefu,zhangdiee,huanshoulv
            # 每列含义：'日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'
            f.readline() # 去掉标题行，之后可以改进一下，谁知道数据字段会不会进一步扩充呢
            for line in f:
                fd = line.strip().split(',')
                try:
                    stocks[fd[0]].update({stock_code: [0, 0] + fd[1:]}) # 记得加上股票名，要做有温度的赚钱机器
                except KeyError:
                    stocks[fd[0]] = {stock_code: [0, 0] + fd[1:]}
    # 好了，以上都是废话，为了导入数据用的。下面才是模块的核心代码，回测。
    stocks = backtest(stocks, test_strategy)
    lastDate = sorted(stocks.keys())[-1]
    for k, v in stocks[lastDate].items():
        print(k, v)
    # 画图
    #drawPig(stocks)
    return 0


if __name__ == '__main__':
    main()
