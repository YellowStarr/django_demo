from django.shortcuts import render, redirect
import pandas as pd
import json
from web.utils.financeFocus import FinanceFocus

from web import models
from web.utils.myLog import MyLog
import tushare
from web.utils.insertDB import PdToSql
from django.core.paginator import Paginator
from web.utils.stock_base import StockBasic
from web.utils.MyTools import MyTools
import datetime
from web.fanacial.financialIndex import FinancialIndex


_TOKEN = "da4c97957d6f4063991d86f1ccce4c43c6c0275d6b640e706ae9ff9d"

def _pro():
    pro = tushare.pro_api(_TOKEN)
    return pro


def show_pe(request):
    """计算pe等数据"""
    ts_code = request.GET.get('code')
    pe_queryset = models.stock_daily.objects.filter(ts_code=ts_code, trade_date__gt='2014-01-01').order_by('trade_date')
    result = list(pe_queryset.values())
    df = pd.DataFrame(result)
    df = df.sort_values(by="trade_date")
    df = df.drop_duplicates(subset=["trade_date"])
    df = df.reset_index(drop=True)
    df["trade_date"] = df["trade_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    data = df.to_dict()
    json_data = json.dumps(data)
    return render(request, "show_pe.html", {"stock": json_data})

def get_daily(request):
    """需要修改，不需要展示这么多数据，核心在可视化股票数据"""
    today = datetime.date.today()

    print(today)
    queryset = models.stock_daily.objects.filter(trade_date='2024-02-28').order_by("id")
    # s = models.stock_info.objects.filter(ts_code__in=queryset).values('name')
    # print(s)
    # 创建分页器
    paginator = Paginator(queryset, 15)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, "daily.html", {"dailyset": page_obj})

def add_daily(request):
    """
    TODO：检查数据是否重复
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "add_daily.html")
    ts_code = request.POST.get("ts_code")
    trade_date = request.POST.get("trade_date")

    pro = _pro()
    daily_price = pro.daily(ts_code=ts_code, trade_date=trade_date)
    daily_basics = pro.daily_basic(ts_code=ts_code, trade_date=trade_date)
    stock_basics = pro.stock_basic(ts_code=ts_code)
    data = {}
    if not daily_price.empty or not daily_basics.empty:
        data = {"ts_code": daily_price["ts_code"].iloc[0],"trade_date":daily_price["trade_date"].iloc[0], "name": stock_basics["name"].iloc[0],"pre_close":daily_price["pre_close"].iloc[0],
                "open": daily_price["open"].iloc[0],"close": daily_price["close"].iloc[0],"high":daily_price["high"].iloc[0], "low":daily_price["low"].iloc[0],
                "change":daily_price["change"].iloc[0], "pct_chg":daily_price["pct_chg"].iloc[0], "vol":daily_price["vol"].iloc[0], "amount":daily_price["amount"].iloc[0],"turnover_rate": daily_basics["turnover_rate"].iloc[0], "PE_TTM":daily_basics["pe_ttm"].iloc[0], "PB":daily_basics["pb"].iloc[0], "float_share":daily_basics["float_share"].iloc[0],
        "circ_mv":daily_basics["circ_mv"].iloc[0],"total_share":daily_basics["total_share"].iloc[0], "total_mv":daily_basics["total_mv"].iloc[0]
                }

    # print(data)
    # print(stock_basics["name"])
    models.stock_daily.objects.create(**data)

    return redirect("/daily/")

def get_price(request, ts_code):
    """
    :param request:
    :return:
    """
    queryset = models.stock_daily.objects.filter(ts_code=ts_code).order_by("-trade_date")
    # 创建分页器
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "price.html", {"priceset": page_obj})

def add_batch_daily(request):
    """
    批量添加历史每日股票数据
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "add_batch_daily.html")
    # 获取传入的开始和结束日期
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    pro = _pro()
    # 获取筛选后的全部股票代码
    stock_codes = StockBasic().get_stock_code()
    all_stocks_list = stock_codes["ts_code"].tolist()

    for code in range(len(all_stocks_list)):
        ts_code = all_stocks_list[code]
        # 如果没传结束日期，就获取当前日期
        if not end_date:
            end_date = MyTools.get_today()
        # 股票每日价格数据
        code_df = StockBasic().pro_bar(ts_code,s_date=start_date, e_date=end_date)
        print(code_df)
        # 解决 noneType
        try:
            code_df["trade_date"] = pd.to_datetime(code_df["trade_date"])
            code_df["trade_date"] = code_df["trade_date"].apply(lambda x: x.strftime("%Y-%m-%d"))

            # 股票每日基本数据
            daily_basics = pro.daily_basic(ts_code=ts_code,start_date=start_date, end_date=end_date)

            for index, row in code_df.iterrows():
                data = {"ts_code": row["ts_code"],"trade_date":row["trade_date"],"pre_close":row["pre_close"],
                        "open": row["open"],"close": row["close"],"high":row["high"], "low":row["low"],
                        "change":row["change"], "pct_chg":row["pct_chg"], "vol":row["vol"], "amount":row["amount"],"turnover_rate": daily_basics["turnover_rate"].iloc[index], "PE_TTM":daily_basics["pe_ttm"].iloc[index], "PB":daily_basics["pb"].iloc[index], "float_share":daily_basics["float_share"].iloc[index],
                        "circ_mv":daily_basics["circ_mv"].iloc[index],"total_share":daily_basics["total_share"].iloc[index], "total_mv":daily_basics["total_mv"].iloc[index]
                        }

                print(data)
                # models.stock_daily.objects.update_or_create(trade_date=data['trade_date'], ts_code=data['ts_code'],defaults=data)
                models.stock_daily.objects.create(**data)
        except Exception as e:
            print(e)
            continue

    return redirect("/daily/")

def add_history_daily(request):
    """
    TODO：检查数据是否重复
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "add_history_daily.html")

    ts_code = request.POST.get("ts_code")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    pro = _pro()
    daily_price = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    daily_basics = pro.daily_basic(ts_code=ts_code, start_date=start_date,
                                   end_date=end_date, fields=["ts_code","trade_date","turnover_rate","pe_ttm","pb",
                                                              "float_share","circ_mv","total_share","total_mv"])
    # stock_basics = pro.stock_basic(ts_code=ts_code)
    # data = {}
    if not daily_price.empty or not daily_basics.empty:

        ptq = PdToSql()
        s = pd.concat([daily_price,daily_basics], axis=1)
        ptq.pd_to_sql(s, "web_stock_daily")

    return redirect("/daily/")

def finance_balance_list(request):
    """
    资产负债表数据展示。
    TODO：分页展示数据，搜索，字段展示，查看历年负债表
    :param request:
    :return:
    """
    queryset = models.Balance.objects.filter(end_date="2022-12-31", update_flag="1").order_by("id")

    paginator = Paginator(queryset, 15)

    page_number = request.GET.get('page')

    page_obj =  paginator.get_page(page_number)

    return render(request, "balance.html", {"balance": page_obj})

def stock_info(request):
    """
    股票基本信息
    :param request:
    :return:
    """
    queryset = models.stock_info.objects.all().order_by("id")
     # 创建分页器
    paginator = Paginator(queryset, 15)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    # 查询逻辑
    if request.method == 'POST':
        sname = request.POST.get('sname')
        ts_code = request.POST.get('ts_code')
        if sname:
            stock_set = models.stock_info.objects.filter(name=sname)
            return render(request, "stock_info.html", {"stock_set": stock_set})
        elif ts_code:
            stock_set = models.stock_info.objects.filter(ts_code=ts_code)
            return render(request, "stock_info.html", {"stock_set": stock_set})


    return render(request, "stock_info.html", {"stock_set": page_obj})

def balance_index(request):
    """
     资产负债表几个核心数据展示
    :param request:
    :return:
    """
    ts_code = request.GET.get('code')
    queryset = models.Balance.objects.filter(ts_code=ts_code)
    result = list(queryset.values())

    df = pd.DataFrame(result)
    df = df.sort_values(by="end_date", ascending=False)
    df = df.drop_duplicates(subset=["end_date"])
    df = df.reset_index(drop=True)

    df["end_date"] = df["end_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["ann_date"] = df["ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["f_ann_date"] = df["f_ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["fix_assets_total"] = df["fix_assets_total"]/1000000
    df["total_cur_assets"] = df["total_cur_assets"]/1000000
    df["total_assets"] = df["total_assets"]/1000000
    df["money_cap"] = df["money_cap"]/1000000
    df["oth_cur_assets"] = df["oth_cur_assets"]/1000000
    df["prepayment"] = df["prepayment"]/1000000
    df["int_receiv"] = df["int_receiv"]/1000000
    df["inventories"] = df["inventories"]/1000000
    df["total_liab"] = df["total_liab"]/1000000
    df["total_cur_liab"] = df["total_cur_liab"]/1000000
    df["int_payable"] = df["int_payable"]/1000000
    df["notes_receiv"] = df["notes_receiv"]/1000000
    df["accounts_receiv"] = df["accounts_receiv"]/1000000

    data = df.to_dict()
    # js中没有None类型，通过json模块 将None转变为null
    json_data = json.dumps(data)
    return render(request, "balance_index.html", {"balance_index": json_data})

def analyze(request):
    """
     跨表数据分析
    :param request:
    :return:
    """
    ts_code = request.GET.get('code')
    queryset1 = models.Balance.objects.filter(ts_code=ts_code)
    queryset2 = models.Income.objects.filter(ts_code=ts_code)
    result1 = list(queryset1.values())
    result2 = list(queryset2.values())
    # print(result2)

    df = pd.DataFrame(result1)
    df = df.sort_values(by="end_date", ascending=False)
    df = df.drop_duplicates(subset=["end_date"])
    df = df.reset_index(drop=True)
    df["end_date"] = df["end_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["ann_date"] = df["ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["f_ann_date"] = df["f_ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    data = df.to_dict()
    # js中没有None类型，通过json模块 将None转变为null
    json_data = json.dumps(data)

    # 重新按时间排序并去除重复数据
    df2 = pd.DataFrame(result2)
    df2 = df2.sort_values(by="end_date", ascending=False)
    df2 = df2.drop_duplicates(subset=["end_date"])
    df2 = df2.reset_index(drop=True)
    # print(result2)
    df2["end_date"] = df2["end_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df2["ann_date"] = df2["ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df2["f_ann_date"] = df2["f_ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    # df["f_ann_date"] = df["f_ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    data2 = df2.to_dict()
    # js中没有None类型，通过json模块 将None转变为null
    income_data = json.dumps(data2)

    return render(request, "analyze.html", {"balance_index": json_data,"income":income_data})
    # return render(request, "balance_index.html")

def income_t(request):
    """
     利润表图表
    :param request:
    :return:
    """
    ts_code = request.GET.get('code')
    queryset1 = models.Income.objects.filter(ts_code=ts_code)
    result1 = list(queryset1.values())

    df = pd.DataFrame(result1)
    df = df.sort_values(by="end_date", ascending=False)
    df = df.drop_duplicates(subset=["end_date"])
    df = df.reset_index(drop=True)

    try:
        df["end_date"] = df["end_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        df["ann_date"] = df["ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        df["f_ann_date"] = df["f_ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))

        df["n_income"] = df["n_income"] / 10000000
        df["total_revenue"] = df["total_revenue"] / 10000000
        df["total_cogs"] = df["total_cogs"] / 10000000
        df["revenue"] = df["revenue"] / 10000000
        gross_profit = df["total_revenue"]-df["total_cogs"]
        total_revenue = df["total_revenue"]
    except Exception:
        print(df)
        return redirect("/stock_info/")
    n_income = df["n_income"]
    df["gross_profit"] = gross_profit

    df["n_rate"] = n_income/total_revenue*100
    df["gross_rate"] = gross_profit/total_revenue*100

    data = df.to_dict()


    # js中没有None类型，通过json模块 将None转变为null
    income_data = json.dumps(data)

    return render(request, "income_t.html", {"income":income_data})
    # return render(request, "balance_index.html")

def index_Info(request):
    """国内主要指数"""
    queryset = models.index_info.objects.all().order_by("id")
    # 创建分页器
    paginator = Paginator(queryset, 15)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    # 查询逻辑
    if request.method == 'POST':
        sname = request.POST.get('sname')
        ts_code = request.POST.get('ts_code')
        if sname:
            stock_set = models.index_info.objects.filter(name=sname)
            return render(request, "index_info.html", {"index_set": stock_set})
        elif ts_code:
            stock_set = models.index_info.objects.filter(ts_code=ts_code)
            return render(request, "index_info.html", {"index_set": stock_set})

    return render(request, "index_info.html", {"index_set": page_obj})

def index_daily(request, ts_code):
    """指数走势
       页面刷新时，会比较今日数据是否已更新，若未更新，则更新
    """
    MyLog.info("================每日指数走势==============")
    print(MyTools.DEFAULT_DATE)
    if request.method == 'GET':
        query_set = models.index_daily.objects.filter(ts_code=ts_code, trade_date__gt=MyTools().DEFAULT_DATE)
        basic_set = models.index_dailybasic.objects.filter(ts_code=ts_code, trade_date__gt=MyTools().DEFAULT_DATE)
        if len(query_set) == 0:
            # 初始化数据
            MyLog.info("================初始化指数数据：%s=============="%ts_code)
            PdToSql().update_index_daily(ts_code)
            query_set = models.index_daily.objects.filter(ts_code=ts_code)
        if len(basic_set) == 0:
            MyLog.info("================初始化指数每日指标：%s=============="%ts_code)
            PdToSql().update_index_dailybasic(ts_code)
            query_set = models.index_dailybasic.objects.filter(ts_code=ts_code)
    elif request.method == "POST":
        # 查询逻辑
        s_date_str = request.POST.get('start_date')
        e_date_str = request.POST.get('end_date')
        if s_date_str != '' or e_date_str != '':
            s_date = MyTools.format_time(s_date_str)
            e_date = MyTools.format_time(e_date_str)
            query_set = models.index_daily.objects.filter(ts_code=ts_code, trade_date__gte=s_date, trade_date__lte=e_date)
            basic_set = models.index_dailybasic.objects.filter(ts_code=ts_code, trade_date__gte=s_date, trade_date__lte=e_date)
        else:
            query_set = models.index_daily.objects.filter(ts_code=ts_code, trade_date__gt=MyTools().DEFAULT_DATE)
            basic_set = models.index_dailybasic.objects.filter(ts_code=ts_code, trade_date__gt=MyTools().DEFAULT_DATE)
    MyLog.info("================返回指数每日数据：%s=============="%ts_code)
    index_data = _handle_set(query_set, ts_code)
    dailybasic = _index_dailybasic(basic_set, ts_code)
    return render(request,"index_daily.html", {"daily_set": index_data, "dailybasic":dailybasic})

def _index_dailybasic(query_set,ts_code):
    result1 = list(query_set.values())
    df = pd.DataFrame(result1)
    df = df.sort_values(by="trade_date")

    df = df.reset_index(drop=True)
    # PE百分位
    df = MyTools.pecentPos(df, "PE_TTM", "PE_TTM", "PE_TTM")
    try:
        df["trade_date"] = df["trade_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    except Exception:

        return redirect("/index_info/")
    data = df.to_dict()

    # js中没有None类型，通过json模块 将None转变为null
    index_data = json.dumps(data)
    # print(index_data)
    return index_data

def _handle_set(query_set, ts_code):
    result1 = list(query_set.values())

    df = pd.DataFrame(result1)
    df = df.sort_values(by="trade_date")
    df = df.reset_index(drop=True)
    try:
        df["trade_date"] = df["trade_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    except Exception:
        return redirect("/index_info/")
    data = df.to_dict()  # js中没有None类型，通过json模块 将None转变为null
    index_data = json.dumps(data)
    return index_data

