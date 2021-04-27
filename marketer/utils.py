'''
Author: your name
Date: 2021-04-26 12:35:42
LastEditTime: 2021-04-27 14:55:51
LastEditors: Please set LastEditors
Description: 通用方法类
'''
import xlrd
import os
import sys

file = './marketer/TongHuaShun.xlsx'

def read_excel():
    '''
    @description: 从同花顺下载的股票信息中提取股票代码
    @param {*}
    @return {市场上所有股票的代码}
    '''
    wb = xlrd.open_workbook(filename=file)
    sheet1 = wb.sheet_by_index(0)
    rows = sheet1.row_values(0)
    cols = sheet1.col_values(0)
    # print(rows)
    # print(cols)
    all_codes = cols[1:] # ['SH688639', 'SZ300153', 'SZ300061'...]
    return all_codes

def gen_secid(rawcode):
    '''
    @description: 生成东方财富专用的secid
    @param {rawcode: 8位股票代码}
    @return {指定格式的字符串}
    '''
    # # 沪市指数
    # if rawcode[:3] == '000':
    #     return f'1.{rawcode}'
    # # 深证指数
    # if rawcode[:3] == '399':
    #     return f'0.{rawcode}'
    # # 深市股票
    # if rawcode[0] != '6':
    #     return f'0.{rawcode}'
    # # 沪市股票
    # return f'1.{rawcode}'
    if rawcode[:2] == 'SZ':
        return f'0.{rawcode[2:]}'
    elif rawcode[:2] == 'SH':
        return f'1.{rawcode[2:]}'
    else:
        return None

def fix_secid(secid, code):
    '''
    @description: 处理东方财富生成secid部分不匹配问题
    @param {*}
    @return {*}
    '''
    if secid[0] == '0':
        return f'1.{code[2:]}'
    else:
        return f'0.{code[2:]}'

