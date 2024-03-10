# -*- coding: utf-8 -*-
# ---
# @File: preManual
# @Author: QiuWenJing
# @Time: 三月 11, 2024
# @Description: 标准化处理
# ---
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels import regression

class PreManual:
    def filter_extreme_percent(self,series, min=0.025, max=0.975):
        """去极值"""
        series = series.sort_values()
        q = series.quantile([min, max])  # 计算分位数值
        return np.clip(series, q.iloc[0], q.iloc[1])

    def filter_extreme_mad(self,series, n=1.4826):
        median = series.quantile(0.5)
        mad = ((series-median).abs()).quantile(0.5)
        max_range = median + n* mad
        min_range = median - n* mad
        return np.clip(series, min_range, max_range)

    def filter_extreme_3sigma(self,series, n=3):
        mean = series.mean()
        std = series.std()
        max_range = mean + n* std
        min_range = mean - n* std
        return np.clip(series, min_range, max_range)

    def standarize(self,series):
        mean = series.mean()
        std = series.std()
        return (series - mean) / std

    def neutral(self,factor, market_cap):
        # 中性化
        y = factor
        x = market_cap
        result = sm.OLS(y.astype(float), x.astype(float)).fit()
        return result.resid
