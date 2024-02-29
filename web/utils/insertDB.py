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
from web.utils.financialToExcel import FinancialToExcel
import pandas as pd
import os
import tushare as ts


class PdToSql:
    def __init__(self):
        pymysql.install_as_MySQLdb()
        self.db_String = 'mysql+mysqldb://root:123456@127.0.0.1/stock_db?charset=utf8'

    def pd_to_sql(self,dataframe,table_name):
        engine = create_engine(self.db_String)
        dataframe.to_sql(table_name,con=engine, if_exists="append", index=False)
        engine.dispose()

    def update_3Sheets(self, s_date, e_date):
        # 股票基本信息表
        pro = ts.pro_api("da4c97957d6f4063991d86f1ccce4c43c6c0275d6b640e706ae9ff9d")
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

if __name__ == "__main__":
    p_to_sql = PdToSql()
    p_to_sql.update_3Sheets(s_date="20240101", e_date="20240430")

