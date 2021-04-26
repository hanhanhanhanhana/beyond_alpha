'''
Author: peihan
Date: 2021-04-26 12:19:40
LastEditTime: 2021-04-26 17:53:37
LastEditors: Please set LastEditors
Description: 接口类
'''
import os
import time
from . import market
from . import utils


def k_history(stock_codes=None, save_dir='k_history', beg='0', end='20500101'):
    '''
    @description: 得到目标股票池的历史k线数据
                包括 [开盘 收盘 最高 最低 成交量 成交额 振幅 涨跌幅 涨跌额 换手率]
    @param {stock_codes: 目标股票池，若用户未自定义，默认为市场所有股票}
    @return {None}
    '''
    if stock_codes is None:
        # 为了得到市场上上市股票的代码
        stock_codes = utils.read_excel()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for stock_code in stock_codes:
        df = market.get_k_history(stock_code, beg, end)
        df.to_csv(f'{save_dir}/k_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
        print(f'股票代码：{stock_code} 的日间k线数据已保存到代码目录下的 {save_dir}/k_history_{stock_code}.csv 文件中')
        time.sleep(0.5)

def bill_history(stock_codes=None, save_dir='bill_history'):
    '''
    @description: 得到目标股票池的历史大单数据
                包括 [主力净流入 小单净流入 中单净流入 大单净流入 超大单净流入 主力净流入占比 小单流入净占比 中单流入净占比 
                大单流入净占比 超大单流入净占比 收盘价 涨跌幅]
    @param {stock_codes: 目标股票池，若用户未自定义，默认为市场所有股票}
    @return {None}
    '''
    if stock_codes is None:
        # 为了得到市场上上市股票的代码
        stock_codes = utils.read_excel()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for stock_code in stock_codes:
        df = market.get_history_bill(stock_code)
        df.to_csv(f'{save_dir}/bill_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
        print(f'股票代码：{stock_code} 的日间大单数据已保存到代码目录下的 {save_dir}/bill_history_{stock_code}.csv 文件中')
        time.sleep(0.5)

def k_history_realtime(stock_codes=None, save_dir='k_history_realtime'):
    '''
    @description: 实时得到当天目标股票池的k线数据
                包括 [未知 价格 未知 未知 成交量 成交额 均价]
                每60s获取并记录一次
    @param {stock_codes: 目标股票池，若用户未自定义，默认为市场所有股票}
    @return {None}
    '''
    if stock_codes is None:
        # 为了得到市场上上市股票的代码
        stock_codes = utils.read_excel()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for _ in range(1000):
        for stock_code in stock_codes:
            df = market.get_k_realtime(stock_code)
            df.to_csv(f'{save_dir}/k_history_realtime_{stock_code}.csv', encoding='utf-8-sig', index=None)
            print(f'股票代码：{stock_code} 的实时k线数据已保存到代码目录下的 {save_dir}/k_history_realtime_{stock_code}.csv 文件中')
            if len(df) >= 240:
                print('已收盘')
                break
            time.sleep(60)

def bill_history_realtime(stock_codes=None, save_dir='bill_history_realtime'):
    '''
    @description: 实时得到当天目标股票池的大单数据
                包括 [主力净流入 小单净流入 中单净流入 大单净流入 超大单净流入]
                每60s获取并记录一次
    @param {stock_codes: 目标股票池，若用户未自定义，默认为市场所有股票}
    @return {None}
    '''
    if stock_codes is None:
        # 为了得到市场上上市股票的代码
        stock_codes = utils.read_excel()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for _ in range(1000):
        for stock_code in stock_codes:
            df = market.get_history_bill_realtime(stock_code)
            df.to_csv(f'{save_dir}/bill_history_realtime_{stock_code}.csv', encoding='utf-8-sig', index=None)
            print(f'股票代码：{stock_code} 的实时大单数据已保存到代码目录下的 {save_dir}/bill_history_realtime_{stock_code}.csv 文件中')
            if len(df) >= 240:
                print('已收盘')
                break
            time.sleep(60)