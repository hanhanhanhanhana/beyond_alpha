from urllib.parse import urlencode
import pandas as pd
import numpy as np
import requests
import time
import xlrd
import os

# requests失效后重连
requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
s = requests.session()
s.keep_alive = False # 关闭多余连接

# 为了得到市场上上市股票的代码
file = 'TongHuaShun.xlsx'
def read_excel():
	wb = xlrd.open_workbook(filename=file)#打开文件
	print(wb.sheet_names())#获取所有表格名字
	sheet1 = wb.sheet_by_index(0)#通过索引获取表格
	# rows = sheet1.row_values(0)#获取行内容
	cols = sheet1.col_values(0)#获取列内容
	# print(rows)
	return cols[1:]
all_codes = read_excel()
all_codes = [code[2:] for code in all_codes]

# flag设置为执行的模式
# 1为get_k_history，2为get_k_realtime，3为get_history_bill，4为get_history_bill_realtime
flag = 1

# 股票池
# stock_codes = ['300750']
stock_codes = all_codes

# TODO:此方法存在问题，有查看到将某些深市股票扔以0.开头，反之亦然，从而导致爬取不到该股票信息
def gen_secid(rawcode: str) -> str:
    '''
    生成东方财富专用的secid

    Parameters
    ----------
    rawcode : 6 位股票代码

    Return
    ------
    str: 指定格式的字符串

    '''
    # 沪市指数
    if rawcode[:3] == '000':
        return f'1.{rawcode}'
    # 深证指数
    if rawcode[:3] == '399':
        return f'0.{rawcode}'
    # 沪市股票
    if rawcode[0] != '6':
        return f'0.{rawcode}'
    # 深市股票
    return f'1.{rawcode}'
 
def get_k_history(code: str, beg: str = '20200101', end: str = '20200201', klt: int = 101, fqt: int = 1) -> pd.DataFrame:
    '''
    功能获取k线数据，得到日间涨跌信息

    Parameters
    ----------
    code : 6 位股票代码
    beg: 开始日期 例如 20200101
    end: 结束日期 例如 20200201
    klt: k线间距 默认为 101 即日k
        klt:1 1 分钟
        klt:5 5 分钟
        klt:101 日
        klt:102 周
    fqt: 复权方式
        不复权 : 0
        前复权 : 1
        后复权 : 2 
    Return
    ------
    DateFrame : 包含股票k线数据
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
    EastmoneyHeaders = {
        'Host': '19.push2.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
    fields = list(EastmoneyKlines.keys())
    columns = list(EastmoneyKlines.values())
    fields2 = ",".join(fields)
    secid = gen_secid(code)
    params = (
        ('fields1', 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13'),
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
    url = base_url+'?'+urlencode(params)
    # print(url)
    json_response: dict = s.get(
        url, headers=EastmoneyHeaders).json()

    data = json_response.get('data')
    if data is None:
        if secid[0] == '0':
            secid = f'1.{code}'
        else:
            secid = f'0.{code}'
        params['secid'] = secid
        url = base_url+'?'+urlencode(params)
        json_response: dict = s.get(
            url, headers=EastmoneyHeaders).json()
        data = json_response.get('data')
    if data is None:
        print('股票代码:', code, '可能有误')
        return pd.DataFrame(columns=columns)

    klines = data['klines']
    rows = []
    for _kline in klines:

        kline = _kline.split(',')
        rows.append(kline)
    df = pd.DataFrame(rows, columns=columns)

    return df

def get_k_realtime(code: str) -> pd.DataFrame:
    '''
    功能获取k线数据，得到实时日内涨跌信息

    Parameters
    ----------
    code : 6 位股票代码

    Return
    ------
    DateFrame : 包含股票k线数据
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
    EastmoneyHeaders = {
        'Host': '19.push2.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
    fields = list(EastmoneyKlines.keys())
    columns = list(EastmoneyKlines.values())
    fields2 = ",".join(fields)
    secid = gen_secid(code)
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
    url = base_url+'?'+urlencode(params)
    # print(url)
    json_response: dict = s.get(
        url, headers=EastmoneyHeaders).json()

    data = json_response.get('data')
    if data is None:
        if secid[0] == '0':
            secid = f'1.{code}'
        else:
            secid = f'0.{code}'
        params['secid'] = secid
        url = base_url+'?'+urlencode(params)
        json_response: dict = s.get(
            url, headers=EastmoneyHeaders).json()
        data = json_response.get('data')
    if data is None:
        print('股票代码:', code, '可能有误')
        return pd.DataFrame(columns=columns)

    trends = data['trends']
    rows = []
    for _trend in trends:

        trend = _trend.split(',')
        rows.append(trend)
    df = pd.DataFrame(rows, columns=columns)

    return df

def get_history_bill(stock_code: str) -> pd.DataFrame:
    '''
    获取日间主力数据，只能获取近半年
    -
    Parameters
    ----------
    stock_code: 6 位股票代码

    Return
    ------
    DataFrame : 包含指定股票的历史交易日单子数据（大单、超大单等）

    '''
    EastmoneyHeaders = {
        'Host': '19.push2.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
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
    secid = gen_secid(stock_code)
    params = (
        ('lmt', '100000'),
        ('klt', '101'),
        ('secid', secid),
        ('fields1', 'f1,f2,f3,f7'),
        ('fields2', fields2)
    )

    base_url = 'http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get'
    url = base_url+'?'+urlencode(params)
    print(url)
    json_response: dict = s.get(
        url, headers=EastmoneyHeaders).json()
    if json_response is None:
        return
    data = json_response['data']
    if data != None:
        klines = data['klines']
        rows = []
        for _kline in klines:
            kline = _kline.split(',')
            rows.append(kline)
        df = pd.DataFrame(rows, columns=columns)
        return df
    else:
        return None

def get_history_bill_realtime(stock_code: str) -> pd.DataFrame:
    '''
    获取实时日内主力数据
    -
    Parameters
    ----------
    stock_code: 6 位股票代码

    Return
    ------
    DataFrame : 包含指定股票实时日内单子数据（大单、超大单等）

    '''
    EastmoneyHeaders = {
        'Host': '19.push2.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
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
    secid = gen_secid(stock_code)
    params = (
        ('lmt', '100000'),
        ('klt', '1'),
        ('secid', secid),
        ('fields1', 'f1,f2,f3,f7'),
        ('fields2', fields2),
    )

    json_response = s.get('http://push2.eastmoney.com/api/qt/stock/fflow/kline/get',
                                 headers=EastmoneyHeaders, params=params).json()
    if json_response is None:
        return
    data = json_response['data']
    klines = data['klines']
    rows = []
    for _kline in klines:
        kline = _kline.split(',')
        rows.append(kline)
    df = pd.DataFrame(rows, columns=columns)

    return df


if __name__ == "__main__":

    # if flag == 1:
    #     for stock_code in stock_codes:
    #         df = get_k_history(stock_code)
    #         df.to_csv(f'k_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
    #         print(f'股票代码：{stock_code} 的日间k线数据已保存到代码目录下的 k_history_{stock_code}.csv 文件中')
    # elif flag == 3:
    #     for stock_code in stock_codes:
    #         df = get_history_bill(stock_code)
    #         df.to_csv(f'bill_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
    #         print(f'股票代码：{stock_code} 的日间大单净量数据已保存到代码目录下的 bill_history_{stock_code}.csv 文件中')
    # elif flag == 2:
    #     for _ in range(1000):
    #         for stock_code in stock_codes:
    #             df = get_k_realtime(stock_code)
    #             df.to_csv(f'k_realtime_{stock_code}.csv', encoding='utf-8-sig', index=None)
    #             print(f'股票代码：{stock_code} 的日内实时k线数据已保存到代码目录下的 k_realtime_{stock_code}.csv 文件中')
    #             # 240 行说明收盘了，结束
    #             if len(df) >= 240:
    #                 print('已收盘')
    #                 break
    #             time.sleep(60)
    # elif flag == 4:
    #     for _ in range(1000):
    #         for stock_code in stock_codes:
    #             df = get_history_bill_realtime(stock_code)
    #             df.to_csv(f'bill_realtime_{stock_code}.csv', encoding='utf-8-sig', index=None)
    #             print(f'股票代码：{stock_code} 的日内实时大单净量数据已保存到代码目录下的 bill_realtime_{stock_code}.csv 文件中')
    #             # 240 行说明收盘了，结束
    #             if len(df) >= 240:
    #                 print('已收盘')
    #                 break
    #             time.sleep(60)

    
    # # 爬取得股票按照前一天主力净流入比例排序
    # list_sort = []
    # # 未爬取到的股票代码
    # none_list = []
    # for i, stock_code in enumerate(stock_codes):
    #     print(str(i) + "-" + stock_code)
    #     df = get_history_bill(stock_code)
    #     if df is None:
    #         none_list.append(stock_code)
    #     else:
    #         df.to_csv(f'bill_history/bill_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
    #         print(f'股票代码：{stock_code} 的日间大单净量数据已保存到代码目录下的 bill_history/bill_history_{stock_code}.csv 文件中')
    #         main_per = df['主力净流入占比'].iloc[-1]
    #         # print(main_per)
    #         list_sort.append(float(main_per))
    #     time.sleep(1)

    # list_sort_ind = np.argsort(list_sort)[::-1] 

    # np.save('list_sort_ind.npy', list_sort_ind)
    # np.save('list_none.npy', none_list)

    # a = np.load('list_none.npy')
    # b = np.load('list_sort_ind.npy')
    # print(len(a)) # 482
    # print(len(b)) # 3818

    save_dir = 'k_history'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for i, stock_code in enumerate(stock_codes):
        print(str(i) + "-" + stock_code)
        df = get_k_history(stock_code, beg='20150101', end='20200501')
        if df is not None:
            df.to_csv(f'{save_dir}/k_history_{stock_code}.csv', encoding='utf-8-sig', index=None)
            print(f'股票代码：{stock_code} 的日间k线数据已保存到代码目录下的 {save_dir}/k_history_{stock_code}.csv 文件中')
        time.sleep(1)

        
