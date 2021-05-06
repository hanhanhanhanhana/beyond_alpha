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
                    done: bool, create_date: int, deal_date:int, dsc='no description'):
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
        self.__id = id
        self.__type = type 
        self.__code = code
        self.__shares = shares
        self.__price = price
        self.__done = done
        self.__dsc = dsc
        self.__create_date = create_date
        self.__deal_date = deal_date
    
    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__type

    def get_code(self):
        return self.__code
    
    def get_shares(self):
        return self.__shares
    
    def get_price(self):
        return self.__price
    
    def is_done(self):
        return self.__done

    def get_dsc(self):
        return self.__dsc

    def get_create_date(self):
        return self.__create_date

    def get_deal_date(self):
        return self.__deal_date
    
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

