'''
Author: your name
Date: 2021-05-12 12:56:14
LastEditTime: 2021-05-12 13:20:11
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\beyond_alpha\jianting.py
'''
from time import sleep
import numpy as np
import time


for i in range(1000):
    opportunity_list = np.load('opportunity_list.npy',allow_pickle=True)
    print(opportunity_list)
   
    for j in range(len(opportunity_list)):
        code = opportunity_list[j][0]
        main_force_value = opportunity_list[j][1]
        main_force_perc = opportunity_list[j][2]
        small_order_value = opportunity_list[j][3]
        small_order_perc = opportunity_list[j][4]
        print('code:', code)
        print('main_force_value:{}, main_force_perc:{}, small_order_value:{}, small_order_perc:{}'.format(main_force_value,
                                        main_force_perc,small_order_value,small_order_perc))
        print('-------------------------------')
    print('等待......')
    time.sleep(30)
        
