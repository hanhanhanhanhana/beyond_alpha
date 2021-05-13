'''
Author: peihan
Date: 2021-04-26 12:19:40
LastEditTime: 2021-05-13 02:24:23
LastEditors: Please set LastEditors
Description: 接口类
'''
import os
import time
import numpy as np
from . import market
from . import utils
import time
import threading
import random


result = [] # 用以临时保存多线程下载下来的数据
lock = threading.Lock() # 多线程的锁，用以控制对result中的写功能

def multi_threads_download(data_type='k_his', stock_code=None, beg=None, end=None):
    if data_type == 'k_realtime':
        df, rows, columns = market.get_k_realtime(stock_code)
    elif data_type == 'bill_realtime':
        df, rows, columns = market.get_history_bill_realtime(stock_code)
    elif data_type == 'k_his':
        df, rows, columns = market.get_k_history(stock_code, beg, end)
    elif data_type == 'bill_his':
        df, rows, columns = market.get_history_bill(stock_code)
    elif data_type == 'bill_realtime_2':
        return_list = market.get_history_bill_realtime_2(stock_code)
    global result
    # 使用finally 块来保证释放锁
    #加锁
    lock.acquire()
    try :
        #需要保证线程安全的代码
        if data_type == 'bill_realtime_2':
            result.append([stock_code, return_list])
        else:
            result.append([stock_code, df, rows, columns])
    #使用finally 块来保证释放锁
    finally :
        #修改完成，释放锁
        lock.release()

# history的数据采用多线程总是被封，服了，故history的还是用老办法吧，慢点就慢点
def history_helper(data_type='k_his', stock_codes=None, save_csv=False, save_dir=None, beg=0, end=20500101):
    '''
    @description: k_history与bill_history两个方法的helper函数
    @param {*}
    @return {*}
    '''
    s_time = time.time()
    if stock_codes is None:
        # 为了得到市场上上市股票的代码
        stock_codes = utils.read_excel()
    dict_code_as_key = {}
    dict_date_as_key = {}
    threads = []
    for code_index, stock_code in enumerate(stock_codes):
        t = threading.Thread(target=multi_threads_download, args=(data_type,stock_code, beg, end))
        t.start()
        print('code index:{},code {}'.format(code_index, stock_code))
        threads.append(t)
        time.sleep(0.05)
    # 等待所有线程完成
    for t in threads:
        t.join()
    for index in range(len(result)):
        stock_code = result[index][0]
        df = result[index][1]
        rows = result[index][2]
        columns = result[index][3]    
        if rows == []: # 股票代码有误
            continue
        dates = [int(row[0].replace('-','')) for row in rows] # 日期list，类型为int
        rows_except_date = [row[1:] for row in rows] # 列表中去除掉日期
        rows_except_date_to_numbers = np.array([np.fromstring(', '.join(row),   
                                        dtype=float, sep=', ') for row in rows_except_date]) # 形成二维array，形状为len(日期)*数据指标数
        dict_code_as_key[stock_code] = [dates, rows_except_date_to_numbers] # 二维list，第一维为日期的list，第二维为上面得到的二维array    
        # 得到dict_date_as_key的部分代码
        for i, date in enumerate(dates):
            if date not in dict_date_as_key.keys():
                dict_date_as_key[date] = [[stock_code], np.array([rows_except_date_to_numbers[i]])]
            else:
                dict_date_as_key[date][0].append(stock_code)
                feat = dict_date_as_key[date][1]
                dict_date_as_key[date][1] = np.insert(feat, feat.shape[0], rows_except_date_to_numbers[i], 0)

        if save_csv is True:
            if data_type == 'k_his':
                df.to_csv(f'{save_dir}/k_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
                print(f'股票代码：{stock_code} 的日间k线数据已保存到代码目录下的 {save_dir}/k_history_{stock_code}.csv 文件中')
            elif data_type == 'bill_his':
                df.to_csv(f'{save_dir}/bill_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
                print(f'股票代码：{stock_code} 的日间大单数据已保存到代码目录下的 {save_dir}/bill_history_{stock_code}.csv 文件中')
    
    if data_type == 'k_his':
        np.save('k_dict_code_as_key', dict_code_as_key)
        np.save('k_dict_date_as_key', dict_date_as_key)
    elif data_type == 'bill_his':
        np.save('bill_dict_code_as_key', dict_code_as_key)
        np.save('bill_dict_date_as_key', dict_date_as_key)
    print('耗时：', time.time()-s_time)
    return dict_code_as_key, dict_date_as_key


def k_history(stock_codes=None, save_csv=False, save_dir='k_history', beg=0, end=20500101):
    '''
    @description: 得到目标股票池的历史k线数据
                包括 [开盘 收盘 最高 最低 成交量 成交额 振幅 涨跌幅 涨跌额 换手率]
    @param {stock_codes: list 目标股票池，若用户未自定义，默认为市场所有股票}
    @return {dict_code_as_key: 股票代码作为key，value为一个二维list，第一维为日期的list，第二维为二维numpy array，形状为len(日期数)*数据指标数
            dict_date_as_key: 日期作为key，value为一个二维list，第一维为股票的list，第二维为二维numpy array，形状为len(股票数)*数据指标数}
    '''

    return history_helper('k_his', stock_codes, save_csv, save_dir, beg, end)

# def k_history_update()

def bill_history(stock_codes=None, save_csv=False, save_dir='bill_history'):
    '''
    @description: 得到目标股票池的历史大单数据
                包括 [主力净流入 小单净流入 中单净流入 大单净流入 超大单净流入 主力净流入占比 小单流入净占比 中单流入净占比 
                大单流入净占比 超大单流入净占比 收盘价 涨跌幅]
    @param {stock_codes: 目标股票池，若用户未自定义，默认为市场所有股票}
    @return {None}
    '''
    return history_helper('bill_his', stock_codes, save_csv, save_dir)

def realtime_helper(data_type='k_realtime', stock_codes=None, save_csv=False, save_dir=None):
    '''
    @description: k_realtime与bill_tealtime两个方法的helper函数
    @param {*}
    @return {*}
    '''
    a_time = time.time()
    if stock_codes is None:
        # 为了得到市场上上市股票的代码
        stock_codes = utils.read_excel()
    dict_code_as_key = {}
    dict_date_as_key = {}
    threads = []
    for _ in range(1000):
        for code_index, stock_code in enumerate(stock_codes):
            t = threading.Thread(target=multi_threads_download, args=(data_type,stock_code))
            t.start()
            print('code index:', code_index)
            threads.append(t)
            time.sleep(0.02)
        # 等待所有线程完成
        for t in threads:
            t.join()
        for index in range(len(result)):
            stock_code = result[index][0]
            df = result[index][1]
            rows = result[index][2]
            columns = result[index][3]
            if rows == []: # 股票代码有误
                continue
            # 得到dict_code_as_key的部分代码
            dates = [int(row[0].replace('-','').replace(':','').replace(' ','')) for row in rows] # 日期list，类型为int
            rows_except_date = [row[1:] for row in rows] # 列表中去除掉日期
            rows_except_date_to_numbers = np.array([np.fromstring(', '.join(row),   
                                            dtype=float, sep=', ') for row in rows_except_date]) # 形成二维array，形状为len(日期)*数据指标数
            dict_code_as_key[stock_code] = [dates, rows_except_date_to_numbers] # 二维list，第一维为日期的list，第二维为上面得到的二维array   
            # 得到dict_date_as_key的部分代码
            for i, date in enumerate(dates):
                if date not in dict_date_as_key.keys():
                    dict_date_as_key[date] = [[stock_code], np.array([rows_except_date_to_numbers[i]])]
                else:
                    dict_date_as_key[date][0].append(stock_code)
                    feat = dict_date_as_key[date][1]
                    dict_date_as_key[date][1] = np.insert(feat, feat.shape[0], rows_except_date_to_numbers[i], 0)

            if save_csv is True:
                if data_type == 'k_realtime':
                    df.to_csv(f'{save_dir}/k_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
                    print(f'股票代码：{stock_code} 的日间k线数据已保存到代码目录下的 {save_dir}/k_history_{stock_code}.csv 文件中')
                elif data_type == 'bill_realtime':
                    df.to_csv(f'{save_dir}/bill_history_realtime_{stock_code}.csv', encoding='utf-8-sig', index=None)
                    print(f'股票代码：{stock_code} 的实时大单数据已保存到代码目录下的 {save_dir}/bill_history_realtime_{stock_code}.csv 文件中')

        if data_type == 'k_realtime':
            np.save('realtime_k_dict_code_as_key', dict_code_as_key)
            np.save('realtime_k_dict_date_as_key', dict_date_as_key)
        elif data_type == 'bill_realtime':
            np.save('realtime_bill_dict_code_as_key', dict_code_as_key)
            np.save('realtime_bill_dict_date_as_key', dict_date_as_key)

        if len(df) >= 240:
            print('已收盘')
            break
        # 每隔一分钟爬一次数据
        time.sleep(50)
    # print(time.time()-a_time)
    return dict_code_as_key, dict_date_as_key

def k_history_realtime(stock_codes=None, save_csv=False, save_dir='k_history_realtime'):
    '''
    @description: 实时得到当天目标股票池的k线数据
                包括 [未知 价格 未知 未知 成交量 成交额 均价]
                每60s获取并记录一次
    @param {stock_codes: 目标股票池，若用户未自定义，默认为市场所有股票}
    @return {None}
    '''
    return realtime_helper('k_realtime', stock_codes, save_csv, save_dir)
    
def bill_history_realtime(stock_codes=None, save_csv=False, save_dir='bill_history_realtime'):
    '''
    @description: 实时得到当天目标股票池的大单数据
                包括 [主力净流入 小单净流入 中单净流入 大单净流入 超大单净流入]
                每60s获取并记录一次
    @param {stock_codes: 目标股票池，若用户未自定义，默认为市场所有股票}
    @return {None}
    '''
    return realtime_helper('bill_realtime', stock_codes, save_csv, save_dir)

def bill_history_realtime_2(stock_codes=None):
    '''
    @description: 实时得到当天目标股票池的大单等数据，较bill_history_realtime更全面
    @param {stock_codes: 目标股票池，若用户未自定义，默认为市场所有股票}
    @return {None}
    '''
    data_type = 'bill_realtime_2'
    if stock_codes is None:
        # 为了得到市场上上市股票的代码
        stock_codes = utils.read_excel()
    dict_code_as_key = {}
    # dict_date_as_key = {}
    # for _ in range(1000):
    threads = []
    for code_index, stock_code in enumerate(stock_codes):
        t = threading.Thread(target=multi_threads_download, args=(data_type,stock_code))
        t.start()
        threads.append(t)
        print('code index:', code_index)
        time.sleep(0.005)
    # 等待所有线程完成
    for t in threads:
        t.join()
    for index in range(len(result)):
        stock_code = result[index][0]
        result_list = result[index][1]
        # if len(result_list) == 0: # 股票代码有误
        #     continue
        # 得到dict_code_as_key的部分代码
        dict_code_as_key[stock_code] = result_list
    
    # # 每隔一分钟爬一次数据
    # time.sleep(50)
    # print(time.time()-a_time)
    return dict_code_as_key

# # 未加多线程的原始方法
# def history_helper(data_type='k_his', stock_codes=None, save_csv=False, save_dir=None, beg=0, end=20500101):
#     '''
#     @description: k_history与bill_history两个方法的helper函数
#     @param {*}
#     @return {*}
#     '''
#     if stock_codes is None:
#         # 为了得到市场上上市股票的代码
#         stock_codes = utils.read_excel()
#     dict_code_as_key = {}
#     dict_date_as_key = {}
#     k = 0
#     for stock_code in stock_codes:
#         print(k)
#         if data_type == 'k_his':
#             df, rows, columns = market.get_k_history(stock_code, beg, end)
#         elif data_type == 'bill_his':
#             df, rows, columns = market.get_history_bill(stock_code)
            
#         if rows == []: # 股票代码有误
#             continue
#         dates = [int(row[0].replace('-','')) for row in rows] # 日期list，类型为int
#         rows_except_date = [row[1:] for row in rows] # 列表中去除掉日期
#         rows_except_date_to_numbers = np.array([np.fromstring(', '.join(row),   
#                                         dtype=float, sep=', ') for row in rows_except_date]) # 形成二维array，形状为len(日期)*数据指标数
#         dict_code_as_key[stock_code] = [dates, rows_except_date_to_numbers] # 二维list，第一维为日期的list，第二维为上面得到的二维array    
#         # 得到dict_date_as_key的部分代码
#         for i, date in enumerate(dates):
#             if date not in dict_date_as_key.keys():
#                 dict_date_as_key[date] = [[stock_code], np.array([rows_except_date_to_numbers[i]])]
#             else:
#                 dict_date_as_key[date][0].append(stock_code)
#                 feat = dict_date_as_key[date][1]
#                 dict_date_as_key[date][1] = np.insert(feat, feat.shape[0], rows_except_date_to_numbers[i], 0)

#         if save_csv is True:
#             if data_type == 'k_his':
#                 df.to_csv(f'{save_dir}/k_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
#                 print(f'股票代码：{stock_code} 的日间k线数据已保存到代码目录下的 {save_dir}/k_history_{stock_code}.csv 文件中')
#             elif data_type == 'bill_his':
#                 df.to_csv(f'{save_dir}/bill_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
#                 print(f'股票代码：{stock_code} 的日间大单数据已保存到代码目录下的 {save_dir}/bill_history_{stock_code}.csv 文件中')
#         time.sleep(0.1)
#         k+=1
    
#     if data_type == 'k_his':
#         np.save('k_dict_code_as_key', dict_code_as_key)
#         np.save('k_dict_date_as_key', dict_date_as_key)
#     elif data_type == 'bill_his':
#         np.save('bill_dict_code_as_key', dict_code_as_key)
#         np.save('bill_dict_date_as_key', dict_date_as_key)
    
#     return dict_code_as_key, dict_date_as_key


# 未加多线程的原始方法，1000只股票耗时为200s左右
# def realtime_helper(data_type='k', stock_codes=None, save_csv=False, save_dir=None):
#     '''
#     @description: k_realtime与bill_tealtime两个方法的helper函数
#     @param {*}
#     @return {*}
#     '''
#     a_time = time.time()
#     if stock_codes is None:
#         # 为了得到市场上上市股票的代码
#         stock_codes = utils.read_excel()
#     dict_code_as_key = {}
#     dict_date_as_key = {}
#     # for _ in range(1000):
#     for code_index, stock_code in enumerate(stock_codes):
#         print('code index:', code_index)
#         if data_type == 'k':
#             df, rows, columns = market.get_k_realtime(stock_code)  
#         elif data_type == 'bill':
#             df, rows, columns = market.get_history_bill_realtime(stock_code)
            
#         if rows == []: # 股票代码有误
#             continue
#         # 得到dict_code_as_key的部分代码
#         dates = [int(row[0].replace('-','').replace(':','').replace(' ','')) for row in rows] # 日期list，类型为int
#         rows_except_date = [row[1:] for row in rows] # 列表中去除掉日期
#         rows_except_date_to_numbers = np.array([np.fromstring(', '.join(row),   
#                                         dtype=float, sep=', ') for row in rows_except_date]) # 形成二维array，形状为len(日期)*数据指标数
#         dict_code_as_key[stock_code] = [dates, rows_except_date_to_numbers] # 二维list，第一维为日期的list，第二维为上面得到的二维array   
#         # 得到dict_date_as_key的部分代码
#         for i, date in enumerate(dates):
#             if date not in dict_date_as_key.keys():
#                 dict_date_as_key[date] = [[stock_code], np.array([rows_except_date_to_numbers[i]])]
#             else:
#                 dict_date_as_key[date][0].append(stock_code)
#                 feat = dict_date_as_key[date][1]
#                 dict_date_as_key[date][1] = np.insert(feat, feat.shape[0], rows_except_date_to_numbers[i], 0)

#         if save_csv is True:
#             if data_type == 'k':
#                 df.to_csv(f'{save_dir}/k_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
#                 print(f'股票代码：{stock_code} 的日间k线数据已保存到代码目录下的 {save_dir}/k_history_{stock_code}.csv 文件中')
#             elif data_type == 'bill':
#                 df.to_csv(f'{save_dir}/bill_history_realtime_{stock_code}.csv', encoding='utf-8-sig', index=None)
#                 print(f'股票代码：{stock_code} 的实时大单数据已保存到代码目录下的 {save_dir}/bill_history_realtime_{stock_code}.csv 文件中')
#         # time.sleep(0.1)

#     # if data_type == 'k':
#     #     np.save('realtime_k_dict_code_as_key', dict_code_as_key)
#     #     np.save('realtime_k_dict_date_as_key', dict_date_as_key)
#     # elif data_type == 'bill':
#     #     np.save('realtime_bill_dict_code_as_key', dict_code_as_key)
#     #     np.save('realtime_bill_dict_date_as_key', dict_date_as_key)
#     print(time.time()-a_time)
#     # if len(df) >= 240:
#     #     print('已收盘')
#     #     break
#     # time.sleep(30)
    
#     return dict_code_as_key, dict_date_as_key
