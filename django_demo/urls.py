"""django_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views



urlpatterns = [
    # path('admin/', admin.site.urls),
    path('show_pe/', views.show_pe),
    path('add/batch/daily/', views.add_batch_daily),
    path('daily/', views.get_daily),
    path('price/<str:ts_code>/', views.get_price),
    path('add/daily/', views.add_daily),
    path('add/history/daily/', views.add_history_daily),
    path('balance/', views.finance_balance_list),
    path('stock_info/', views.stock_info),
    path('index_info/', views.index_Info),
    path('index_daily/<str:ts_code>', views.index_daily),
    path('balance_index/', views.balance_index),
    path('income_t/', views.income_t),
    path('analyze/', views.analyze),

]
