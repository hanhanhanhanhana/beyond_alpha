import easyquotation

quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq'] 

# 获取所有股票行情
all = quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
# print(all['sh600295'])

# 单只股票
one = quotation.real('sh600295') # 支持直接指定前缀，如 'sh000001'

# 多只股票
some = quotation.stocks(['000001', '162411']) 
print(some)