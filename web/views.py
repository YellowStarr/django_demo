from django.shortcuts import render, redirect
import pandas as pd
import json
from web.utils.financeFocus import FinanceFocus

# Create your views here.

from django.shortcuts import HttpResponse
from web import models
import tushare
from web.utils.insertDB import PdToSql
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

_TOKEN = "da4c97957d6f4063991d86f1ccce4c43c6c0275d6b640e706ae9ff9d"

def _pro():
    pro = tushare.pro_api(_TOKEN)
    return pro

def show_pe(request):
    # return HttpResponse("登录页面")
    # stocklist = [{"ts_code": 111, "name":"九阳股份","TTM":24.59, "LYR": 22.53, "FORWARD":24.55, "netincome":5.21, "industry":"小家电",
    #               "CGR": -8.38, "gross": 29.09, "amplitude": -7.02},
    #              {"ts_code": 112, "name":"小熊电器","TTM":28.55, "LYR": 33.03, "FORWARD":19.33, "netincome":9.37, "industry":"小家电",
    #               "CGR": 20.10, "gross": 36.45, "amplitude": 33.94},
    #              {"ts_code": 112, "name":"三花智控","TTM":31.54, "LYR": 33.35, "FORWARD":35.69, "netincome":12.21, "industry":"小家电",
    #               "CGR": 18.76, "gross": 26.08, "amplitude": 14.84},
    #              {"ts_code": 112, "name":"长虹美菱","TTM":20.14, "LYR": 29.83, "FORWARD":14.85, "netincome":1.37, "industry":"小家电",
    #               "CGR": 67.89, "gross": 13.71, "amplitude": 61.83},
    #              {"ts_code": 112, "name":"海信家电","TTM":18.27, "LYR": 22.71, "FORWARD":13.24, "netincome":4.14, "industry":"小家电",
    #               "CGR": 20.69, "gross": 20.69, "amplitude": 63.56}
    #              ]

    pe_queryset = models.PeCompare.objects.all()
    # for obj in pe_queryset:

    return render(request, "show_pe.html", {"stock": pe_queryset})
    # return redirect("www.baidu.com")

def get_daily(request):
    queryset = models.stock_daily.objects.all().order_by("-trade_date")

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
    print(result)
    df = pd.DataFrame(result)
    df["end_date"] = df["end_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["ann_date"] = df["ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["f_ann_date"] = df["f_ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    # df["f_ann_date"] = df["f_ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    data = df.to_dict()
    # js中没有None类型，通过json模块 将None转变为null
    json_data = json.dumps(data)

    '''
    result = list(queryset.values())
    df = pd.DataFrame(result)
    month = df["end_date"]
    print(month)'''
    return render(request, "balance_index.html", {"balance_index": json_data})
    # return render(request, "balance_index.html")

def analyze(request):
    """
     跨表数据分析
    :param request:
    :return:
    """
    ts_code = request.GET.get('code')
    queryset1 = models.Balance.objects.filter(ts_code=ts_code, update_flag='1')
    queryset2 = models.Income.objects.filter(ts_code=ts_code)
    result1 = list(queryset1.values())
    result2 = list(queryset2.values())
    print(result2)

    df = pd.DataFrame(result1)
    df["end_date"] = df["end_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["ann_date"] = df["ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["f_ann_date"] = df["f_ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    data = df.to_dict()
    # js中没有None类型，通过json模块 将None转变为null
    json_data = json.dumps(data)

    df2 = pd.DataFrame(result2)
    print(result2)
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
    df["end_date"] = df["end_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["ann_date"] = df["ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df["f_ann_date"] = df["f_ann_date"].apply(lambda x: x.strftime("%Y-%m-%d"))

    df["n_income"] = df["n_income"]/10000000
    df["total_revenue"] = df["total_revenue"]/10000000
    df["total_cogs"] = df["total_cogs"]/10000000
    df["revenue"] = df["revenue"]/10000000
    gross_profit = df["total_revenue"]-df["total_cogs"]
    total_revenue = df["total_revenue"]
    n_income = df["n_income"]
    df["gross_profit"] = gross_profit

    df["n_rate"] = n_income/total_revenue*100
    df["gross_rate"] = gross_profit/total_revenue*100

    data = df.to_dict()


    # js中没有None类型，通过json模块 将None转变为null
    income_data = json.dumps(data)

    return render(request, "income_t.html", {"income":income_data})
    # return render(request, "balance_index.html")

