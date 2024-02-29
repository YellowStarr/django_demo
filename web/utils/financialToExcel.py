#!/user/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : stockProject
@File :financialToExcel.py
@Author: Azure Qiu
@Date: 2023/4/19 14:59
@Desc: 将财务报表写入excel，以及读取对应sheet的数据
@ToDo: 每季新增的报表信息应该追加到对应excel。目前每次更新都需要删除全部目录excel
'''
from web.utils.stock_base import StockBasic
from web.utils.MyTools import MyTools
import pandas as pd

class FinancialToExcel(StockBasic):
    def __init__(self):
        super(FinancialToExcel, self).__init__()
        self.root_dir = "E:\\WorkPlace\\stockProject\\finance\\"

    def updateFinacial(self, s_date, e_date):
        # filename_list = MyTools.walk_dirs(self.root_dir)
        # print(type(filename_list))

        all_stocks_df = self.get_stock_code()
        all_stocks_list = all_stocks_df["ts_code"].tolist()

        for code in range(len(all_stocks_list)):
            file_path = self.root_dir + all_stocks_list[code] + ".xlsx"
            print(all_stocks_list[code])
            try:
                income_df = self.pro.income(ts_code=all_stocks_list[code], start_date=s_date, end_date=e_date, report_type=2)
                # print(income_df)
                balance_df = self.pro.balancesheet(ts_code=all_stocks_list[code], start_date=s_date, end_date=e_date)
                cashflow_df = self.pro.cashflow(ts_code=all_stocks_list[code], start_date=s_date, end_date=e_date, report_type=2)
                mainOper_df = self.pro.fina_mainbz(ts_code=all_stocks_list[code], start_date=s_date, end_date=e_date)
                MyTools.writeToExcel(income_df, file_path, sheetname="income")
                MyTools.writeToExcel(balance_df, file_path, sheetname="balance")
                MyTools.writeToExcel(cashflow_df, file_path, sheetname="cashflow")
                MyTools.writeToExcel(mainOper_df, file_path, sheetname="mainOper")
            except Exception as e:
                print(e)

    def finance_Income_readToDf(self, code):
        file_path = self.root_dir + code +  ".xlsx"
        df = pd.read_excel(file_path, sheet_name='income', index_col=0)
        df.drop_duplicates(subset="end_date", inplace=True)
        df["end_date"] = pd.to_datetime(df["end_date"].astype('str'))
        df.set_index(df["end_date"], inplace=True)
        # df.sort_index(ascending=True, inplace=True)
        return df

    def finance_Balance_readToDf(self, code):
        file_path = self.root_dir + code + ".xlsx"
        df = pd.read_excel(file_path, sheet_name='balance', index_col=0)
        # print(pd.to_datetime(df["end_date"].astype('str')))
        # df.drop_duplicates(subset="end_date", inplace=True)
        df["end_date"] = pd.to_datetime(df["end_date"].astype('str'))
        df.set_index(df["end_date"], inplace=True)
        # df.sort_index(ascending=True, inplace=True)
        return df

    def finance_Cashflow_readToDf(self, code):
        file_path = self.root_dir + code +  ".xlsx"
        df = pd.read_excel(file_path, sheet_name='cashflow', index_col=0)
        df.drop_duplicates(subset="end_date", inplace=True)
        df["end_date"] = pd.to_datetime(df["end_date"].astype('str'))
        df.set_index(df["end_date"], inplace=True)
        # df.sort_index(ascending=True, inplace=True)
        return df

    def finance_MainOper_readToDf(self, code):
        file_path = self.root_dir + code +  ".xlsx"
        df = pd.read_excel(file_path, sheet_name='mainoper', index_col=0)
        df["end_date"] = pd.to_datetime(df["end_date"].astype('str'))
        df.set_index(df["end_date"], inplace=True)
        df.sort_index(ascending=True, inplace=True)
        return df

    def add_Finance_Data(self,s_date,e_date):
        # df.to_excel(file_path)

        all_stocks_df = self.get_stock_code()
        all_stocks_list = all_stocks_df["ts_code"].tolist()

        for code in range(len(all_stocks_list)):
            file_path = self.root_dir + all_stocks_list[code] + ".xlsx"
            # print(all_stocks_list[code])
            try:
                income_df = self.pro.income(ts_code=all_stocks_list[code], start_date=s_date, end_date=e_date, report_type=2,fields='oth_income,asset_disp_income')
                # print(income_df)
                balance_df = self.pro.balancesheet(ts_code=all_stocks_list[code], start_date=s_date, end_date=e_date, fields='receiv_financing')
                # cashflow_df = self.pro.cashflow(ts_code=all_stocks_list[code], start_date=s_date, end_date=e_date, report_type=2)
                # mainOper_df = self.pro.fina_mainbz(ts_code=all_stocks_list[code], start_date=s_date, end_date=e_date)
                df2 = pd.read_excel(file_path, sheet_name='balance', index_col=0)
                df1 = pd.read_excel(file_path, sheet_name='income', index_col=0)
                df2 = pd.concat([df2, balance_df], axis=1)
                df1 = pd.concat([df1, income_df], axis=1)

                MyTools.writeToExcel(df1, file_path, sheetname="income")
                MyTools.writeToExcel(df2, file_path, sheetname="balance")
            except Exception as e:
                print(e)



if __name__ == "__main__":
    # root = "E:\\WorkPlace\\stockProject\\finance\\"
    # filePath = MyTools.walk_dirs(root)[1]
    # for path in range(len(filePath)):
    #     MyTools.del_sheet(filePath[path],"balance")
    d = FinancialToExcel()
    # s = d.pro.income(ts_code="002594.SZ", start_date='20080101', end_date="20231231", report_type=2, fields='oth_income,asset_disp_income')
    # s = d.pro.balancesheet(ts_code="002594.SZ", start_date='20080101', end_date="20231231", report_type=1, fields='receiv_financing')
    # filePath = "E:\\WorkPlace\\stockProject\\finance\\002594.SZ.xlsx"
    # MyTools.writeToExcel(s,filePath,"balance")
    # print(s)
    d.add_Finance_Data("20230301", "20231231")





