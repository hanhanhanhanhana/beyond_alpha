'''
Author: peihan
Date: 2021-04-25 16:40:05
LastEditTime: 2021-05-06 21:12:31
LastEditors: Please set LastEditors
Description: In User Settings Edit
'''

import dataloader as dl
import numpy as np


ml = dl.MarketLoader(beg='20210101', end='20210506', period='day', save_csv=True, save_dir='k_history')
dict_code_as_key, dict_date_as_key = ml.load_k_history()


# mk.bill_history()
# mk.k_history_realtime(stock_codes=['SH002460'])
# mk.bill_history_realtime()

