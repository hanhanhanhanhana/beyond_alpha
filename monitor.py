'''
Author: your name
Date: 2021-05-12 12:56:14
LastEditTime: 2021-05-12 13:51:06
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\beyond_alpha\jianting.py
'''
from time import sleep
import numpy as np
import time

last_len = 0
for i in range(1000):
    opportunity_list = np.load('opportunity_list.npy',allow_pickle=True)
    if opportunity_list == []:
        print('还未检测到数据，稍等！')
        continue
    now_len = len(opportunity_list)
    for j in range(len(opportunity_list)):
        code = opportunity_list[j][0]
        main_force_value = opportunity_list[j][1]
        main_force_perc = opportunity_list[j][2]
        small_order_value = opportunity_list[j][3]
        small_order_perc = opportunity_list[j][4]
        # print('code:', code)
        # print('main_force_value:{}, main_force_perc:{}, small_order_value:{}, small_order_perc:{}'.format(main_force_value,
        #                                 main_force_perc,small_order_value,small_order_perc))
        # print('-------------------------------')
    if now_len > last_len:
        print('!!!!!!!!!!!!!!!!! 注意注意，有新的股票满足条件 !!!!!!!!!!!!!!!!!')
        print(opportunity_list[last_len:])
    last_len = now_len
    print('上一次检测有{}只股票满足条件！！！'.format(len(opportunity_list)))
    print('等待......')
    time.sleep(5)
        
