# Generated by Django 3.2.19 on 2024-02-29 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_alter_stock_daily_trade_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeCompare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_code', models.CharField(max_length=16, verbose_name='代码')),
                ('name', models.CharField(max_length=32, verbose_name='股票名称')),
                ('industry', models.CharField(max_length=32, verbose_name='行业')),
                ('TTM', models.FloatField(verbose_name='PE TTM')),
                ('LYR', models.FloatField(verbose_name='LYR')),
                ('FORWARD', models.FloatField(verbose_name='FORWARD')),
                ('netincome', models.FloatField(verbose_name='净利率')),
                ('gross', models.FloatField(verbose_name='毛利率')),
                ('CGR', models.FloatField(verbose_name='过去五年净利润复合增长率')),
                ('amplitude', models.FloatField(verbose_name='年初至今涨辐')),
            ],
        ),
    ]
