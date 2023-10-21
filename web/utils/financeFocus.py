#!/user/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : stockProject
@File :financeFocus.py
@Author: Azure Qiu
@Date: 2023/5/20 10:37
@Desc: 财报主要关注信息重组。 十一张图表
'''

from web.strategy.selectStocks.finaceStratagy import FinaceStrategy
from web.utils.financialToExcel import FinancialToExcel
import pandas as pd
from web.utils.dailyToExcel import DailyToExcel
from web.utils.dataGraphs import DataGraphs
from web.utils.stock_base import StockBasic

class FinanceFocus:
    def __init__(self):
        self.finance = FinancialToExcel()
        self.strategy = FinaceStrategy()
        self.code = ''

    def _get_code(self):
        return self.code

    def _set_code(self, code):
        self.code = code

    def get_Finance(self, code):
        """
        获取三张表的年报信息
        :param code: 股票代码
        :return: income, balance, cashflow
        """
        self._set_code(code)
        income_df = self.finance.finance_Income_readToDf(code)
        balance_df = self.finance.finance_Balance_readToDf(code)
        cashflow_df = self.finance.finance_Cashflow_readToDf(code)
        month = income_df["end_date"].dt.month.head(1).values
        if  month != 12:
            income_df_yrl = income_df[1:].resample('Y', on='end_date').sum()
            balance_df_yrl = balance_df[1:].resample('Y', on='end_date').sum()
            cashflow_df_yrl = cashflow_df[1:].resample('Y', on='end_date').sum()
        else:
            income_df_yrl = income_df
            balance_df_yrl = balance_df
            cashflow_df_yrl = cashflow_df
        return income_df_yrl, balance_df_yrl, cashflow_df_yrl

    def singleStockIncomeFocus(self, income_df):
        """
        个股利润表关注内容
        :param code:
        :return:
        """
        n_income = income_df["n_income"]    # 净利润 = 利润总额-所得税
        gross_profit = self.strategy.gross_Profit(income_df)   # 毛利
        t_revenue = income_df["total_revenue"]  # 总营收
        oper_cost = income_df["oper_cost"]   # 营业成本
        total_cogs = income_df["total_cogs"]   # 营业总成本 = 营业成本+营业税金及附加+销售费用+管理费用+财务费用+资产减值损失
        sell_cost = income_df["sell_exp"]    # 销售费用
        operate_profit = income_df["operate_profit"]    # 营业利润
        total_profit = income_df["total_profit"]   # 利润总额 = 营业利润 + 营业外收入-营业外支出
        interest_payable = self.strategy.interest_Payable(income_df)   # 利息保障倍数
        roe = self.strategy.ROE(income_df)   # 净资产收益率


        dd = {"n_income": n_income, "gross_profit": gross_profit, "t_revenue": t_revenue, "oper_cost": oper_cost,
         "total_cogs": total_cogs, "sell_cost": sell_cost,"operate_profit": operate_profit, "total_profit": total_profit,
              "interest_payable": interest_payable, "roe": roe}
        data = pd.DataFrame(dd)
        return data

    def singleStockBalanceFocus(self, balance_df):
        """
        个股资产负债表关注点
        :param balance_df:
        :return:
        """
        notes_receiv = balance_df["notes_receiv"]    # 应收票据
        notes_payable = balance_df["notes_payable"]    # 应付票据
        accounts_receiv = balance_df["accounts_receiv"]    # 应收账款
        lt_rec = balance_df["lt_rec"]    # 长期应收款
        oth_receiv = balance_df["oth_receiv"]    # 其他应收款
        prepayment = balance_df["prepayment"]    # 预付款项
        inventories = balance_df["inventories"]    # 存货
        fix_assets = balance_df["fix_assets"]    # 	固定资产
        goodwill = balance_df["goodwill"]    # 		商誉
        lt_borr = balance_df["lt_borr"]    # 	长期借款
        st_borr = balance_df["st_borr"]    # 	短期借款
        working_capital = self.strategy.working_Capital(balance_df)    # 营运资金
        # total_assets = balance_df["total_assets"]    # 	资产总计
        int_payable = balance_df["int_payable"]    # 应付利息
        total_liab_hldr_eqy = balance_df["total_liab_hldr_eqy"]    # 负债及股东权益总计
        total_hldr_eqy_inc_min_int = balance_df["total_hldr_eqy_inc_min_int"]    # 股东权益合计(含少数股东权益)
        cur_rate = self.strategy.cur_Rate(balance_df)    # 流动比率
        debt_to_equalty_rate = self.strategy.debt_To_Equalty_Ratio(balance_df)    # 杠杆比率
        lia_assets_rate = self.strategy.lia_Assets_Rate(balance_df)    # 资产负债率
        quick_ratio = self.strategy.quick_Ratio(balance_df)    # 速动比率
        interest = int_payable/(lt_borr + notes_payable)   # 利率

        dd = {"working_capital":working_capital, "notes_receiv": notes_receiv, "accounts_receiv": accounts_receiv,"lt_rec": lt_rec, "oth_receiv": oth_receiv,
         "prepayment": prepayment, "inventories": inventories,"fix_assets": fix_assets, "goodwill": goodwill, "lt_borr": lt_borr,
              "st_borr": st_borr, "int_payable": int_payable, "total_liab_hldr_eqy": total_liab_hldr_eqy,"total_hldr_eqy_inc_min_int":total_hldr_eqy_inc_min_int,
              "cur_rate": cur_rate, "debt_to_equalty_rate": debt_to_equalty_rate, "lia_assets_rate": lia_assets_rate, "quick_ratio": quick_ratio, "interest":interest}
        data = pd.DataFrame(dd)
        return data

    def singleStockCashflowFocus(self, cashflow_df):
        """
        :param cashflow:
        :return:
        """
        n_cashflow_act = cashflow_df["n_cashflow_act"]    # 自由现金流比率，比值越高，说明企业财务实力越雄厚，投资质量越高
        free_cashflow = cashflow_df["free_cashflow"]    # 企业自动有现金流
        c_pay_dist_dpcp_int_exp = cashflow_df["c_pay_dist_dpcp_int_exp"]    # 分配股利、利润或偿付利息支付的现金

        dd = {"n_cashflow_act": n_cashflow_act, "free_cashflow": free_cashflow,"c_pay_dist_dpcp_int_exp": c_pay_dist_dpcp_int_exp}
        data = pd.DataFrame(dd)
        return data

    def singleStockFocus(self, income_df, balance_df, cashflow_df):
        ROA = self.strategy.ROA(income_df, balance_df)   # 净资产收益率
        fix_assets_rate = self.strategy.fix_Assets_Rate(income_df, balance_df)   # 固定资产占比
        turnover = self.strategy.turnOver(income_df, balance_df)   # 存货周转率
        account_recive_rate = self.strategy.accounts_Receiv_Rate(income_df, balance_df)   # 应收账款周转率
        total_assets_turnover = self.strategy.total_Assets_Turnover(income_df, balance_df)   # 总资产周转率
        inventory_revenue_turnover = self.strategy.inventory_Revenue_Ratio(income_df, balance_df)   # 总资产周转率

        dd = {"ROA": ROA, "fix_assets_rate": fix_assets_rate,"turnover": turnover, "account_recive_rate":account_recive_rate,
             "total_assets_turnover":total_assets_turnover, "inventory_revenue_turnover":inventory_revenue_turnover }
        data = pd.DataFrame(dd)
        return data

    def historyOfPriceVSCompositeIndex(self, code):
        """
        历年股价涨跌幅与指数涨跌幅，股票超额收益
        :param code:
        :return:
        """
        daily = DailyToExcel()
        daily_df = daily.daily_readToDf(code)

        last = daily_df.loc[daily_df.groupby(daily_df.index.to_period('Y')).apply(lambda x: x.index.max())]
        first = daily_df.loc[daily_df.groupby(daily_df.index.to_period('Y')).apply(lambda x: x.index.min())]
        l = list(last["close"])
        f =  list(first["close"])
        delta  = []
        for i in range(len(l)):
            delta.append(round((l[i]-f[i])/f[i]*100,2))
        print(delta)
        # print(first["close"])
        close_prices = daily_df["close"]
        # 判断指数
        if 'SZ' == code.split(".")[1]:
            index = '399005.SZ'
        else:
            index = '000001.SH'
        composit_index = daily.daily_readToDf(index)
        index_close = composit_index.loc[close_prices.index]

        l_i = index_close.loc[index_close.groupby(index_close.index.to_period('Y')).apply(lambda x: x.index.max())]
        f_i = index_close.loc[index_close.groupby(index_close.index.to_period('Y')).apply(lambda x: x.index.min())]

        li = list(l_i["close"])
        fi =  list(f_i["close"])
        deltai  = []
        for i in range(len(li)):
            deltai.append(round((li[i]-fi[i])/fi[i]*100,2))
        print(deltai)
        # print(first["close"])
        close_prices = daily_df["close"]

        dd = {"close_price": close_prices, "index_close": index_close}
        # data = pd.DataFrame(dd)
        return dd

    def historyOfRevenue(self, income_df, cashflow_df, isshow):
        """
        历年营业收入，经营收到现金和收入增速变动
        :param income_df:
        :return:
        """
        code = self._get_code()
        t_revenue = income_df["total_revenue"]  # 总营收
        c_fr_sale_sg = cashflow_df["c_fr_sale_sg"]  # 经营活动现金流入小计
        increase_of_revenue = (t_revenue - income_df["total_revenue"].shift(1))/income_df["total_revenue"].shift(1) * 100

        m = min(len(income_df.index), len(cashflow_df.index))
        t_revenue = t_revenue.tail(m)
        c_fr_sale_sg = c_fr_sale_sg.tail(m)
        increase_of_revenue = increase_of_revenue.tail(m)

        dd = {"t_revenue": t_revenue, "c_fr_sale_sg": c_fr_sale_sg,"increase_of_revenue": increase_of_revenue}

        labels = income_df.tail(m).index

        bars = {"t_revenue": t_revenue/100000000, "c_fr_sale_sg":c_fr_sale_sg/100000000}
        plots = {"increase_of_revenue": increase_of_revenue}
        DataGraphs.draw_diff(code+"_historyOfRevenue",1, labels, bars, plots,isshow)
        return dd

    def historyOfNetIncome(self, income_df, cashflow_df, isshow=0):
        """
        历年净利润，经营活动产生的现金流量净额，净利润增速变动
        :param income_df:
        :param cashflow_df:
        :return:
        """
        code = self._get_code()
        n_income = income_df["n_income"]  # 净利润
        n_cashflow_act = cashflow_df["n_cashflow_act"]  # 经营活动产生的现金流量净额
        increase_of_netincome = (n_income - income_df["n_income"].shift(1))/income_df["n_income"].shift(1) * 100
        dd = {"n_income": n_income, "n_cashflow_act": n_cashflow_act,"increase_of_netincome": increase_of_netincome}

        m = min(len(income_df.index), len(cashflow_df.index))
        n_income = n_income.tail(m)
        n_cashflow_act = n_cashflow_act.tail(m)
        increase_of_netincome = increase_of_netincome.tail(m)

        dd = {"n_income": n_income, "n_cashflow_act": n_cashflow_act,"increase_of_netincome": increase_of_netincome}

        labels = income_df.tail(m).index
        bars = {"n_income": n_income/100000000, "n_cashflow_act":n_cashflow_act/100000000}
        plots = {"increase_of_netincome": increase_of_netincome}
        DataGraphs.draw_diff(code+"_historyOfNetIncome",1, labels, bars, plots, isshow=isshow)
        return dd

    def historyOfProfitBeforeTax(self,income_df, isshow=0):
        """
        历年税前利润构成
        经营利润，投资收益，资产减值损失，营业外收支，其他收益
        :return:
        """
        continued_net_profit = income_df["continued_net_profit"]  # 经营利润
        assets_impair_loss = income_df["assets_impair_loss"]  # 资产减值损失
        non_oper_act = income_df["non_oper_income"] - income_df["non_oper_exp"]  # 营业外收支
        oth_income = income_df["oth_income"]  # 其他收益
        invest_income = income_df["invest_income"]   # 投资收益

        dd = {"continued_net_profit": continued_net_profit, "invest_income": invest_income,"assets_impair_loss": assets_impair_loss,
              "non_oper_act": non_oper_act, "oth_income": oth_income}
        # data = pd.DataFrame(dd)
        labels = income_df.index
        for k,v in dd.items():
            dd[k] = v/100000000
        bars = dd
        code = self._get_code()
        DataGraphs.draw_diff(code+"_historyOfProfitBeforeTax",1, labels, bars, isshow=isshow)
        return dd

    def interestOfFees(self, income_df):
        """
        历年费率变动
        :param income_df:
        :return:
        """
        gross_profit_rate = self.strategy.gross_Profit_Rate(income_df)   # 毛利率
        net_income_rate = self.strategy.net_Income_Rate(income_df)   # 净利率
        biz_tax_rate = income_df["biz_tax_surchg"]/income_df["total_revenue"]   # 税金及附加率
        sell_exp_rate = income_df["sell_exp"]/income_df["total_revenue"]   # 销售费用率
        admin_exp_rate = income_df["admin_exp"]/income_df["total_revenue"]   # 管理费用率
        fin_exp_rate = income_df["fin_exp"]/income_df["total_revenue"]   # 财务费用率
        rd_exp_rate = income_df["rd_exp"]/income_df["total_revenue"]   # 研发费用率

        dd = {"gross_profit_rate": gross_profit_rate, "net_income_rate": net_income_rate,"biz_tax_rate": biz_tax_rate,
              "sell_exp_rate": sell_exp_rate, "admin_exp_rate": admin_exp_rate,"fin_exp_rate":fin_exp_rate,"rd_exp_rate":rd_exp_rate}
        # data = pd.DataFrame(dd)
        labels = income_df.index
        # for k,v in dd.items():
        #     dd[k] = v/100000000
        bars = dd
        code = self._get_code()
        DataGraphs.draw_diff(code+"_interestOfFees",1, labels, plots=bars)
        return dd

    def assetChange(self, balance_df, isshow):
        """
        各类资产变动
        :param balance_df:
        :return:
        """
        fix_assets_cip = balance_df["fix_assets"]+balance_df["cip"]   # 固定资产+在建工程
        lt_eqt_invest = balance_df["lt_eqt_invest"]   # 长期股权投资
        invisibel_assets = balance_df["intan_assets"]+ balance_df["goodwill"]  # 商誉+无形资产
        # 应收类资产：应收票据及账款 应收款项融资 其他应收款项
        receiv_assets =balance_df["receiv_financing"] + balance_df["notes_receiv"]+balance_df["accounts_receiv"]+ balance_df["oth_receiv"]
        inventory = balance_df["inventories"]
        # 预付类资产
        prepayment = balance_df["prepayment"]
        # 现金类资产
        cash = balance_df["money_cap"] + balance_df["trad_asset"]
        oth_assets = balance_df["oth_assets"] # 其他资产


        dd = {"fix_assets_cip": fix_assets_cip, "lt_eqt_invest": lt_eqt_invest,"invisibel_assets": invisibel_assets,
              "receiv_assets": receiv_assets, "inventory": inventory,"prepayment":prepayment,"cash":cash, "oth_assets":oth_assets}
        # data = pd.DataFrame(dd)
        labels = balance_df.index
        for k,v in dd.items():
            dd[k] = v/100000000

        code = self._get_code()
        DataGraphs.draw_area(code+"_assetChange",1, labels, dd,isshow)
        return dd

    def liabityChange(self, balance_df, isshow=1):
        """
        负债和股东权益变动
        :param balance_df:
        :return:
        """
        # 有息负债＝短期借款＋一年内到期的长期负债＋长期借款＋应付债券＋长期应付款
        int_liab = balance_df["lt_borr"]+balance_df["st_borr"]+balance_df["non_cur_liab_due_1y"]+balance_df["bond_payable"]+balance_df["long_pay_total"]
        payroll_payable = balance_df["payroll_payable"]  #应付职工薪酬
        adv_receipts = balance_df["adv_receipts"] + balance_df["contract_liab"]# 预收类款项
        total_hldr_eqy_exc_min_int = balance_df["total_hldr_eqy_exc_min_int"] # 股东权益合计(不含少数股东权益)
        pays = balance_df["accounts_pay"]+balance_df["oth_payable"] # 应付类负债
        taxes_payable = balance_df["taxes_payable"].mask(balance_df["taxes_payable"]<0,0) # 应交税费
        # print(taxes_payable)
        oth_liab = balance_df["oth_liab"] # 其他负债
        minority_int = balance_df["minority_int"] # 少数股东权益

        dd = {"int_liab": int_liab, "payroll_payable": payroll_payable,"adv_receipts": adv_receipts,
              "total_hldr_eqy_exc_min_int": total_hldr_eqy_exc_min_int, "pays": pays,"taxes_payable":taxes_payable,
              "oth_liab":oth_liab, "minority_int":minority_int}
        # data = pd.DataFrame(dd)
        labels = balance_df.index
        for k,v in dd.items():
            dd[k] = v/100000000

        code = self._get_code()
        DataGraphs.draw_area(code+"_liabityChange",1, labels, dd,isshow)
        return dd

    def operatingThing(self, income_df, balance_df, isshow=0):
        """
        营运资产 营运负债及营运净资产变动
        :param cashflow_df:
        :return:
        """
        operating_assets = balance_df["total_cur_assets"]-balance_df["total_cur_liab"]
        operating_lia = balance_df["notes_payable"] + balance_df["acct_payable"]+ balance_df["payroll_payable"]+balance_df["taxes_payable"]+ balance_df["acc_exp"] + balance_df["deferred_inc"]+ balance_df["oth_payable"] + balance_df["adv_receipts"] + balance_df["int_payable"]+ balance_df["div_payable"]
        net_working_capital = balance_df["total_cur_assets"]-balance_df["money_cap"]- operating_lia
        operating_rate = net_working_capital/income_df["total_revenue"]


        m = min(len(income_df.index), len(balance_df.index))
        operating_assets = operating_assets.tail(m)
        operating_lia = operating_lia.tail(m)
        net_working_capital = net_working_capital.tail(m)
        operating_rate = operating_rate.tail(m)

        dd = {"operating_assets": operating_assets, "operating_lia": operating_lia,"net_working_capital": net_working_capital}
        pl = {"operating_rate": operating_rate}

        labels = income_df.tail(m).index

        for k,v in dd.items():
            dd[k] = v/100000000

        code = self._get_code()

        DataGraphs.draw_diff(code+"_operatingThing",1, labels, dd, pl,isshow)
        return dd

    def cashflow_Detail(self,cashflow_df, isshow=0):
        """
        现金流量明细，
        :param cashflow_df:
        :return:
        """
        n_cashflow_act = cashflow_df["n_cashflow_act"]   #经营活动产生的现金流量净额
        n_cashflow_inv_act = cashflow_df["n_cashflow_inv_act"]   #	投资活动产生的现金流量净额
        c_recp_cap_contrib = cashflow_df["c_recp_cap_contrib"] - cashflow_df["c_pay_dist_dpcp_int_exp"]   # 发行股份筹资净额
        borrow = cashflow_df["c_recp_borrow"] + cashflow_df["proc_issue_bonds"] - cashflow_df["c_prepay_amt_borr"]  # 有息负债筹资净额
        c_pay_dist_dpcp_int_exp = cashflow_df["c_pay_dist_dpcp_int_exp"]   # 分配股利、利润或偿付利息支付的现金

        dd = {"n_cashflow_act": n_cashflow_act, "n_cashflow_inv_act": n_cashflow_inv_act,"c_recp_cap_contrib": c_recp_cap_contrib,
              "borrow": borrow, "c_pay_dist_dpcp_int_exp":c_pay_dist_dpcp_int_exp}
        # data = pd.DataFrame(dd)
        labels = cashflow_df.index
        for k,v in dd.items():
            dd[k] = v/100000000

        code = self._get_code()

        DataGraphs.draw_diff(code+"_cashflow_Detail",1, labels, dd,isshow=isshow)
        return dd

    def workingCashflow(self, cashflow_df, isshow=0):

        c_inf_fr_operate_a = cashflow_df["c_inf_fr_operate_a"]   #经营活动现金流
        c_pay_acq_const_fiolta = cashflow_df["c_pay_acq_const_fiolta"]   #资本支出
        free_cashflow = cashflow_df["free_cashflow"]  #自由现金流
        dd = {"c_inf_fr_operate_a": c_inf_fr_operate_a, "c_pay_acq_const_fiolta": c_pay_acq_const_fiolta,"free_cashflow": free_cashflow}
        # data = pd.DataFrame(dd)
        labels = cashflow_df.index
        for k,v in dd.items():
            dd[k] = v/100000000

        code = self._get_code()

        DataGraphs.draw_diff(code+"_workingCashflow",1, labels, dd,isshow=isshow)
        return dd

    def rateThing(self,s_date, e_date,income_df,balance_df, isshow=1):

        sb = StockBasic()
        code = self._get_code()
        d_basic = sb.pro.daily_basic(ts_code=code, start_date=s_date, end_date=e_date)
        d_basic["trade_date"] = pd.to_datetime(d_basic["trade_date"].astype('str'))
        d_basic.set_index(d_basic["trade_date"], inplace=True)
        df = d_basic.resample('Y', on='trade_date').mean()
        PB = df["pb"]
        PE = df["pe"]
        ROE = self.strategy.ROE(income_df)
        ROA = self.strategy.ROA(income_df,balance_df)
        # print(dd)
        # data = pd.DataFrame(dd)

        m = min(len(income_df.index), len(PB), len(PE), len(ROE),len(ROA))
        PB = PB.tail(m)
        PE = PE.tail(m)
        ROE = ROE.tail(m)
        ROA = ROA.tail(m)

        dd = {"PE": PE,"PB": PB}
        pl = {"ROE": ROE,"ROA":ROA}
        labels = income_df.tail(m).index

        code = self._get_code()

        DataGraphs.draw_diff(code+"_rateThing",1, labels, dd, pl,isshow=isshow)
        return dd

    def interest_cal(self, balance_df):
        """
        存款利率 %
        :param balance_df:
        :return:
        """
        int_rate = balance_df["int_receiv"]/balance_df["money_cap"] * 100
        return int_rate









