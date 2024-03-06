# Generated by Django 3.2.19 on 2024-03-01 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_auto_20240301_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='index_info',
            name='delist_date',
        ),
        migrations.RemoveField(
            model_name='index_info',
            name='industry',
        ),
        migrations.AddField(
            model_name='index_info',
            name='base_date',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='基期'),
        ),
        migrations.AddField(
            model_name='index_info',
            name='base_point',
            field=models.FloatField(blank=True, null=True, verbose_name='基点'),
        ),
        migrations.AddField(
            model_name='index_info',
            name='category',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='指数类别'),
        ),
        migrations.AddField(
            model_name='index_info',
            name='desc',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='描述'),
        ),
        migrations.AddField(
            model_name='index_info',
            name='exp_date',
            field=models.DateField(blank=True, null=True, verbose_name='终止日期'),
        ),
        migrations.AddField(
            model_name='index_info',
            name='fullname',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='指数全称'),
        ),
        migrations.AddField(
            model_name='index_info',
            name='index_type',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='指数风格'),
        ),
        migrations.AddField(
            model_name='index_info',
            name='publisher',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='发布方'),
        ),
        migrations.AddField(
            model_name='index_info',
            name='weight_rule',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='加权方式'),
        ),
    ]