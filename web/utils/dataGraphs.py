# -*- coding: utf-8 -*-
'''
@File     : dataGraph.py
@Copyright: Qiuwenjing
@Date     : 2022/7/17
@Desc     : 主要指标图形展示
'''

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

class DataGraphs:
    def __init__(self, _file_path):
        profit_df = pd.read_excel(_file_path, sheet_name='profit', index_col=0)
        cashflow_df = pd.read_excel(_file_path, sheet_name='cashflow', index_col=0)
        debt_df = pd.read_excel(_file_path, sheet_name='debt', index_col=0)

        self.profit_df = profit_df.T
        self.profit_df = self.profit_df.drop('CN')

        self.cashflow_df = cashflow_df.T
        self.cashflow_df = self.cashflow_df.drop('CN')

        self.debt_df = debt_df.T
        self.debt_df = self.debt_df.drop('CN')



    def get_grossProfit(self, report_type='y'):
        grossProfit = self.profit_df['grossProfitMargin']
        print(type(grossProfit))
        if report_type == 'y':
            grossProfit = grossProfit.loc[self._year]
        print(type(grossProfit))
        return grossProfit

    def draw_grossProfit(self, report_type='y'):
        """毛利"""
        grossProfit = self.get_grossProfit(report_type)

        grossProfit.plot()
        plt.show()

    def get_netProfit_Rate(self, report_type='y'):
        netProfit = self.profit_df['netProfitRate']
        if report_type == 'y':
            netProfit = netProfit.loc[self._year]
        return netProfit

    def draw_netProfit_Rate(self, report_type='y'):
        netProfit = self.get_netProfit_Rate(report_type)
        netProfit.plot()
        plt.show()

    def get_roe(self, report_type='y'):
        """净资产收益率ROE=净利润÷净资产（所有权权益|股东权益）x100%.反映企业的股东权益的投资报酬率，是评价股东权益财务状况的重要指标"""
        roe = self.profit_df['weightedRoe']
        if report_type == 'y':
            roe = roe.loc[self._year]
        return roe

    def draw_roe(self, report_type='y'):
        roe = self.get_roe(report_type)
        roe.plot()
        plt.show()

    def get_pe(self, report_type='y'):
        pe = self.profit_df['priceEarningRatio']
        if report_type == 'y':
            pe = pe.loc[self._year]
        return pe

    def draw_pe(self, report_type='y'):
        pe = self.get_pe(report_type)
        pe.plot()
        plt.show()

    def get_pb(self, report_type='y'):
        pb = self.profit_df['priceBookRatio']
        if report_type == 'y':
            pb = pb.loc[self._year]
        return pb

    def draw_pb(self, report_type='y'):
        pb = self.get_pb(report_type)
        pb.plot()
        plt.show()

    def cal_turnover(self, report_type='y'):
        """销售收入÷平均总资产（就是总资产周转率）."""
        # print(self.debt_df['assetSum'])
        assetSum = self.debt_df['assetSum']
        cashReceivedFromSaleOfGoodsAndServices = self.cashflow_df['cashReceivedFromSaleOfGoodsAndServices']
        if report_type == 'y':
            assetSum = assetSum.loc[self._year]
            cashReceivedFromSaleOfGoodsAndServices = cashReceivedFromSaleOfGoodsAndServices.loc[self._year]
        turnover = cashReceivedFromSaleOfGoodsAndServices / assetSum
        return turnover

    def cal_lever(self, report_type='y'):
        """平均总资产÷净资产（就是杠杆系数）."""
        assetSum = self.debt_df['assetSum']
        parentComOwnerTotalEquity = self.debt_df['parentComOwnerTotalEquity']
        if report_type == 'y':
            assetSum = assetSum.loc[self._year]
            parentComOwnerTotalEquity = parentComOwnerTotalEquity.loc[self._year]
        lever = parentComOwnerTotalEquity / assetSum
        return lever

    @staticmethod
    def draw_IN_One(*args):
        num = len(args)
        fig = plt.figure(figsize=(10,9))
        for i in range(num):
            ax = fig.add_subplot(num,1,i+1)
            ax.plot(args[i].index,args[i])
        plt.show()

    @staticmethod
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2, 1.02*height, '%s'%round(height,2), size=10)

    @staticmethod
    def draw_diff(title, save, labels, bars=None, plots=None, isshow=0):
        """
        labels, x年
        """
        fig = plt.figure(figsize=(10,5))
        # 设置图像区域大小，left,bottom,right, height
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        # 显示网格线
        # ax.grid(True)
        ax.set_xlabel("year")
        ax.set_ylabel("billion")
        ax.set_title(title)
        if bars and plots:
            width = 0.2
            n = 0
            x = np.arange(len(labels))
            for k,v in bars.items():
                m = plt.bar(x+n*width, v, width, label=k)
                DataGraphs.autolabel(m)
                n += 1
            plt.xticks(x, labels=labels, rotation=-90)
            plt.legend(loc="upper left")

            ax2 = plt.twinx()
            ax2.set_ylabel("rate(%)")
            # ax2.set_ylim([0, ymax])
            for kp,vp in plots.items():
                 plt.plot(x, vp, label=kp)

            for a,b in zip(x, vp):
                plt.text(a, b+10,round(b,1), verticalalignment='center',color='red')

            plt.legend(loc="upper right")

        elif bars and not plots:
            width = 0.2
            n = 0
            # labels = bars.index
            x = np.arange(len(labels))
            for k,v in bars.items():
                m=plt.bar(x+n*width, v, width, label=k)
                DataGraphs.autolabel(m)
                n += 1
            plt.xticks(x, labels=labels, rotation=-90)
            plt.legend(loc="upper left")

        elif not bars and plots:

            x = np.arange(len(labels))
            for k,v in plots.items():
                plt.plot(x, v, label=k)
            plt.xticks(x, labels=labels, rotation=-90)
            plt.legend(loc="upper left")
        if save:
            path = "E:\\WorkPlace\\stockProject\\img\\"+title+".png"
            plt.savefig(path)
        if isshow:
            plt.show()

    @staticmethod
    def draw_area(title, save, labels, area, isshow=0):
        """
        labels, x年 堆积图
        """
        fig = plt.figure(figsize=(10,5))
        # 设置图像区域大小，left,bottom,right, height
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        # 显示网格线
        # ax.grid(True)
        ax.set_xlabel("year")
        ax.set_ylabel("billion")
        ax.set_title(title)
        area_df = pd.DataFrame(area)
        area_df.plot.area()

        plt.legend(loc="upper left")
        if save:
            path = "E:\\WorkPlace\\stockProject\\img\\"+title+".png"
            plt.savefig(path)
        if isshow:
            plt.show()

if __name__ == "__main__":
    xlt = DataGraphs(".\\finance\\000600.xlsx")
    # xxw = DataGraphs(".\\finance\\新希望.xlsx")
    # xwf = DataGraphs(".\\finance\\600975.xlsx")
    grossProfit = xlt.get_grossProfit()
    netProfit = xlt.get_netProfit_Rate()
    pe = xlt.get_pe()
    lever = xlt.cal_lever()
    xlt.draw_IN_One(grossProfit, netProfit, pe, lever)
    # xxw = xxw.get_roe()
    # xwf = xwf.get_roe()
    # DataGraphs.draw_diff("ROE_3", 1,muyuan=my, xxw=xxw, xwf=xwf)
