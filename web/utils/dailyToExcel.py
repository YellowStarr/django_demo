#!/user/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : stockProject
@File :dailyToExcel.py
@Author: Azure Qiu
@Date: 2023/4/18 19:23
@Desc：每日收盘数据写回excel
'''

from utils.stock_base import StockBasic
from utils.MyTools import MyTools
import pandas as pd

class DailyToExcel(StockBasic):
    def __init__(self):
        super(DailyToExcel, self).__init__()
        self.root_dir = "E:\\WorkPlace\\stockProject\\stock\\"

    def updateDaily(self, trade_day=''):
        # filename_list = MyTools.walk_dirs(self.root_dir)
        # print(type(filename_list))

        all_stocks_df = self.get_stock_code()
        all_stocks_list = all_stocks_df["ts_code"].tolist()

        if not trade_day:
            trade_day = MyTools.get_today()
        for code in range(len(all_stocks_list)):
            file_path = self.root_dir + all_stocks_list[code] + "_daily.csv"
            # print(all_stocks_list[code])
            code_df = self.pro_bar(all_stocks_list[code],s_date=trade_day, e_date=trade_day)
            if not code_df.empty:
                   code_df.to_csv(file_path, mode='a', header=False)

    def compositIndex(self, code="000001.SH", trade_day=''):
        file_path = self.root_dir + code + "_daily.csv"
        if trade_day != '':
            code_df = self.pro.index_daily(ts_code=code,s_date=trade_day, e_date=trade_day)
        else:
            code_df = self.pro.index_daily(ts_code=code)
        if not code_df.empty:
            code_df.to_csv(file_path, mode='a', header=False)


    def daily_readToDf(self, code):
        file_path = self.root_dir + code + "_daily.csv"
        df = pd.read_csv(file_path, index_col=0)
        df["trade_date"] = pd.to_datetime(df["trade_date"].astype('str'))
        df.set_index(df["trade_date"], inplace=True)
        df.sort_index(ascending=True, inplace=True)
        return df


    def insertPeriod(self, s_date, e_date=''):
        """
        增加一段时期内的价格
        :param s_date:
        :param e_date:
        :return:
        """

        all_stocks_df = self.get_stock_code()
        all_stocks_list = all_stocks_df["ts_code"].tolist()

        if not e_date:
            e_date = MyTools.get_today()
        for code in range(len(all_stocks_list)):
            file_path = self.root_dir + all_stocks_list[code] + "_daily.csv"
            # print(all_stocks_list[code])
            code_df = self.pro_bar(all_stocks_list[code],s_date=s_date, e_date=e_date)
            try:
                if not code_df.empty:
                    code_df.to_csv(file_path, mode='a', header=False)
            except Exception as e:
                print("获取日线出错，code:", all_stocks_list[code])


if __name__ == "__main__":
    d = DailyToExcel()
    d.insertPeriod("20230517","20230522")
    # d.compositIndex("399005.SZ")



