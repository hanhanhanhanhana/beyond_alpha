# coding:utf-8
# backtrader的第一个策略
import datetime
import sys
import pandas as pd
import backtrader as bt
import tushare as ts

# 创建一个策略
class TestStrategy(bt.Strategy):
    def log(self, txt, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))
 
    def __init__(self):
        # The first data in the list self.datas[0] is the default data for trading operations and to keep all strategy elements synchronized (it’s the system clock)
        self.dataclose = self.datas[0].close
 
    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])
        # 今天收盘价比昨天低
        if self.dataclose[0] < self.dataclose[-1]:
            # 昨天收盘价比前天低
            if self.dataclose[-1] < self.dataclose[-2]:
                # 买买买
                self.log("在%.2f创建买单" % self.dataclose[0])
                self.buy()

if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    # 加载数据
    start = "2019-01-01"
    end = "2019-2-01"
    # DataFrame格式数据，列名分别为 date   open  close   high    low     volume    code
    df = ts.get_k_data("510300", autype = "qfq", start = start,  end = end)

    # 将date设置为index
    df.index = pd.to_datetime(df.date)
    # 列名修改为 open   high    low  close     volume  openinterest
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    
    data = bt.feeds.PandasData(dataname = df, fromdate = datetime.datetime(2019, 1, 1), todate = datetime.datetime(2019, 2, 1))
    cerebro.adddata(data)

    # 设置初始资金
    cerebro.broker.setcash(100000.0)
    print("初始资金:%.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("期末资金:%.2f" % cerebro.broker.getvalue())