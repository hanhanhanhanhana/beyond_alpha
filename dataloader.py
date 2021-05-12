'''
Author: your name
Date: 2021-04-28 21:55:28
LastEditTime: 2021-05-12 13:21:57
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\beyond_alpha\dataloader.py
'''
import os
import marketer as mk

class MarketLoader:
    def __init__(self, beg=20210101, end=2050101, period='day',  
                constituent_index=None, custom_stocks=None, save_csv=False, save_dir=None):
        '''
        @description: 根据要求输出对应股票池的股票信息
        @param {beg: 开始日期，20200101
                end: 截止日期
                period: 'min' or 'day'，分别表示获取分钟级别与日级别的数据
                constituent_index: 各种股指对应的成分股
                custom_stocks: 用户自定义股票池，['SH600000','SZ000002',....]
                save_csv: 是否需要保存数据到本地
                save_dir: 保存数据到本地的路径}
        @return {dict: key为股票代码 val为二维numpy D1：202001011030, D2: features}
        '''
        self.__beg = beg
        self.__end = end
        self.__period = period
        self.__constituent_index = constituent_index
        self.__custom_stocks = custom_stocks
        self.__save_csv = save_csv
        self.__save_dir = save_dir
        
    # 处理save_csv与save_dir匹配问题
    def _handle_save_dir(self):
        if self.__save_csv is False and self.__save_dir is not None:
            raise Exception('save_dir勿须设置!')
        elif self.__save_csv is True and self.__save_dir is None:
            raise Exception('请设置save_dir!')
        elif self.__save_csv is True and self.__save_dir is not None:
            if not os.path.exists(self.__save_dir):
                os.makedirs(self.__save_dir)
                
    def load_k_history(self):    
        # 数据格式 [开盘 收盘 最高 最低 成交量 成交额 振幅 涨跌幅 涨跌额 换手率]
        self._handle_save_dir()
        # 用户未定义，默认为全市场股票
        if self.__constituent_index is None and self.__custom_stocks is None:
            dict_code_as_key, dict_date_as_key = mk.k_history(save_csv=self.__save_csv, save_dir=self.__save_dir, beg=self.__beg, end=self.__end)
        # TODO: 实现成分股
        elif self.__constituent_index is not None:
            constituent_index_stocks = []
            dict_code_as_key, dict_date_as_key = mk.k_history(stock_codes=constituent_index_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir, beg=self.__beg, end=self.__end)
        # 用户自定义股票池
        elif self.__custom_stocks is not None:
            dict_code_as_key, dict_date_as_key = mk.k_history(stock_codes=self.__custom_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir, beg=self.__beg, end=self.__end)
        elif self.__constituent_index is not None and self.__custom_stocks is not None:
            raise Exception('constituent_index与custom_stocks不能被同时设置，请选其一进行设置!')

        return dict_code_as_key, dict_date_as_key
    
    def load_bill_history(self):
        # 数据格式 [主力净流入 小单净流入 中单净流入 大单净流入 超大单净流入 主力净流入占比 小单流入净占比 中单流入净占比 
        #       大单流入净占比 超大单流入净占比 收盘价 涨跌幅]
        self._handle_save_dir()
        # 用户未定义，默认为全市场股票
        if self.__constituent_index is None and self.__custom_stocks is None:
            dict_code_as_key, dict_date_as_key = mk.bill_history(save_csv=self.__save_csv, save_dir=self.__save_dir)
        # TODO: 实现成分股
        elif self.__constituent_index is not None:
            constituent_index_stocks = []
            dict_code_as_key, dict_date_as_key = mk.bill_history(stock_codes=constituent_index_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir)
        # 用户自定义股票池
        elif self.__custom_stocks is not None:
            dict_code_as_key, dict_date_as_key = mk.bill_history(stock_codes=self.__custom_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir)
        elif self.__constituent_index is not None and self.__custom_stocks is not None:
            raise Exception('constituent_index与costom_stocks不能被同时设置，请选其一进行设置!')

        return dict_code_as_key, dict_date_as_key

    def load_bill_realtime(self):
        # 数据格式[主力净流入 小单净流入 中单净流入 大单净流入 超大单净流入]
        self._handle_save_dir()
        # 用户未定义，默认为全市场股票
        if self.__constituent_index is None and self.__custom_stocks is None:
            dict_code_as_key, dict_date_as_key = mk.bill_history_realtime(save_csv=self.__save_csv, save_dir=self.__save_dir)
        # TODO: 实现成分股
        elif self.__constituent_index is not None:
            constituent_index_stocks = []
            dict_code_as_key, dict_date_as_key = mk.bill_history_realtime(stock_codes=constituent_index_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir)
        # 用户自定义股票池
        elif self.__custom_stocks is not None:
            dict_code_as_key, dict_date_as_key = mk.bill_history_realtime(stock_codes=self.__custom_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir)
        elif self.__constituent_index is not None and self.__custom_stocks is not None:
            raise Exception('constituent_index与costom_stocks不能被同时设置，请选其一进行设置!')

        return dict_code_as_key, dict_date_as_key
    
    def load_bill_realtime_2(self):
        if self.__constituent_index is None and self.__custom_stocks is None:
            dict_code_as_key = mk.bill_history_realtime_2()
        # TODO: 实现成分股
        elif self.__constituent_index is not None:
            constituent_index_stocks = []
            dict_code_as_key = mk.bill_history_realtime_2(stock_codes=constituent_index_stocks)
        # 用户自定义股票池
        elif self.__custom_stocks is not None:
            dict_code_as_key = mk.bill_history_realtime_2(stock_codes=self.__custom_stocks)
        elif self.__constituent_index is not None and self.__custom_stocks is not None:
            raise Exception('constituent_index与costom_stocks不能被同时设置，请选其一进行设置!')

        return dict_code_as_key
    
    def load_k_realtime(self):
        # 数据格式 [未知 价格 未知 未知 成交量 成交额 均价]
        self._handle_save_dir()
        # 用户未定义，默认为全市场股票
        if self.__constituent_index is None and self.__custom_stocks is None:
            dict_code_as_key, dict_date_as_key = mk.k_history_realtime(save_csv=self.__save_csv, save_dir=self.__save_dir)
        # TODO: 实现成分股
        elif self.__constituent_index is not None:
            constituent_index_stocks = []
            dict_code_as_key, dict_date_as_key = mk.k_history_realtime(stock_codes=constituent_index_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir)
        # 用户自定义股票池
        elif self.__custom_stocks is not None:
            dict_code_as_key, dict_date_as_key = mk.k_history_realtime(stock_codes=self.__custom_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir)
        elif self.__constituent_index is not None and self.__custom_stocks is not None:
            raise Exception('constituent_index与costom_stocks不能被同时设置，请选其一进行设置!')

        return dict_code_as_key, dict_date_as_key
        
