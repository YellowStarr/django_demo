#!/user/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : stockProject
@File :increaseVolumn.py
@Author: Azure Qiu
@Date: 2023/4/18 19:19
@Desc: 放量选股
'''

from pandas import DataFrame
from utils.dailyToExcel import DailyToExcel
from utils.stock_base import StockBasic

class IncreaseVolumn(StockBasic):
    def __init__(self, code):
        super(IncreaseVolumn, self).__init__()
        self.path = ''
        self.total_num = 0
        self.up1_num = 0
        self.up3_num = 0
        self.up5_num = 0
        self._daily = DailyToExcel()
        self.df = self._daily.daily_readToDf(code)

    def set_num_clear(self):
        self.total_num = 0
        self.up1_num = 0
        self.up3_num = 0
        self.up5_num = 0

    def total_increase_df(self):
        # 获取历史上的放量数据
        # print((self.df['vol']-self.df['vol'].shift(1))>2*self.df['vol'].shift(1))
        vol_df = self.df.loc[(self.df['vol']-self.df['vol'].shift(1))>2*self.df['vol'].shift(1)]
        return vol_df

    def close_up_df(self):
        """
        收盘当天上涨的放量数据
        :return:
        """
        # 获取历史上的放量数据
        vol_df = self.total_increase_df()
        close_df  = vol_df[vol_df['close'].lt(vol_df['open'])]
        return close_df

    def up_df(self, total_increase_df,day=1):
        """
        N日上涨数
        :param total_increase_df: 历史上总放量df
        :param day: -1，-3，-5
        :return:
        """
        day = 0-day
        up_df = self.df.loc[self.df['close'].shift(day)-self.df.loc[total_increase_df.index]["close"]>0]
        return up_df

    def compare_vol(self):
        """
        无论当日收盘涨跌，计算总的放量次数及1日，3日，5日上涨概率
        :return:
        """
        # 获取历史上的放量数据
        vol_df = self.total_increase_df()
        # 历史总放量数
        total_num = vol_df.shape[0]
        if total_num:
            self.total_num = self.total_num + total_num
            up_df = self.up_df(vol_df)
            # 一天后上涨数
            up_num = up_df.shape[0]
            self.up1_num += up_num
            # 一日后上涨概率为
            day1_up_percentage = up_num/total_num *100
            # print(day1_up_percentage)

            # 三日后上涨
            up3_df = self.up_df(vol_df, 3)
            # 三日后上涨数
            up3_num = up3_df.shape[0]
            self.up3_num += up3_num
            # 三日后上涨概率为
            day3_up_percentage = up3_num/total_num *100
            # print(day3_up_percentage)

            # 五日后上涨
            up5_df = self.up_df(vol_df, 5)
            # 5日后上涨数
            up5_num = up5_df.shape[0]
            self.up5_num += up5_num
            # 5日后上涨概率为
            day5_up_percentage = up5_num/total_num *100
            # print(day5_up_percentage)

    def close_down(self):
        """
        当日收盘下跌,计算总的放量次数及1日，3日，5日上涨概率
        :return:
        """
        # 获取历史上的放量数据
        vol_df = self.total_increase_df()
        # 历史总放量数
        total_num = vol_df.shape[0]
        self.total_num += total_num
        if total_num:
            # 在一日上涨中，筛选出当日收盘下跌的数量
            close_df  = vol_df[vol_df['close'].lt(vol_df['open'])]
            up1_df = self.up_df(close_df)
            up1_num = up1_df.shape[0]

            self.up1_num += up1_num
            # 一日后上涨概率为
            day1_up_percentage = up1_num/total_num *100
            print(day1_up_percentage)

            # 三日后上涨
            up3_df = self.up_df(close_df, 3)
            # 三日后上涨数
            up3_num = up3_df.shape[0]
            self.up3_num += up3_num
            # 三日后上涨概率为
            day3_up_percentage = up3_num/total_num *100
            print(day3_up_percentage)

            # 五日后上涨
            up5_df = self.up_df(close_df, 5)
            # 5日后上涨数
            up5_num = up5_df.shape[0]
            self.up5_num += up5_num
            # 5日后上涨概率为
            day5_up_percentage = up5_num/total_num *100
            print(day5_up_percentage)

    def close_up(self):
        """
        当日收盘上涨,计算总的放量次数及1日，3日，5日上涨概率
        :return:
        """
        # 获取历史上的放量数据
        vol_df = self.total_increase_df()
        # 历史总放量数
        total_num = vol_df.shape[0]
        self.total_num += total_num
        if total_num:
            # 在一日上涨中，筛选出当日收盘下跌的数量
            close_df  = vol_df[vol_df['close'].gt(vol_df['open'])]
            up1_df = self.up_df(close_df)
            up1_num = up1_df.shape[0]

            self.up1_num += up1_num
            # 一日后上涨概率为
            day1_up_percentage = up1_num/total_num *100
            print(day1_up_percentage)

            # 三日后上涨
            up3_df = self.up_df(close_df, 3)
            # 三日后上涨数
            up3_num = up3_df.shape[0]
            self.up3_num += up3_num
            # 三日后上涨概率为
            day3_up_percentage = up3_num/total_num *100
            print(day3_up_percentage)

            # 五日后上涨
            up5_df = self.up_df(close_df, 5)
            # 5日后上涨数
            up5_num = up5_df.shape[0]
            self.up5_num += up5_num
            # 5日后上涨概率为
            day5_up_percentage = up5_num/total_num *100
            print(day5_up_percentage)

    def times_Of_Vol(self):
        """
        放量倍数与后续上涨的关系
        :return:
        """
        # 获取历史上的放量数据
        vol_df = self.total_increase_df()
        # 历史总放量数
        total_num = vol_df.shape[0]
        self.total_num += total_num
        if total_num:
            # 在一日上涨中，筛选出当日收盘上涨的数量
            up1_df = self.up_df(vol_df)
            # 获取放量倍数
            self.up1_num += up1_df.shape[0]
            # 3
            vol3_df = up1_df.loc[(up1_df['vol']-up1_df['vol'].shift(1))>=3*up1_df['vol'].shift(1)]
            vol3_num = vol3_df.shape[0]
            print(vol3_num)

            self.up3_num += vol3_num

            vol4_df = up1_df.loc[(up1_df['vol']-up1_df['vol'].shift(1))>=4*up1_df['vol'].shift(1)]
            vol4_num = vol4_df.shape[0]
            print(vol4_num)
            self.up5_num += vol4_num

    def total_Percentage(self):

        print(self.total_num)
        print(self.up1_num)
        print(self.up3_num)
        print(self.up5_num)
        up1 = self.up1_num/self.total_num*100
        up3 = self.up3_num/self.total_num*100
        up5 = self.up5_num/self.total_num*100
        print("所有股票1日后上涨率为", up1)
        print("所有股票3日后上涨率为", up3)
        print("所有股票5日后上涨率为", up5)


    def average_5day(self):
        """
        5日均线
        :return:
        """
        self.df["ma5"] = self.df["close"].rolling(5).mean()

    def trend(self):
        """
        5日线趋势
        :return:
        """
        increase = self.total_increase_df()
        self.average_5day()
        down_trend_df = increase.loc[self.df["ma5"].gt(self.df["ma5"].shift(1))]
        return down_trend_df