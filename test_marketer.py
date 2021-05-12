'''
Author: peihan
Date: 2021-04-25 16:40:05
LastEditTime: 2021-05-12 13:44:58
LastEditors: Please set LastEditors
Description: In User Settings Edit
'''
import marketer as mk
import dataloader as dl
import numpy as np
import time

ml = dl.MarketLoader(beg='20210101', end='20210506', period='day', save_csv=True, save_dir='k_history')
dict_code_as_key, dict_date_as_key = ml.load_k_history()

# mk.bill_history(save_csv=True, save_dir='bill_history')
# mk.k_history_realtime(stock_codes=['SH002460'])
# mk.bill_history_realtime()

# a = np.load('bill_dict_date_as_key.npy', allow_pickle=True).item()
# print(a[20201210][1][-1])



