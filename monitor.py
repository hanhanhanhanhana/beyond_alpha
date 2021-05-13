'''
Author: your name
Date: 2021-05-12 12:56:14
LastEditTime: 2021-05-13 13:34:21
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\beyond_alpha\jianting.py
'''
from time import sleep
import numpy as np
import time
import os

print_first = True
global_codes_pool = []

for i in range(1000):
    if os.path.exists('opportunity_list.npy'):
        opportunity_list = np.load('opportunity_list.npy',allow_pickle=True)
        if len(opportunity_list) == 0:
            print('还未检测到数据，稍等！')
            continue
        if len(opportunity_list) != 0 and len(global_codes_pool) == 0:
            global_codes_pool = opportunity_list[-1]
        if global_codes_pool != opportunity_list[-1]:
            new_added = [i for i in opportunity_list[-1] if i not in global_codes_pool]
            new_reduced = [i for i in global_codes_pool if i not in opportunity_list[-1]]
            if new_added != []:
                print('!'*100)
                print(' '*30 +'注意注意，有新满足条件的股票进入的股票池'+' '*50)
                print(new_added)
                print('!'*100)
                
            if new_reduced != []:
                print('*'*100)
                print(' '*30 + '注意注意，有股票退出满足条件的股票池'+' '*50)
                print(new_reduced)
                print('*'*100)
            
            global_codes_pool = opportunity_list[-1]

        print(' '*25 +'上一次检测有{}只股票满足条件，等待下一次监测'.format(len(opportunity_list[-1]))+' '*50)
    time.sleep(10)
        
