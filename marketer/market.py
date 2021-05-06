'''
Author: peihan
Date: 2021-04-26 12:34:54
LastEditTime: 2021-05-06 17:25:07
LastEditors: Please set LastEditors
Description: 获取市场信息的内部接口类
'''
import pandas as pd
from urllib.parse import urlencode
import requests
from . import utils
import socket
 
socket.setdefaulttimeout(60)  # 设置socket层的超时时间为60秒

# 同花顺网站Headers
EastmoneyHeaders = {
        'Host': '19.push2.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }

def fetch_data(data_type, params, base_url, code, secid, columns):
    '''
    @description: 通用获取股票信息的方法
    @param {data_type: 东方财富自定义的key，包括klines，trends等
            code: 8位股票代码
            secid: 东方财富专用的secid
            columns: 各指标的名称}
    @return {DataFrame}
    '''
    url = base_url+'?'+urlencode(params)
    response = requests.get(url, headers=EastmoneyHeaders)
    json_response = response.json()
    data = json_response['data']
    if data is None:
        secid = utils.fix_secid(secid, code)
        params['secid'] = secid
        url = base_url+'?'+urlencode(params)
        response = requests.get(url, headers=EastmoneyHeaders)
        json_response = response.json()
        data = json_response.get('data')
    if data is None:
        print('股票代码:', code, '可能有误')
        return pd.DataFrame(columns=columns), [], columns
    lines = data[data_type]
    rows = []
    for _line in lines:
        line = _line.split(',')
        rows.append(line)

    df = pd.DataFrame(rows, columns=columns)

    response.close() # 关闭连接

    return df, rows, columns

def get_k_history(code: str, beg: int, end: int, klt=101, fqt=1):
    '''
    @description: 获取k线数据，得到日间涨跌信息
    @param {code: 8位股票代码
            beg: 开始日期 例如 20200101
            end: str 结束日期 例如 '20200201'
            klt: int k线间距 默认为 101 即日k
                klt:1 1 分钟
                klt:5 5 分钟
                klt:101 日
                klt:102 周
            fqt: int 复权方式
                不复权 : 0
                前复权 : 1
                后复权 : 2 }
    @return {DateFrame}
    '''
    EastmoneyKlines = {
        'f51': '日期',
        'f52': '开盘',
        'f53': '收盘',
        'f54': '最高',
        'f55': '最低',
        'f56': '成交量',
        'f57': '成交额',
        'f58': '振幅',
        'f59': '涨跌幅',
        'f60': '涨跌额',
        'f61': '换手率',
    }
    fields = list(EastmoneyKlines.keys())
    columns = list(EastmoneyKlines.values())
    fields2 = ",".join(fields)
    secid = utils.gen_secid(code)
    params = (
        ('fields1', 'f1,f2,f3,f4,f5,f6'),
        ('fields2', fields2),
        ('beg', beg),
        ('end', end),
        ('rtntype', '6'),
        ('secid', secid),
        ('klt', f'{klt}'),
        ('fqt', f'{fqt}'),
    )
    params = dict(params)
    base_url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'

    return fetch_data('klines', params, base_url, code, secid, columns)

def get_k_realtime(code):
    '''
    @description: 获取k线数据，得到实时日内涨跌信息
    @param {code: 8位股票代码}
    @return {DateFrame}
    '''
    EastmoneyKlines = {
        'f51': '日期',
        'f52': '未知',
        'f53': '价格',
        'f54': '未知',
        'f55': '未知',
        'f56': '成交量',
        'f57': '成交额',
        'f58': '均价',
    }

    fields = list(EastmoneyKlines.keys())
    columns = list(EastmoneyKlines.values())
    fields2 = ",".join(fields)
    secid = utils.gen_secid(code)
    params = (
        ('fields1', 'f1,f2,f3,f4,f5,f6'),
        ('fields2', fields2),
        ('rtntype', '6'),
        ('secid', secid),
        ('ndays', '1'),
        ('iscr', '0'),
        ('iscca', '0')
    )
    params = dict(params)
    base_url = 'https://push2.eastmoney.com/api/qt/stock/trends2/get'

    return fetch_data('trends', params, base_url, code, secid, columns)

def get_history_bill(code):
    '''
    @description: 获取日间主力数据，只能获取近半年
    @param {*}
    @return {DataFrame}
    '''
    EastmoneyBills = {
        'f51': '日期',
        'f52': '主力净流入',
        'f53': '小单净流入',
        'f54': '中单净流入',
        'f55': '大单净流入',
        'f56': '超大单净流入',
        'f57': '主力净流入占比',
        'f58': '小单流入净占比',
        'f59': '中单流入净占比',
        'f60': '大单流入净占比',
        'f61': '超大单流入净占比',
        'f62': '收盘价',
        'f63': '涨跌幅'
    }
    fields = list(EastmoneyBills.keys())
    columns = list(EastmoneyBills.values())
    fields2 = ",".join(fields)
    secid = utils.gen_secid(code)
    params = (
        ('lmt', '100000'),
        ('klt', '101'),
        ('secid', secid),
        ('fields1', 'f1,f2,f3,f7'),
        ('fields2', fields2)
    )
    params = dict(params)
    base_url = 'http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get'
   
    return fetch_data('klines', params, base_url, code, secid, columns)


def get_history_bill_realtime(code):
    '''
    @description: 获取实时日内主力数据
    @param {*}
    @return {*}
    '''
    EastmoneyBills = {
        'f51': '日期',
        'f52': '主力净流入',
        'f53': '小单净流入',
        'f54': '中单净流入',
        'f55': '大单净流入',
        'f56': '超大单净流入'
    }
    fields = list(EastmoneyBills.keys())
    columns = list(EastmoneyBills.values())
    fields2 = ",".join(fields)
    secid = utils.gen_secid(code)
    params = (
        ('lmt', '100000'),
        ('klt', '1'),
        ('secid', secid),
        ('fields1', 'f1,f2,f3,f7'),
        ('fields2', fields2),
    )
    params = dict(params)
    base_url = 'http://push2.eastmoney.com/api/qt/stock/fflow/kline/get'
    
    return fetch_data('klines', params, base_url, code, secid, columns)






