# -*- coding: utf-8 -*-
# ---
# @File: financialIndex
# @Author: QiuWenJing
# @Time: 三月 10, 2024
# @Description: 财务指标封装
# ---
from web import models

class FinancialIndex:
    def __init__(self):
        pass

    def get_PE_TTM(self,ts_code, trade_date):
        query = models.stock_daily.objects.filter(ts_code=ts_code,trade_date=trade_date)
        return query.values("PE_TTM")

    def get_PB(self,ts_code, trade_date):
        query = models.stock_daily.objects.filter(ts_code=ts_code,trade_date=trade_date)
        return query.values("PB")

    def get_Capital(self,ts_code, trade_date):
        query = models.stock_daily.objects.filter(ts_code=ts_code,trade_date=trade_date)
        return query.values("total_mv")
