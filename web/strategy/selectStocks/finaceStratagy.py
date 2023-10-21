#!/user/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : stockProject
@File :finaceStratagy.py
@Author: Azure Qiu
@Date: 2023/4/19 0:06
@Desc: 财务指标筛选
'''
from web.utils.financialToExcel import FinancialToExcel
from web.utils.stock_base import StockBasic
import time
import matplotlib.pyplot as plt
from web.utils.dataGraphs import DataGraphs
from web.utils.MyTools import MyTools
import pandas as pd
import numpy as np


class FinaceStrategy(StockBasic):
    def __init__(self):
        super(FinaceStrategy,self).__init__()

    def operating_Progress_Rate(self, income_df):
        """
        营业收入同比增长率 TTM
        :param income_df:
        :param code:
        :return:
        """
        # print(income_df.info())
        revenue_cur = income_df["total_revenue"]
        revenue_last = income_df["total_revenue"].shift(1)
        revenue_ttm = (revenue_cur-revenue_last)/revenue_last
        return revenue_ttm

    def operating_Profit(self,income_df):
        """
        operate_profit
        营业利润（息税前利润） = 毛利润 - 营业支出（operating expenses)
        潜在收购者最有可能关注的数字
        :param income_df:
        :return:
        """
        return income_df["operate_profit"]

    def operating_Expenses(self, income_df):
        """
        占比越小越好，较高或是不断增长的营业费用，可能意味着工资膨胀或是费用管理不到位
        :param income_df:
        :return:
        """

        operating_expenses = income_df["revenue"] - income_df["oper_cost"] - income_df["operate_profit"]
        income_df['operating_expenses'] = operating_expenses/income_df["revenue"]
        return income_df['operating_expenses']

    def gross_Profit(self, income_df):
        """
        年毛利
        :param income_df:
        :param code:
        :return:
        """
        income_df["gross_profit"] = income_df["revenue"] - income_df["oper_cost"]

        return income_df["gross_profit"]

    def gross_Profit_Rate(self, income_df):
        """
        年毛利率
        :param income_df:
        :param code:
        :return:
        """

        income_df["grossProfit"] = income_df["revenue"] - income_df["oper_cost"]

        return income_df["grossProfit"]/income_df["total_revenue"]

    def diluted_EPS_Rate(self, income_df):
        """
        稀释后每股收益和基本每股收益之差比，如果数值很大，则说明股票并不如想想中便宜
        :param income_df:
        :return:
        """
        rate = income_df["basic_eps"] - income_df["diluted_eps"] / income_df["basic_eps"]
        return rate

    def net_Income(self, income_df):
        """
        年净利润
        :param income_df:
        :return:
        """

        return income_df["n_income"]

    def net_Income_Rate(self, income_df):
        """
        年净利润率
        :param income_df:
        :return:
        """

        income_df["n_income_rate"] = income_df["n_income"] / income_df["total_revenue"]
        return income_df["n_income_rate"]

    def ROE(self, income_df):
        """
        净资产收益率
        :param income_df:
        :return:
        """
        return income_df["n_income"]/income_df["compr_inc_attr_p"]

    def ROA(self, income_df, balance_df):
        """
        资产回报率。衡量公司利用所有资产获取回报的效率
        :param income_df:
        :return:
        """
        # print(balance_df["total_assets"])
        return income_df["n_income"]/balance_df["total_assets"]

    def fix_Assets_Rate(self, income_df, balance_df):
        """
        固定资产占比.一般固资占比低的企业营运能力强
        :param balance_df:
        :return:
        """
        return balance_df["fix_assets_total"]/balance_df["total_assets"]

    def turnOver(self, income_df,balance_df):
        """
        存货周转率, 存货周转率高，销售能力强
        :return:
        """
        return income_df["total_revenue"]/balance_df["inventories"]

    def accounts_Receiv_Rate(self, income_df, balance_df):
        """
        应收账款周转率
        :param income_df:
        :param balance_df:
        :return:
        """
        return income_df["total_revenue"]/balance_df["accounts_receiv"]

    def total_Assets_Turnover(self, income_df, balance_df):
        """
        总资产周转率
        :param income_df:
        :param balance_df:
        :return:
        """
        return income_df["total_revenue"]/balance_df["total_assets"]

    def cur_Rate(self, balance_df):
        """
        流动比率。衡量企业短期偿债能力
        :param balance_df:
        :return:
        """
        balance_df["cur_rate"] = balance_df["total_cur_assets"]/balance_df["total_cur_liab"]
        return balance_df["cur_rate"]

    def lia_Assets_Rate(self, balance_df):
        """
        资产负债率。负债率上涨并伴随实现较高利润，则说明企业经营活动是良性的
        :param balance_df:
        :return:
        """
        balance_df["lia_asset"] = balance_df["total_liab"]/balance_df["total_assets"]
        return balance_df["lia_asset"]

    def interest_Payable(self, income_df):
        """
        利息保障倍数，衡量企业偿付借款利息的能力。倍数越大，说明企业支付利息费用的能力越强
        :param income_df:
        :return:
        """
        income_df["int_payable"] = income_df["ebit"]/income_df["int_exp"]
        return income_df["int_payable"]

    def bookValue(self, balance_df):
        """
        每股账面价值 = （资产 - 负债）  即所有者权益
        :param balance_df:
        :return:
        """
        # total_share = self.get_Total_Share(code, start_date, end_date) * 10000
        book_value = balance_df["total_hldr_eqy_inc_min_int"]
        return book_value

    def debt_To_Equalty_Ratio(self, balance_df):
        """
        杠杆比率，
        :param balance_df:
        :return:
        """
        balance_df["debt_equalty"] =  balance_df["total_liab"]/balance_df["total_hldr_eqy_inc_min_int"]

        return balance_df["debt_equalty"]

    def working_Capital(self, balance_df):
        """
        营运资金
        :param balance_df:
        :return:
        """
        balance_df["work_capital"] = balance_df["total_cur_assets"] - balance_df["total_cur_liab"]
        return balance_df["work_capital"]

    def quick_Ratio(self, balance_df):
        """
        速动比率，反映企业用短期资金偿付短期负债的能力
        :param balance_df:
        :return:
        """
        return (balance_df["total_cur_assets"]-balance_df["inventories"])/ balance_df["total_cur_liab"]

    def inventory_Revenue_Ratio(self, income_df, balance_df):
        """
        存货与销售额的比值是否逐年稳步增长。存货积压量的增加可能说明市场吸引力正在下降，盈利能力受到威胁
        :param balance_df:
        :param income_df:
        :return:
        """
        return balance_df["inventories"]/income_df["total_revenue"]


    def CAGR_5(self, income_df):
        """复合增长率"""

        income_df_5 = income_df.tail(5)
        CAGR = (income_df_5['n_income'].iloc[4]/income_df_5['n_income'].iloc[0])**(1/4)-1
        return CAGR


if __name__ == "__main__":
    code_list =  ['000046.SZ', '000667.SZ', '000682.SZ', '000950.SZ', '002212.SZ', '600103.SH', '600133.SH', '600959.SH', '601949.SH']
    f_excel = FinancialToExcel()

    # income_df = f_excel.finance_Income_readToDf('000623.SZ')
    # 002050 三花智控 000521 长虹美菱 002242 九阳股份 002959 小熊电器
    # 003035 南网 600089 特变电工
    # 000021 深科技
    # 002294.SZ 信立泰 600276.HS 恒瑞医药 000963 华东医药 002821凯莱英 002001 新和成 002422 科伦药业 600079 人福医药
    # 300558 贝达药业  600521 华海药业
    code = "000963.SZ"
    code1 = "002294.SZ"
    code2 = "600276.SH"
    code3 = "002821.SZ"
    code4 = "002001.SZ"
    code5 = "002422.SZ"


    income_df = f_excel.finance_Income_readToDf(code)
    income_df1 = f_excel.finance_Income_readToDf(code1)
    income_df2 = f_excel.finance_Income_readToDf(code2)
    income_df3 = f_excel.finance_Income_readToDf(code3)
    income_df4 = f_excel.finance_Income_readToDf(code4)
    income_df5 = f_excel.finance_Income_readToDf(code5)
    # income_df6 = f_excel.finance_Income_readToDf(code6)



    # balance_df = f_excel.finance_Balance_readToDf(code)
    # balance_df1 = f_excel.finance_Balance_readToDf(code1)
    # balance_df2 = f_excel.finance_Balance_readToDf(code2)
    # balance_df3 = f_excel.finance_Balance_readToDf(code3)
    # balance_df4 = f_excel.finance_Balance_readToDf(code4)
    # balance_df5 = f_excel.finance_Balance_readToDf(code5)
    # balance_df6 = f_excel.finance_Balance_readToDf(code6)


    f = FinaceStrategy()

    # 个股纵向对比

    yl_df = income_df[1:].resample('Y', on='end_date').sum()
    yl_df1 = income_df1[1:].resample('Y', on='end_date').sum()
    yl_df2 = income_df2[1:].resample('Y', on='end_date').sum()
    yl_df3 = income_df3[1:].resample('Y', on='end_date').sum()
    yl_df4 = income_df4[1:].resample('Y', on='end_date').sum()
    yl_df5 = income_df5[1:].resample('Y', on='end_date').sum()
    # yl_df6 = income_df6[1:].resample('Y', on='end_date').sum()


    # yl_balance = balance_df[1:].resample('Y', on='end_date').sum()
    # yl_balance1 = balance_df1[1:].resample('Y', on='end_date').sum()
    # yl_balance2 = balance_df2[1:].resample('Y', on='end_date').sum()
    # yl_balance3 = balance_df3[1:].resample('Y', on='end_date').sum()
    # yl_balance4 = balance_df4[1:].resample('Y', on='end_date').sum()
    # yl_balance5 = balance_df5[1:].resample('Y', on='end_date').sum()
    # yl_balance6 = balance_df6[1:].resample('Y', on='end_date').sum()


    # gross_profit = f.gross_Profit(yl_df6)
    # net_Income = f.net_Income(yl_df6)
    # working_Capital = f.working_Capital(yl_balance6)
    # operating_Profit = f.operating_Profit(yl_df6)
    # bookValue = f.bookValue(yl_balance6)
    # dd = {"gross_profit": gross_profit, "net_Income": net_Income,"working_Capital": working_Capital, "operating_Profit": operating_Profit,
    #      "bookValue": bookValue }

    # data = pd.DataFrame(dd)
    # data.plot(kind='bar')
    # plt.show()

    net_income_rate = f.operating_Progress_Rate(yl_df)
    net_income_rate1 = f.operating_Progress_Rate(yl_df1)
    net_income_rate2 = f.operating_Progress_Rate(yl_df2)
    net_income_rate3 = f.operating_Progress_Rate(yl_df3)
    net_income_rate4 = f.operating_Progress_Rate(yl_df4)
    net_income_rate5 = f.operating_Progress_Rate(yl_df5)
    # print(net_income_rate, net_income_rate1, net_income_rate2, net_income_rate3, net_income_rate4,net_income_rate5)
    dd = {"HuaDong": net_income_rate, "XinLiTai": net_income_rate1,"HengRui": net_income_rate2, "KaiLaiYing": net_income_rate3,
         "XinHeCheng": net_income_rate4, "KeLun": net_income_rate5}
    #
    data = pd.DataFrame(dd)
    data.plot()
    plt.show()


    # cur = f.cur_Rate(yl_balance)
    # cur1 = f.cur_Rate(yl_balance1)
    # cur2 = f.cur_Rate(yl_balance2)
    # cur3 = f.cur_Rate(yl_balance3)

    # debt = f.debt_To_Equalty_Ratio(yl_balance)
    # debt1 = f.debt_To_Equalty_Ratio(yl_balance1)
    # debt2 = f.debt_To_Equalty_Ratio(yl_balance2)
    # debt3 = f.debt_To_Equalty_Ratio(yl_balance3)

    # lia = f.lia_Assets_Rate(yl_balance)
    # lia1 = f.lia_Assets_Rate(yl_balance1)
    # lia2 = f.lia_Assets_Rate(yl_balance2)
    # lia3 = f.lia_Assets_Rate(yl_balance3)

    # quick = f.quick_Ratio(yl_balance)
    # quick1 = f.quick_Ratio(yl_balance1)
    # quick2 = f.quick_Ratio(yl_balance2)
    # quick3 = f.quick_Ratio(yl_balance3)

    # dd = {"9yang": quick, "3hua": quick1,"meiLing": quick2, "xiaoXiong": quick3}
    # data = pd.DataFrame(dd)
    # data.sort_index(ascending=False, inplace=True)

    # s =  income_df[['total_revenue','n_income', 'grossProfit', 'operating_expenses']]

    # data.plot()
    # plt.show()

    #年初至今涨辐
    # sb = StockBasic()
    # start_price = sb.pro.daily(ts_code=code, trade_date="20230103")["close"]
    # end_price = sb.pro.daily(ts_code=code, trade_date="20230516")["close"]
    # A = (end_price-start_price)/start_price*100
    # print(A)
    # yl_income_df['n_income'].plot(kind='bar', ax=ax)

    # yearly_netIncome = season_netIncome.shift(-1).groupby([n // 4 for n in range(len(season_netIncome))]).sum()
    # yearly_revenue.plot(kind='bar')
    # yearly_netIncome.plot(kind='bar')


    # d1 = f.net_Income_Rate(income_df1)


    # yearly_netIncomeRate = d.shift(-1).groupby([n // 4 for n in range(len(d))]).sum()
    # yearly_netIncomeRate1 = d1.shift(-1).groupby([n // 4 for n in range(len(d1))]).sum()
    # index = min(len(yearly_netIncomeRate),len(yearly_netIncomeRate1))
    # print(yearly_netIncomeRate.tolist())
    # dd = {"jilinAoDong": yearly_netIncomeRate[:index].tolist(), "XinLiTai":yearly_netIncomeRate1.tolist()}
    # data = pd.DataFrame(dd)
    # data.sort_index(ascending=False, inplace=True)
    # data.plot()
    # plt.show()
    # data.reset_index()
    # print(data)

    # DataGraphs.draw_diff("netIncomeRate_3", 0,jilinAoDong=yearly_netIncomeRate[-index:], XinLiTai=yearly_netIncomeRate1)





