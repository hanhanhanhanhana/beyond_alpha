'''
Author: peihan
Date: 2021-04-25 16:40:05
LastEditTime: 2021-05-13 21:55:16
LastEditors: Please set LastEditors
Description: In User Settings Edit
'''
import marketer as mk
import dataloader as dl
import numpy as np
import time
import helper

# ml = dl.MarketLoader(save_csv=True, save_dir='k_history')
# dict_code_as_key, dict_date_as_key = ml.load_k_history(beg='20201201', end='20500101')

# # load load_k_realtime数据
# ml = dl.MarketLoader(save_csv=True, save_dir='k_realtime_513')
# dict_code_as_key, dict_date_as_key = ml.load_k_realtime()
# load load_bill_realtime数据
ml = dl.MarketLoader(save_csv=True, save_dir='bill_realtime_513')
dict_code_as_key, dict_date_as_key = ml.load_bill_realtime()

# # 合并k_dict_code_as_key与bill_dict_code_as_key
# k = np.load('k_dict_code_as_key.npy',allow_pickle=True).item()
# bill = np.load('bill_dict_code_as_key.npy',allow_pickle=True).item()
# helper.combile_k_bill_code_as_key(k, bill)

# # 合并k_dict_date_as_key与bill_dict_date_as_key
# k = np.load('k_dict_date_as_key.npy',allow_pickle=True).item()
# bill = np.load('bill_dict_date_as_key.npy',allow_pickle=True).item()
# helper.combile_k_bill_date_as_key(k, bill)

# mk.bill_history(save_csv=True, save_dir='bill_history')
# mk.k_history_realtime(stock_codes=['SH002460'])
# mk.bill_history_realtime()

# a = np.load('data_dict_code_as_key.npy', allow_pickle=True).item()
# print(a['SH603297'][1][-1])



