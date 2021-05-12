'''
Author: peihan
Date: 2021-04-26 12:34:54
LastEditTime: 2021-05-12 10:29:05
LastEditors: Please set LastEditors
Description: 获取市场信息的内部接口类
'''
import pandas as pd
from urllib.parse import urlencode
import requests
from . import utils
import socket
import random
import time
 
socket.setdefaulttimeout(60)  # 设置socket层的超时时间为60秒

# 同花顺网站Headers
EastmoneyHeaders = {
        'Host': '19.push2.eastmoney.com',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }


def get_headers():
    '''
    随机获取一个headers
    '''
    user_agents =  ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
                    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
                    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11','Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
                    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1']
    headers = {'User-Agent':random.choice(user_agents)}
    return headers

def fetch_data(data_type, params, base_url, code, secid, columns):
    '''
    @description: 通用获取股票信息的方法
    @param {data_type: 东方财富自定义的key，包括klines，trends等
            code: 8位股票代码
            secid: 东方财富专用的secid
            columns: 各指标的名称}
    @return {DataFrame}
    '''
    EastmoneyHeaders.update(get_headers())
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

def fetch_data_2(data_type, params, base_url, code, secid, columns):
    '''
    @description: 针对bill_history_realtime_2获取股票信息的方法
    @param {data_type: 东方财富自定义的key，包括klines，trends等
            code: 8位股票代码
            secid: 东方财富专用的secid
            columns: 各指标的名称}
    @return {DataFrame}
    '''
    EastmoneyHeaders.update(get_headers())
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
        return []
    data_dict = data[data_type][0]

    main_force_value = data_dict['f62']
    small_order_value = data_dict['f84']
    mid_order_value = data_dict['f78']
    large_order_value = data_dict['f72']
    super_large_order_value = data_dict['f66']
    main_force_perc = data_dict['f184']
    small_order_perc = data_dict['f87']
    mid_order_perc = data_dict['f81']
    large_order_perc = data_dict['f75']
    super_large_order_perc = data_dict['f69']

    return_list = [main_force_value, main_force_perc, super_large_order_value, super_large_order_perc, large_order_value, large_order_perc,
                    mid_order_value, mid_order_perc, small_order_value, small_order_perc]
    
    response.close() # 关闭连接

    return return_list

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



def get_history_bill_realtime_2(code):
    '''
    @description: 获取实时日内主力数据
    @param {*}
    @return {*}
    '''
    EastmoneyBills = {
        'f62': '主力净流入',
        'f184': '主力净比',
        'f66': '超大单净流入',
        'f69': '超大单净比',
        'f72': '大单净流入',
        'f75': '大单净比',
        'f78': '中单净流入',
        'f81': '中单净比',
        'f84': '小单净流入',
        'f87': '小单净比',
        'f64': '超大单流入',
        'f65': '超大单流出',
        'f70': '大单流入',
        'f71': '大单流出',
        'f76': '中单流入',
        'f77': '中单流出',
        'f82': '小单流入',
        'f83': '小单流出',
        'f164': '未知',
        'f166': '未知',
        'f168': '未知',
        'f170': '未知',
        'f172': '未知',
        'f252': '未知',
        'f253': '未知',
        'f254': '未知',
        'f255': '未知',
        'f256': '未知',
        'f124': '未知',
        'f6': '金额',
        'f278': '未知',
        'f279': '未知',
        'f280': '未知',
        'f281': '未知',
        'f282': '未知',
    }
    fields = list(EastmoneyBills.keys())
    columns = list(EastmoneyBills.values())
    fields = ",".join(fields)
    secid = utils.gen_secid(code)
    params = (
        ('fltt', '2'),
        ('secids', secid),
        ('fields', fields),
    )
    params = dict(params)
    base_url = 'http://push2.eastmoney.com/api/qt/ulist.np/get'
    
    return fetch_data_2('diff', params, base_url, code, secid, columns)





