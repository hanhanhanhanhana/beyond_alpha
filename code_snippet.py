'''
Author: your name
Date: 2021-05-12 11:34:39
LastEditTime: 2021-05-12 13:20:28
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\beyond_alpha\code_snippet.py
'''
import numpy as np
import dataloader as dl
import time

# load_bill_realtime_2测试代码，实时监控进行分析判断
all_codes = np.load('all_codes.npy', allow_pickle=True)
# 挑选了3000来只股票，后需要将股票池进一步缩小
selected_codes = [code for code in all_codes if code.startswith('SH60') or code.startswith('SZ000') or code.startswith('SZ002')]
ml = dl.MarketLoader(custom_stocks=selected_codes)
opportunity_list = []
for i in range(1000):
    dict_code_as_key = ml.load_bill_realtime_2()
    for code, value in dict_code_as_key.items():
        if value == []:
            continue
        main_force_value = value[0]
        main_force_perc = value[1]
        super_large_order_value = value[2]
        super_large_order_perc = value[3]
        large_order_value = value[4]
        large_order_perc = value[5]
        mid_order_value = value[6]
        mid_order_perc = value[7]
        small_order_value = value[8]
        small_order_perc = value[9]
        # 策略部分代码，后续需完善
        if main_force_perc > 40 and small_order_perc < -10:
            print('注意机会：', code)
            opportunity_list.append([code, main_force_value, main_force_perc, small_order_value, small_order_perc])
    np.save('opportunity_list.npy', opportunity_list)
    print('每次爬取后暂停一段时间')
    time.sleep(60)


# 简单主力净流入的分析部分代码
# [开盘 收盘 最高 最低 成交量 成交额 振幅 涨跌幅 涨跌额 换手率 主力净流入 小单净流入 中单净流入 大单净流入 超大单净流入 
# 主力净流入占比 小单流入净占比 中单流入净占比 大单流入净占比 超大单流入净占比 收盘价 涨跌幅]

# #获取平均数
# def Get_Average(list):
#    sum = 0
#    for item in list:     
#       sum += item  
#    return sum/len(list)

# code_as_key_data = np.load('data_dict_code_as_key.npy', allow_pickle=True).item()
# flag = False
# all_ = 0
# threshold_zhulizhanbi = 40
# threshold_zhangdiefu = -9
# count_exceed = 0
# count_below = 0
# code_date_list = []
# code_date_list_no = []
# profit = []

# for code, value in code_as_key_data.items():
#     # 去除新股
#     if len(value[0]) > 30:
#         for i in range(len(value[0])):
#             kai_pan = value[1][i][0]
#             shou_pan = value[1][i][1]
#             zui_gao = value[1][i][2]
#             zui_di = value[1][i][3]
            
#             zhu_li_liu_ru = value[1][i][10]
#             zhu_li_zhan_bi = value[1][i][15]
#             chao_da_dan_zhan_bi = value[1][i][19]
#             zhang_die_fu = value[1][i][-1]

#             # 去除股票的第一天开盘
#             if i == 0:
#                 continue

#             if flag == True:
#                 profit.append(zhang_die_fu)
#                 flag=False

#             # 去除一字板
#             if kai_pan == shou_pan == zui_gao == zui_di:
#                 continue
            
#             if zhu_li_zhan_bi > threshold_zhulizhanbi:
#                 if zhang_die_fu > threshold_zhangdiefu:
#                     count_exceed+=1
#                     code_date_list.append(code+'-'+str(value[0][i]))
#                     flag=True
#                 else:
#                     count_below+=1
#                     code_date_list_no.append(code+'-'+str(value[0][i]))
#                 all_+=1

# print(all_)
# print(count_exceed)
# print(count_below)
# print(count_exceed/all_)
# # print(code_date_list)
# # print(code_date_list_no)
# print(count_exceed)
# over_zero = [i for i in profit if i > 0]
# below_zero = [i for i in profit if i < 0]
# zhang_ting = [i for i in profit if i > 9]
# die_ting = [i for i in profit if i < -9]

# print('涨停率：', len(zhang_ting)/len(profit))
# print('跌停率：', len(die_ting)/len(profit))
# print('上涨率：', len(over_zero)/len(profit))
# print('下跌率：', len(below_zero)/len(profit))
# print('均收益：', Get_Average(profit))



# date_as_key_data = np.load('data_dict_date_as_key.npy', allow_pickle=True).item()
# threshold_zhulizhanbi = 40

# # TODO:如何判断新股
# for date, value in date_as_key_data.items():
#     print(date)
#     for i in range(len(value[0])):
#         print(value[0][i])
#         print(value[1][i])
#         kai_pan = value[1][i][0]
#         shou_pan = value[1][i][1]
#         zui_gao = value[1][i][2]
#         zui_di = value[1][i][3]
        
#         zhu_li_liu_ru = value[1][i][10]
#         zhu_li_zhan_bi = value[1][i][15]
#         chao_da_dan_zhan_bi = value[1][i][19]
#         zhang_die_fu = value[1][i][-1]

#         print(zhu_li_zhan_bi)
#         print(zhang_die_fu)
#         exit()


