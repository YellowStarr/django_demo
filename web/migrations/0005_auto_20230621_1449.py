# Generated by Django 3.2.19 on 2023-06-21 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_delete_pecompare'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='ann_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='balance',
            name='comp_type',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='balance',
            name='end_type',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='报表类型'),
        ),
        migrations.AddField(
            model_name='balance',
            name='f_ann_date',
            field=models.DateField(blank=True, null=True, verbose_name='公告期'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
