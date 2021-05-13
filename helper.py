'''
Author: your name
Date: 2021-05-12 11:30:01
LastEditTime: 2021-05-13 22:50:22
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\beyond_alpha\helper.py
'''
import numpy as np

def combile_k_bill_code_as_key(k, bill):
    '''
    @description: 合并code作为key的k与bill指标数据
    @param {k: k_dict_code_as_key, 
            bill: bill_dict_code_as_key}
    @return {data_dict_code_as_key}
    '''
    data_dict_code_as_key = {}
    for code, value in k.items():
        rows = []
        date_len = 0
        bill_data_after_index = []
        k_data_after_index = []
        date_after_index = []
        # bill与k线的开始日期不一致
        # 此种方式有一个前提是bill的截止日期与k线截止日期一致
        if bill[code][0][-1] != value[0][-1]:
            raise Exception('bill与k线截止日期不同!')
            
        # 若bill的开始日期早于k线，则找k线的开始日期在bill中的index
        if len(bill[code][0]) > len(value[0]):
            index = bill[code][0].index(value[0][0])
            if bill[code][0][index:] != value[0]:
                raise Exception('bill index错误!')
            bill_data_after_index= bill[code][1][index:]
            k_data_after_index = value[1]
            date_after_index = value[0]
            date_len = len(value[0])
        # 若k线的开始日期早于bill，则找bill的开始日期在k线中的index
        elif len(bill[code][0]) <= len(value[0]):
            index = value[0].index(bill[code][0][0])
            if value[0][index:] != bill[code][0]:
                raise Exception('k线 index错误!')
            k_data_after_index= value[1][index:]
            bill_data_after_index = bill[code][1]
            date_after_index = bill[code][0]
            date_len = len(bill[code][0])
            
        for i in range(date_len):
            k_data = k_data_after_index[i]
            bill_data = bill_data_after_index[i]
            row = np.concatenate((k_data, bill_data), axis=0)
            rows.append(row)

        data_dict_code_as_key[code] = [date_after_index, np.array(rows)]
    np.save('data_dict_code_as_key.npy', data_dict_code_as_key)


def combile_k_bill_date_as_key(k, bill):
    '''
    @description: 合并date作为key的k与bill指标数据
    @param {k: k_dict_date_as_key, 
            bill: bill_dict_date_as_key}
    @return {data_dict_date_as_key}
    '''
    data_dict_date_as_key = {}
    for date, value in k.items():
        rows = []
        codes_list = []
        code_len = 0
        
        # 遍历某一天k线数据中所有股票代码，若股票代码在同一天bill数据中出现，则合并
        for i in range(len(value[0])):
            code = value[0][i]
            if code in bill[date][0]:
                k_data = value[1][i]
                
                # 获取股票代码在bill数据中心的index
                index = bill[date][0].index(code)
                bill_data = bill[date][1][index]

                row = np.concatenate((k_data, bill_data), axis=0)
                rows.append(row)
                codes_list.append(code)

        data_dict_date_as_key[date] = [codes_list, rows]
    np.save('data_dict_date_as_key.npy', data_dict_date_as_key)

def calculate_nMA(input_data, n):
    '''
    @description: 计算n日均线
    @param {input_data: data_dict_code_as_key.npy的地址
            n: 需计算的n日均线}
    @return {MA_dict: 保持data_dict_code_as_key的格式，key为code，value为二维list
                    第一维为日期的list，第二维为n日均线的list}
    '''
    his_data = np.load(input_data,allow_pickle=True).item() 
    MA = n
    MA_dict = {}

    for code, value in his_data.items():
        MA_list = []
        close_price_list = value[1][:,1]
        for i in range(len(value[0])):
            if i+1 < MA:
                MA_list.append(-1)
            else:
                MA_value = round(sum(close_price_list[i+1-MA:i+1])/MA, 2)
                MA_list.append(MA_value)
        if len(value[0]) != len(MA_list):
            raise Exception('有问题!!!')
        MA_dict[code] = [value[0], MA_list]
    np.save('MA{}.npy'.format(MA), MA_dict)