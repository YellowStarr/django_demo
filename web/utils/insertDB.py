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
import pandas as pd
import os
import tushare as ts




# pro = ts.pro_api("da4c97957d6f4063991d86f1ccce4c43c6c0275d6b640e706ae9ff9d")
# stock = pro.stock_basic()
# stocks = stock["ts_code"].tolist()

class PdToSql:
    def __init__(self):
        pymysql.install_as_MySQLdb()
        self.db_String = 'mysql+mysqldb://root:123456@127.0.0.1/stock_db?charset=utf8'

    def pd_to_sql(self,dataframe,table_name):
        engine = create_engine(self.db_String)
        dataframe.to_sql(table_name,con=engine, if_exists="append", index=False)
        engine.dispose()

if __name__ == "__main__":
    pro = ts.pro_api("da4c97957d6f4063991d86f1ccce4c43c6c0275d6b640e706ae9ff9d")
    stock_df = pro.stock_basic(fields='ts_code, name, list_date, industry, market, delist_date')
    p_to_sql = PdToSql()
    p_to_sql.pd_to_sql(stock_df, 'web_stock_info')


