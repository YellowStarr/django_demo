# Generated by Django 3.2.19 on 2024-03-01 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20240301_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='fund_daily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_code', models.CharField(max_length=16, verbose_name='代码')),
                ('trade_date', models.DateField(blank=True, null=True, verbose_name='交易日期')),
                ('open', models.FloatField(blank=True, null=True, verbose_name='当日开盘价')),
                ('close', models.FloatField(blank=True, null=True, verbose_name='当日收盘价')),
                ('high', models.FloatField(blank=True, null=True, verbose_name='当日最高价')),
                ('low', models.FloatField(blank=True, null=True, verbose_name='当日最低价')),
                ('change', models.FloatField(blank=True, null=True, verbose_name='涨跌额')),
                ('pct_chg', models.FloatField(blank=True, null=True, verbose_name='涨跌幅')),
                ('vol', models.FloatField(blank=True, null=True, verbose_name='成交量（手）')),
                ('amount', models.FloatField(blank=True, null=True, verbose_name='成交额（千元）')),
                ('pre_close', models.FloatField(blank=True, null=True, verbose_name='昨收价(前复权)')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.fund_info')),
            ],
        ),
        migrations.AddIndex(
            model_name='fund_daily',
            index=models.Index(fields=['ts_code', 'trade_date'], name='web_fund_da_ts_code_0b53f9_idx'),
        ),
    ]
