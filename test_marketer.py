'''
Author: peihan
Date: 2021-04-25 16:40:05
LastEditTime: 2021-04-26 17:56:04
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\beyond_alpha\test1.py
'''
# import easyquotation

# quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq'] 

# # 获取所有股票行情
# all = quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
# # print(all['sh600295'])

# # 单只股票
# one = quotation.real('sh600295') # 支持直接指定前缀，如 'sh000001'

# # 多只股票
# some = quotation.stocks(['000001', '162411']) 
# # print(some)

# # 
# quotation = easyquotation.use("timekline")
# data = quotation.real(['603828'], prefix=True)
# print(data)

# # # 
# # quotation  = easyquotation.use("daykline")
# # data = quotation.real(['00001'])
# # print(data.keys())

import marketer as mk

mk.bill_history_realtime()


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
