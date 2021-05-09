'''
Author: your name
Date: 2021-04-28 20:58:38
LastEditTime: 2021-04-28 22:01:58
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\beyond_alpha\order.py
'''
class Order(object):
    def __init__(self, id: int, type: str, code: str, shares: int, price: float, 
                    done: bool, create_date: str, deal_date: str, dsc='no description'):
        '''
        @description: 生成订单对象
        @param {id: 订单id
                type: 'b' or 's'
                code: 'SH600000'
                shares: 买入或卖出的股数
                price: 买入或卖出的价格,如果为-1则按市价买入
                done: 成交与否
                dsc: 额外的描述信息
                create_date: 订单创建的时间，202001010930
                deal_date: 订单成交的时间}
        @return {dict}       
        '''     
        self.__id = int(id)
        self.__type = str(type)
        self.__code = str(code)
        self.__shares = int(shares)
        self.__price = float(price)
        self.__done = done
        self.__dsc = str(dsc)
        self.__create_date = str(create_date)
        self.__deal_date = str(deal_date)
    
    @property
    def id(self):
        return self.__id

    @property
    def type(self):
        return self.__type
    
    @property
    def code(self):
        return self.__code

    @property
    def shares(self):
        return self.__shares
    
    @property
    def price(self):
        return self.__price
    
    @property
    def done(self):
        return self.__done
    @done.setter
    def done(self, value):
        if not isinstance(value, bool):
            raise ValueError("done must be bool")
        self.__done = value
    
    @property
    def dsc(self):
        return self.__dsc
    @dsc.setter
    def dsc(self, value):
        if not isinstance(value, str):
            raise ValueError("dsc must be str")
        self.__dsc = value
    
    @property
    def create_date(self):
        return self.__create_date
    
    @property
    def deal_date(self):
        return self.__deal_date
    @deal_date.setter
    def deal_date(self, value):
        if not isinstance(value, str):
            raise ValueError("deal_date must be str")
        if len(value) != 14:
            raise ValueError("deal_date需要包含年月日时分秒数据，时分秒均占2位")
        self.__deal_date = value
    
    def create_order(self):
        return {
            "id": self.__id,
            "type": self.__type,
            "code": self.__code,
            "shares": self.__shares,
            "price": self.__price,
            "done": self.__done,
            "dsc": self.__dsc,
            "create_date": self.__create_date,
            "deal_date": self.__deal_date
        }

    # 打印当前订单
    def err(self, msg):
        print("订单失败原因:", msg)
        print("----------订单详情如下----------")
        print("id:    ", self.__id)
        print("type:  ", self.__type)
        print("code:  ", self.__code)
        print("shares:", self.__shares)
        print("price: ", self.__price)
        print("done:  ", self.__done)
        print("dsc:   ", self.__dsc)
        print("create_date:", self.__create_date)
        print("deal_date:  ", self.__deal_date)
        print("--------------------------------")
