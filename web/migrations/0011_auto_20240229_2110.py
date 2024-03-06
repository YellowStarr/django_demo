# Generated by Django 3.2.19 on 2024-02-29 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_pecompare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pecompare',
            name='ts_code',
            field=models.CharField(db_index=True, max_length=16, verbose_name='代码'),
        ),
        migrations.AlterField(
            model_name='stock_info',
            name='ts_code',
            field=models.CharField(db_index=True, max_length=16, verbose_name='代码'),
        ),
        migrations.AddIndex(
            model_name='balance',
            index=models.Index(fields=['ts_code', 'end_date'], name='web_balance_ts_code_cfcf20_idx'),
        ),
        migrations.AddIndex(
            model_name='cashflow',
            index=models.Index(fields=['ts_code', 'end_date'], name='web_cashflo_ts_code_733c57_idx'),
        ),
        migrations.AddIndex(
            model_name='income',
            index=models.Index(fields=['ts_code', 'end_date'], name='web_income_ts_code_b80d38_idx'),
        ),
    ]