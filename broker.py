#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Ji Li

import os
import sys
import time
import order

class Broker:
    '''
    股票经理人
    '''
    stamp_duty = 0.001                                              # 印花税率，0.1%
    transfer_fee = 0.00002                                          # 过户费，沪市0.002%，深市目前不收取（根据2020年实操交易结果显示，手续费无需满足每笔最少1元的要求） 
    precise_digits = 5                                              # money精确到小数点后五位，对股价暂不作限制，显示结果时用
    price_limit = 0.1                                               # A股默认10%，科创板头5个交易日不设涨跌限制，后面40%，后续完善
    stock_symbol_rules = {                                          # 股票代码板块规则
        '沪A': 'SH60', 
        '沪B': 'SH900', 
        '科创板': 'SH688', 
        '深A': 'SZ000', 
        '深B': 'SZ200', 
        '中小板': 'SZ002', 
        '创业板': 'SZ300', 
    }
    ''' 待完善
    stock_market_index = {                                          # 各种股指及其成分股
        ('SH000001', '沪指'): [],
        ('SH000688', '科创50'): [], 
        ('SH000003', '沪B指数'): [], 
        ('SZ399001', '深指'): [], 
        ('SZ399006', '创业板指'): [], 
        ('SZ399005', '中小板指'): [], 
        ('SZ399003', '深B指数'): [],
    }
    '''

    def __init__(self, startMoney=1000000, commission=0.0002):
        self.__total_invset = startMoney                            # 总投入，该值不允许修改
        self.remain_money = self.__total_invset                     # 剩余现金，默认开局全是现金
        self.total_market = 0                                       # 总市值，所有股票的价值和
        self.total_assets = self.__total_invset                     # 总资产 = 总市值 + 剩余现金，开局默认为总投入
        self.total_profitloss = 0                                   # 总盈亏 = 总资产 - 总投入，开局默认0，正数表示盈，负数表示亏
        self.stocks_assets = {}                                     # 'SZ000002': [昨日持仓股数, 今日买入股数, 实时成本价，T日收盘价]
        self.his_orders = []                                        # list, Order类的队列，只进不出，存放所有的单
        self.pending_orders = []                                    # 存放待处理的单
        self.fee = 0                                                # 统计缴纳了多少税费
        self.stock_transaction_fee = {                              # 股票交易费率
            'bSH': lambda x: max(5, x*commission)+x*Broker.transfer_fee,                        # 买入沪市收取费用，券商佣金 + 股市过户费
            'bSZ': lambda x: max(5, x*commission),                                              # 买入深市收取费用，券商佣金
            'sSH': lambda x: max(5, x*commission)+x*Broker.transfer_fee+x*Broker.stamp_duty,    # 卖出沪市收取费用，券商佣金 + 股市过户费 + 印花税
            'sSZ': lambda x: max(5, x*commission)+x*Broker.stamp_duty,                          # 卖出深市收取费用，券商佣金 + 印花税
        }

    # 得到正在等待的订单
    def get_pending_orders(self):
        for order in self.pending_orders:
            print(order.err())

    # 判断股票能否被交易
    def can_be_traded(self, stock_code: str) -> bool:
        if stock_code[:4] == 'SH60':
            return True
        if stock_code[:5] in ('SH900', 'SH688', 'SZ000', 'SZ200', 'SZ002', 'SZ300'):
            return True
        return False

    # 判断价格是否被允许（即判断是否超出涨跌停）
    def check_price(self, closing_tm1, order_price) -> bool:
        '''
        价格判断

        Parameters
        ----------
        closing_tm1：t-1日收盘价
        order_price：t日订单价

        Return
        ------
        价格是否允许
        '''
        return True if round(closing_tm1*0.9, 2) <= order_price <= round(closing_tm1*1.1, 2) else False # 后面需要检查这个等于

    # 分日分分操作逻辑（订单撮合）
    def match_order_by_day_or_minute(self, stock: list, closing_tm1, order) -> bool:
        '''
        撮合订单

        Parameters
        ----------
        stock：T日数据
        order：Order类型的变量

        Return
        ------
        该单是否成功
        '''
        if self.can_be_traded(order.code) == False:                     # 判断股票能否交易
            return False
        self.his_orders.append(order)                                   # 保存合法订单信息
        open_price, closing_price, high_price, low_price = stock[:4]    # 获取T日或T时价格信息
        trade_price, trade_shares = order.price, order.shares           # 从订单中获取交易信息

        if high_price == low_price and (high_price == round(closing_tm1*0.9, 2) or low_price == round(closing_tm1*1.1, 2)): # 一字涨停和一字跌停无法买入卖出
            self.pending_orders.append(order)                           # 对T时交易
            return False
        trade_money = trade_price * trade_shares                        # 交易金额
        
        if low_price <= trade_price <= high_price:                      # 判断价格是否可以成交
            # 计算交易费率
            fee = self.stock_transaction_fee[order.type + order.code[:2]](trade_money)
            # 获取持仓信息
            try:
                tm1_shares, t_shares, had_price, _ = self.stocks_assets[order.code] # 按照self.stocks_assets的上述约定
            except KeyError:
                if order.type == 's':                                               # 处理首次卖出的错误逻辑
                    return False
                self.stocks_assets[order.code] = [0, 0, 0, 0]
                tm1_shares, t_shares, had_price = 0, 0, 0
            # 判断并执行交易
            if order.type == 'b' and fee + trade_money <= self.remain_money:
                self.remain_money -= fee + trade_money
                self.stocks_assets[order.code][1] += trade_shares
                self.stocks_assets[order.code][2] = (fee + trade_money + (tm1_shares + t_shares) * had_price) / (tm1_shares + t_shares + trade_shares)
            elif order.type == 's' and trade_shares <= tm1_shares:
                self.remain_money += trade_money - fee
                self.stocks_assets[order.code][0] = tm1_shares - trade_shares
            else:
                return False
            order.deal_date = time.strftime("%Y%m%d%H%M%S", time.localtime())       # 成交日期时间：年月日时分秒
            order.done = True
            self.fee += fee
        else:
            self.pending_orders.append(order)                           # 对分时交易而言
            return False

    # 秒级操作逻辑
    def match_order_by_second(self, stock: list, order) -> bool:
        '''
        未完待续
        '''
        pass

    # 处理一串串订单
    def run(self, tm1: dict, t1: dict, stocks: dict, orders: list, show=False):
        '''
        处理多支股票的交易
        
        Parameters
        ----------
        stocks：'t1'表示T日数据，'tm1'表示T-1日数据，对于分均数据，以tm1表示前一分钟，t1表示当前这一分钟
                即要获取一个股票T日的数据应stocks['t1'][t1['SZ000002']]
                T日上市的股票的t1日开、收、高、低四个价位均为发行价
        tm1：stocks中tm1内股票的code和其在array中的对应关系
        t1：stocks中t1内股票的code和其在array中的对应关系
        orders：Order类的数组

        Return
        ------
        无返回值
        '''
        # 将上一日的pending_orders清空
        if self.pending_orders != []:
            pending_date = self.pending_orders[0].create_date
            running_date = orders[0].create_date
            if pending_date != running_date:
                self.pending_orders = []
        # 处理所有订单（分时交易未成交的单暂时如此处理，最好是可以回调）
        for order in orders + self.pending_orders:
            closing_tm1 = stocks['tm1'][tm1[order.code]][1]                              # 收盘价默认放到索引为1的位置
            if order.price == -1:                                                           # 如果order中订单价为-1则以开盘价买入
                order.price = stocks['t1'][t1[order.code]][0]
            if self.check_price(closing_tm1, order.price) == False:                         # 判断订单价格是否超出涨跌停，超出则打印
                order.err("超过涨跌幅限制")
                continue
            self.match_order_by_day_or_minute(list(stocks['t1'][t1[order.code]]), closing_tm1, order)   # 根据T日或T时数据撮合交易
            # 测试，正式需删除
            #order.err("测试")
        self.total_market = 0
        # 更新交易数据
        for stock_code in self.stocks_assets:
            tm1_shares, t_shares, had_price, _ = self.stocks_assets[stock_code]
            tm1_shares += t_shares
            closing_price = stocks['t1'][t1[stock_code]][1]
            self.stocks_assets[stock_code] = [tm1_shares, 0, had_price, closing_price]
            self.total_market += closing_price * tm1_shares
        self.total_assets = self.total_market + self.remain_money
        self.total_profitloss = self.total_assets - self.__total_invset
        # 展示收益
        if show:
            self.show()
        self.pending_orders = []

    # 可视化收益情况
    def show(self):
        print(f"总资产: {self.total_assets:.2f}")
        print(f"总市值: {self.total_market:.2f}")
        print(f"可用现金: {self.remain_money:.2f}")
        print(f"总盈亏: {self.total_profitloss:.2f}")
        print(f"总手续费: {self.fee:.5f}")
        print(f"个股代码\t股价\t成本价\t持仓\t盈亏")
        for code, v in self.stocks_assets.items():
            print(f"{code}\t{v[3]:.2f}\t{v[2]:.3f}\t{v[0]}\t{(v[3] - v[2])/v[2] * 100:.2f}%")
        #sys.stdout.flush()
