'''
Author: your name
Date: 2021-04-28 21:55:28
LastEditTime: 2021-05-07 10:48:09
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \code\beyond_alpha\dataloader.py
'''
import marketer as mk

class MarketLoader:
    def __init__(self, beg: int, end: int, period: str,  
                constituent_index=None, costom_stocks=None, save_csv=False, save_dir=None):
        '''
        @description: 根据要求输出对应股票池的股票信息
        @param {beg: 开始日期，20200101
                end: 截止日期
                period: 'min' or 'day'，分别表示获取分钟级别与日级别的数据
                constituent_index: 各种股指对应的成分股
                costom_stocks: 用户自定义股票池，['SH600000','SZ000002',....]
                save_csv: 是否需要保存数据到本地
                save_dir: 保存数据到本地的路径}
        @return {dict: key为股票代码 val为二维numpy D1：202001011030, D2: features}
        '''   
        self.__beg = beg
        self.__end = end
        self.__period = period
        self.__constituent_index = constituent_index
        self.__costom_stocks = costom_stocks
        self.__save_csv = save_csv
        self.__save_dir = save_dir
        
        
        
    def load_k_history(self):
        # 处理save_csv与save_dir匹配问题
        if self.__save_csv is False and self.__save_dir is not None:
            raise Exception('save_dir勿须设置!')
        elif self.__save_csv is True and self.__save_dir is None:
            raise Exception('请设置save_dir!')
        elif self.__save_csv is True and self.__save_dir is not None:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

        # 用户未定义，默认为全市场股票
        if self.__constituent_index is None and self.__costom_stocks is None:
            dict_code_as_key, dict_date_as_key = mk.k_history(save_csv=self.__save_csv, save_dir=self.__save_dir, beg=self.__beg, end=self.__end)
        # TODO: 实现成分股
        elif constituent_index is not None:
            constituent_index_stocks = []
            dict_code_as_key, dict_date_as_key = mk.k_history(stock_codes=constituent_index_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir, beg=self.__beg, end=self.__end)
        # 用户自定义股票池
        elif costom_stocks is not None:
            dict_code_as_key, dict_date_as_key = mk.k_history(stock_codes=self.__costom_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir, beg=self.__beg, end=self.__end)
        elif self.__constituent_index is not None and self.__costom_stocks is not None:
            raise Exception('constituent_index与costom_stocks不能被同时设置，请选其一进行设置!')

        return dict_code_as_key, dict_date_as_key
    
    def load_bill_history(self):
        # 处理save_csv与save_dir匹配问题
        if self.__save_csv is False and self.__save_dir is not None:
            raise Exception('save_dir勿须设置!')
        elif self.__save_csv is True and self.__save_dir is None:
            raise Exception('请设置save_dir!')
        elif self.__save_csv is True and self.__save_dir is not None:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

        # 用户未定义，默认为全市场股票
        if self.__constituent_index is None and self.__costom_stocks is None:
            dict_code_as_key, dict_date_as_key = mk.k_history(save_csv=self.__save_csv, save_dir=self.__save_dir, beg=self.__beg, end=self.__end)
        # TODO: 实现成分股
        elif constituent_index is not None:
            constituent_index_stocks = []
            dict_code_as_key, dict_date_as_key = mk.k_history(stock_codes=constituent_index_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir, beg=self.__beg, end=self.__end)
        # 用户自定义股票池
        elif costom_stocks is not None:
            dict_code_as_key, dict_date_as_key = mk.k_history(stock_codes=self.__costom_stocks, save_csv=self.__save_csv, save_dir=self.__save_dir, beg=self.__beg, end=self.__end)
        elif self.__constituent_index is not None and self.__costom_stocks is not None:
            raise Exception('constituent_index与costom_stocks不能被同时设置，请选其一进行设置!')

        return dict_code_as_key, dict_date_as_key
        
        
