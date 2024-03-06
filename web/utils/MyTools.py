#!/user/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : stockProject
@File :MyTools.py
@Author: Azure Qiu
@Date: 2023/4/18 19:59
@Desc:工具类
'''

# from statsmodels.api import OLS
import os, datetime
from chinese_calendar import is_holiday
from web.utils import operExcel
import pandas as pd
from scipy.stats import stats
import openpyxl


class MyTools:
    @property
    def DEFAULT_DATE(self):
        return "2020-01-01"

    @staticmethod
    def pecentPos(df, col1, col2, col3):
        """计算百分位"""
        # PE百分位
        df["median"] = df[col1].median()
        df["20%"] = df[col2].quantile(0.2)
        # 当日pe
        pe = df[col3].iloc[-1]
        percentile = stats.percentileofscore(df[col3], pe)
        df["cur_percent"] = percentile
        return df

    @staticmethod
    def format_time(t):
        """输入的时间格式应该是20200101 或者 2020-01-01"""
        try:
            date = datetime.datetime.strptime(t, "%Y-%m-%d")

            return date
        except ValueError:
            try:
                date = datetime.datetime.strptime(t, "%Y%m%d")
                date = date.strftime("%Y-%m-%d")
                return date
            except ValueError:
                return "Invalid date format"

    @staticmethod
    def str_time(t):
        """把datetime字符串化"""
        try:
            date = t.strftime("%Y%m%d")
            return date
        except ValueError:
            return "Invalid date format"

    @staticmethod
    def get_today():
        day = datetime.date.today()
        delta = datetime.timedelta(days=1)
        while is_holiday(day):
            day = day - delta
        return day

    @staticmethod
    def get_last_trade_day():
        day = datetime.date.today()
        delta = datetime.timedelta(days=1)
        yesterday = day - delta
        while is_holiday(yesterday):
            yesterday = yesterday - delta
        return yesterday

    @staticmethod
    def walk_dirs(root):
        """
        取得指定目录下得文件名列表
        :param root:
        :return:
        """
        file_names = []
        filePath = []
        for roots, dirs, files in os.walk(root, topdown=True):
            file_names = files
        for file in range(len(file_names)):
            filePath.append(roots + file_names[file])
        return file_names, filePath

    @staticmethod
    def writeToExcel(df, filepath, sheetname):
        isExist = os.path.exists(filepath)
        if isExist:
            writer = pd.ExcelWriter(filepath, mode='a', engine='openpyxl', if_sheet_exists='replace')
            # book = load_workbook(writer.path)
            try:
                df.to_excel(writer, sheet_name=sheetname)
                writer.save()
                writer.close()
            except Exception as e:
                print("写入excel出错", e)

        else:
            operExcel.create_excel(filepath)
            df.to_excel(filepath, sheet_name=sheetname)

    @staticmethod
    def del_sheet(filepath, sheetname):
        wb = openpyxl.load_workbook(filepath)
        try:
            ws = wb[sheetname]
            wb.remove(ws)
            wb.save(filepath)
        except:
            print("sheets not exists")

    @staticmethod
    def std_Function(serise):
        """
        标准化函数
        :param serise:
        :return:
        """
        std = serise.std()
        mean = serise.mean()
        z = (serise - mean) / std
        return z

    @staticmethod
    def neutralization(data, factor_value):
        """
        中性化风险因子。市值影子作为重要因子，pe,pb,roe剔除掉市值因子的作用，剩余部分如果表现仍然优秀，该因子才是优秀的因子
        :param data:
        :param factor_value:
        :return:
        """
        # 取风险因子
        # 最小二乘法，对因子值和分线因子做线性规划
