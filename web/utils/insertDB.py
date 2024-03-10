#!/user/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : django_demo
@File :insertDB.py
@Author: Azure Qiu
@Date: 2023/6/8 14:55
@Desc: 股票基本信息写数据库，股票名，代码，上市时间，行业，上市板块，退市时间
'''

import pymysql
from sqlalchemy import create_engine
import datetime
import pandas as pd
from web.utils.MyTools import MyTools
import tushare as ts
from scipy.stats import stats


class PdToSql:
    def __init__(self):
        pymysql.install_as_MySQLdb()
        self.db_String = 'mysql+mysqldb://root:123456@127.0.0.1/stock_db?charset=utf8'
        self.pro = ts.pro_api("da4c97957d6f4063991d86f1ccce4c43c6c0275d6b640e706ae9ff9d")

    def pd_to_sql(self,dataframe,table_name):
        engine = create_engine(self.db_String)
        dataframe.to_sql(table_name,con=engine, if_exists="append", index=False)
        engine.dispose()

    def pd_from_sql(self, sql):
        db = pymysql.connect(host='localhost',
                        user='root',
                        password='123456',
                        database='stock_db')
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return results



    def update_3Sheets(self, s_date, e_date):
        # 股票基本信息表
        pro = self.pro
        stock_df = pro.stock_basic(fields='ts_code, name, list_date, industry, market, delist_date')
        #   财务报表
        code_list = stock_df["ts_code"].to_list()
        for code in range(len(code_list)):
            # 手动更新三张表。起止时间由人填写
            income = pro.income(ts_code=code_list[code],start_date=s_date,end_date=e_date)
            balance = pro.balancesheet(ts_code=code_list[code],start_date=s_date,end_date=e_date)
            cashflow = pro.cashflow(ts_code=code_list[code],start_date=s_date,end_date=e_date)
            cashflow['end_date'] = pd.to_datetime(cashflow['end_date'])
            # df = cashflow.drop_duplicates(subset=["end_date"], keep='last')
            print(code_list[code])
            # print(income)
            # p_to_sql = PdToSql()
            self.pd_to_sql(income, 'web_income')
            self.pd_to_sql(balance, 'web_balance')
            self.pd_to_sql(cashflow, 'web_cashflow')

    def update_index(self):
        index_df = self.pro.index_basic()
        self.pd_to_sql(index_df, 'web_index_info')

    def update_index_dailybasic(self, ts_code):
        df = self.pro.index_dailybasic(ts_code=ts_code)
        if not df.empty:
            self.pd_to_sql(df, 'web_index_dailybasic')
        else:
            return []

    def update_index_daily(self, ts_code):

        df = self.pro.index_daily(ts_code=ts_code)
        if not df.empty:
            self.pd_to_sql(df, 'web_index_daily')
        else:
            return []


    def update_daily(self,**kwargs):
        """指数每日行情"""
        print("======执行每日指数行情更新数据库======")
        sql = "select DISTINCT ts_code from web_index_daily"
        codes = self.pd_from_sql(sql)
        for row in codes:
            if not kwargs:
                today = datetime.datetime.today()
                dt = today.date()
                d = MyTools.str_time(dt)
                df = self.pro.index_daily(ts_code=row[0], trade_date=d)
            else:
                for key, value in kwargs.items():
                    if key == 'start_date':
                        s_date = value
                    elif key == 'end_date':
                        e_date = value
                print([row[0],s_date,e_date])
                df = self.pro.index_daily(ts_code=row[0], start_date=s_date, end_date=e_date)
                print(df)
            if not df.empty:
                self.pd_to_sql(df, 'web_index_daily')
            else:
                continue

    def update_dailybasics(self, **kwargs):
        """指数每日行情"""
        print("======执行每日指数指标更新数据库======")
        sql = "select DISTINCT ts_code from web_index_dailybasic "
        # ts_code_list = []
        codes = self.pd_from_sql(sql)
        for row in codes:
            if not kwargs:
                today = datetime.datetime.today()
                dt = today.date()
                d = MyTools.str_time(dt)
                self.pro.index_dailybasic(ts_code=row[0], trade_date=d)
            else:
                for key, value in kwargs.items():
                    if key == 'start_date':
                        s_date = value
                    elif key == 'end_date':
                        e_date = value
                for row in codes:

                    df = self.pro.index_dailybasic(ts_code=row[0], start_date=s_date, end_date=e_date)
                    if not df.empty:
                        self.pd_to_sql(df, 'web_index_dailybasic')
                    else:
                        continue

if __name__ == "__main__":

    p_to_sql = PdToSql()
    # p_to_sql.update_daily(start_date="20240302", end_date="20240306")
    # p_to_sql.update_dailybasics(start_date="20240302", end_date="20240306")
    # p_to_sql.update_3Sheets(s_date="20240101", e_date="20240430")
    # p_to_sql.update_daily('000001.SH')
    # d = [6,4,5,7,9,22,1,10]
    # percentile = stats.percentileofscore(d, 9)
    # print(percentile)
