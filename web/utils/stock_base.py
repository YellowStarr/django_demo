#!/user/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : stockProject
@File :stock_base.py
@Author: Azure Qiu
@Date: 2023/4/13 12:49
'''

import tushare as ts


class StockBasic:
    def __init__(self):
        _token = "da4c97957d6f4063991d86f1ccce4c43c6c0275d6b640e706ae9ff9d"
        self.pro = ts.pro_api(_token)

    def get_stock_code(self):
        """返回剔除了北交所和科创板,创业板的上市公司"""
        print("==============get_stock_code==============")
        stock_df = self.pro.stock_basic()
        index1 = stock_df[stock_df["market"] == "北交所"].index
        index2 = stock_df[stock_df["market"] == "科创板"].index
        index3 = stock_df[stock_df["market"] == "创业板"].index
        stock_df.drop(index1, inplace=True)
        stock_df.drop(index2, inplace=True)
        stock_df.drop(index3, inplace=True)
        # self._stock_list = stock_df
        print(stock_df.shape)
        return stock_df

    def get_Total_Share(self, code, trade_date):
        try:
            basic_df = self.pro.daily_basic(ts_code=code, trade_date=trade_date)
        except Exception as e:
            print(basic_df)
            print(e)
        return basic_df['total_share']

    def get_Trade_Calender(self, start_date, end_date, is_open=1):
        trade_cal = self.pro.trade_cal(exchange='', start_date=start_date,end_date=end_date, is_open=is_open)
        return trade_cal

    def pro_bar(self, code,s_date, e_date, asset='E', adj='qfq', adjfactor=True):
        df = ts.pro_bar(ts_code=code,start_date=s_date, end_date=e_date, asset=asset, adj=adj, adjfactor=adjfactor)
        return df

    def get_Industry(self, code):
        """
        获取企业所属行业。申万
        :param code:
        :return: dataframe
        """
        industry_df = self.pro.index_member(ts_code=code)
        return industry_df

    def get_Concept(self):
        """
        获取概念股分类
        :param index_code:
        :return:
        """
        concept_df = self.pro.concept()
        return concept_df

    def get_Stock_Concept(self, code):
        """
        获取股票关联概念
        :param code:
        :return:
        """
        concept = self.pro.concept_detail(ts_code=code)
        return concept

    def get_Concept_Contains(self, id):
        """
        获取概念股分类明细
        :param id:
        :return:
        """
        concept_container = self.pro.concept_detail(id=id)
        return concept_container

    def stock_MV(self, code):
        """小沛动量
        """
        mv = self.pro.stock_mx(ts_code = code)
        return mv

    def stock_MV_Daily(self, trade_date='', start_date='', end_date=''):
        """小沛动量
        """
        if start_date and end_date:

                mv = self.pro.stock_mx(start_date = start_date, end_date=end_date)

        else:
            try:
                mv = self.pro.stock_mx(trade_date = trade_date)
            except Exception as e:
                print(trade_date)
                print(mv)
        return mv




