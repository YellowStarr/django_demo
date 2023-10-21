# Generated by Django 3.2.19 on 2023-06-08 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_stock_daily'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_code', models.CharField(max_length=16, verbose_name='代码')),
                ('report_type', models.CharField(max_length=32, verbose_name='报表类型')),
                ('end_date', models.CharField(max_length=32, verbose_name='报告日期')),
                ('cap_rese', models.FloatField(verbose_name='资本公积金')),
                ('undistr_porfit', models.FloatField(verbose_name='未分配利润')),
                ('surplus_rese', models.FloatField(verbose_name='盈余公积金')),
                ('special_rese', models.FloatField(verbose_name='专项储备')),
                ('trad_asset', models.FloatField(verbose_name='交易性金融资产')),
                ('money_cap', models.FloatField(verbose_name='货币资金')),
                ('notes_receiv', models.FloatField(verbose_name='应收票据')),
                ('accounts_receiv', models.FloatField(verbose_name='应收账款')),
                ('oth_receiv', models.FloatField(verbose_name='其他应收款')),
                ('prepayment', models.FloatField(verbose_name='预付款项')),
                ('div_receiv', models.FloatField(verbose_name='应收股利')),
                ('int_receiv', models.FloatField(verbose_name='应收利息')),
                ('inventories', models.FloatField(verbose_name='存货')),
                ('amor_exp', models.FloatField(verbose_name='待摊费用')),
                ('total_share', models.FloatField(verbose_name='总股本')),
                ('nca_within_1y', models.FloatField(verbose_name='一年内到期的非流动资产')),
                ('sett_rsrv', models.FloatField(verbose_name='结算备付金')),
                ('loanto_oth_bank_fi', models.FloatField(verbose_name='拆出资金')),
                ('premium_receiv', models.FloatField(verbose_name='应收保费')),
                ('reinsur_receiv', models.FloatField(verbose_name='应收分保账款')),
                ('reinsur_res_receiv', models.FloatField(verbose_name='应收分保合同准备金')),
                ('pur_resale_fa', models.FloatField(verbose_name='买入返售金融资产')),
                ('oth_cur_assets', models.FloatField(verbose_name='其他流动资产')),
                ('total_cur_assets', models.FloatField(verbose_name='流动资产合计')),
                ('fa_avail_for_sale', models.FloatField(verbose_name='可供出售金融资产')),
                ('htm_invest', models.FloatField(verbose_name='持有至到期投资')),
                ('lt_eqt_invest', models.FloatField(verbose_name='长期股权投资')),
                ('invest_real_estate', models.FloatField(verbose_name='投资性房地产')),
                ('time_deposits', models.FloatField(verbose_name='定期存款')),
                ('oth_assets', models.FloatField(verbose_name='其他资产')),
                ('lt_rec', models.FloatField(verbose_name='长期应收款')),
                ('fix_assets', models.FloatField(verbose_name='固定资产')),
                ('cip', models.FloatField(verbose_name='在建工程')),
                ('const_materials', models.FloatField(verbose_name='工程物资')),
                ('fixed_assets_disp', models.FloatField(verbose_name='固定资产清理')),
                ('produc_bio_assets', models.FloatField(verbose_name='生产性生物资产')),
                ('oil_and_gas_assets', models.FloatField(verbose_name='油气资产')),
                ('intan_assets', models.FloatField(verbose_name='无形资产')),
                ('r_and_d', models.FloatField(verbose_name='研发支出')),
                ('goodwill', models.FloatField(verbose_name='商誉')),
                ('lt_amor_exp', models.FloatField(verbose_name='长期待摊费用')),
                ('defer_tax_assets', models.FloatField(verbose_name='递延所得税资产')),
                ('decr_in_disbur', models.FloatField(verbose_name='发放贷款及垫款')),
                ('oth_nca', models.FloatField(verbose_name='其他非流动资产')),
                ('total_nca', models.FloatField(verbose_name='非流动资产合计')),
                ('cash_reser_cb', models.FloatField(verbose_name='现金及存放中央银行款项')),
                ('depos_in_oth_bfi', models.FloatField(verbose_name='存放同业和其它金融机构款项')),
                ('prec_metals', models.FloatField(verbose_name='贵金属')),
                ('deriv_assets', models.FloatField(verbose_name='衍生金融资产')),
                ('rr_reins_une_prem', models.FloatField(verbose_name='应收分保未到期责任准备金')),
                ('rr_reins_outstd_cla', models.FloatField(verbose_name='应收分保未决赔款准备金')),
                ('rr_reins_lins_liab', models.FloatField(verbose_name='应收分保寿险责任准备金')),
                ('rr_reins_lthins_liab', models.FloatField(verbose_name='应收分保长期健康险责任准备金')),
                ('refund_depos', models.FloatField(verbose_name='存出保证金')),
                ('ph_pledge_loans', models.FloatField(verbose_name='保户质押贷款')),
                ('refund_cap_depos', models.FloatField(verbose_name='存出资本保证金')),
                ('indep_acct_assets', models.FloatField(verbose_name='独立账户资产')),
                ('client_depos', models.FloatField(verbose_name='其中：客户资金存款')),
                ('client_prov', models.FloatField(verbose_name='其中：客户备付金')),
                ('transac_seat_fee', models.FloatField(verbose_name='其中：交易席位费')),
                ('invest_as_receiv', models.FloatField(verbose_name='应收款项类投资')),
                ('total_assets', models.FloatField(verbose_name='资产总计')),
                ('lt_borr', models.FloatField(verbose_name='长期借款')),
                ('st_borr', models.FloatField(verbose_name='短期借款')),
                ('cb_borr', models.FloatField(verbose_name='向中央银行借款')),
                ('depos_ib_deposits', models.FloatField(verbose_name='吸收存款及同业存放')),
                ('loan_oth_bank', models.FloatField(verbose_name='拆入资金')),
                ('trading_fl', models.FloatField(verbose_name='交易性金融负债')),
                ('notes_payable', models.FloatField(verbose_name='应付票据')),
                ('acct_payable', models.FloatField(verbose_name='应付账款')),
                ('adv_receipts', models.FloatField(verbose_name='预收款项')),
                ('sold_for_repur_fa', models.FloatField(verbose_name='卖出回购金融资产款')),
                ('comm_payable', models.FloatField(verbose_name='应付手续费及佣金')),
                ('payroll_payable', models.FloatField(verbose_name='应付职工薪酬')),
                ('taxes_payable', models.FloatField(verbose_name='应交税费')),
                ('int_payable', models.FloatField(verbose_name='应付利息')),
                ('div_payable', models.FloatField(verbose_name='应付股利')),
                ('oth_payable', models.FloatField(verbose_name='其他应付款')),
                ('acc_exp', models.FloatField(verbose_name='预提费用')),
                ('deferred_inc', models.FloatField(verbose_name='递延收益')),
                ('st_bonds_payable', models.FloatField(verbose_name='应付短期债券')),
                ('payable_to_reinsurer', models.FloatField(verbose_name='应付分保账款')),
                ('rsrv_insur_cont', models.FloatField(verbose_name='保险合同准备金')),
                ('acting_trading_sec', models.FloatField(verbose_name='代理买卖证券款')),
                ('acting_uw_sec', models.FloatField(verbose_name='代理承销证券款')),
                ('non_cur_liab_due_1y', models.FloatField(verbose_name='一年内到期的非流动负债')),
                ('oth_cur_liab', models.FloatField(verbose_name='其他流动负债')),
                ('total_cur_liab', models.FloatField(verbose_name='流动负债合计')),
                ('bond_payable', models.FloatField(verbose_name='应付债券')),
                ('lt_payable', models.FloatField(verbose_name='长期应付款')),
                ('specific_payables', models.FloatField(verbose_name='专项应付款')),
                ('estimated_liab', models.FloatField(verbose_name='预计负债')),
                ('defer_tax_liab', models.FloatField(verbose_name='递延所得税负债')),
                ('defer_inc_non_cur_liab', models.FloatField(verbose_name='递延收益-非流动负债')),
                ('oth_ncl', models.FloatField(verbose_name='其他非流动负债')),
                ('total_ncl', models.FloatField(verbose_name='非流动负债合计')),
                ('depos_oth_bfi', models.FloatField(verbose_name='同业和其它金融机构存放款项')),
                ('deriv_liab', models.FloatField(verbose_name='衍生金融负债')),
                ('depos', models.FloatField(verbose_name='吸收存款')),
                ('agency_bus_liab', models.FloatField(verbose_name='代理业务负债')),
                ('oth_liab', models.FloatField(verbose_name='其他负债')),
                ('prem_receiv_adva', models.FloatField(verbose_name='预收保费')),
                ('depos_received', models.FloatField(verbose_name='存入保证金')),
                ('ph_invest', models.FloatField(verbose_name='保户储金及投资款')),
                ('reser_une_prem', models.FloatField(verbose_name='未到期责任准备金')),
                ('reser_outstd_claims', models.FloatField(verbose_name='未决赔款准备金')),
                ('reser_lins_liab', models.FloatField(verbose_name='寿险责任准备金')),
                ('reser_lthins_liab', models.FloatField(verbose_name='长期健康险责任准备金')),
                ('indept_acc_liab', models.FloatField(verbose_name='独立账户负债')),
                ('pledge_borr', models.FloatField(verbose_name='其中:质押借款')),
                ('indem_payable', models.FloatField(verbose_name='应付赔付款')),
                ('policy_div_payable', models.FloatField(verbose_name='应付保单红利')),
                ('total_liab', models.FloatField(verbose_name='负债合计')),
                ('treasury_share', models.FloatField(verbose_name='减:库存股')),
                ('ordin_risk_reser', models.FloatField(verbose_name='一般风险准备')),
                ('forex_differ', models.FloatField(verbose_name='\t外币报表折算差额')),
                ('invest_loss_unconf', models.FloatField(verbose_name='未确认的投资损失')),
                ('minority_int', models.FloatField(verbose_name='少数股东权益')),
                ('total_hldr_eqy_exc_min_int', models.FloatField(verbose_name='股东权益合计(不含少数股东权益)')),
                ('total_hldr_eqy_inc_min_int', models.FloatField(verbose_name='股东权益合计(含少数股东权益)')),
                ('total_liab_hldr_eqy', models.FloatField(verbose_name='负债及股东权益总计')),
                ('lt_payroll_payable', models.FloatField(verbose_name='长期应付职工薪酬')),
                ('oth_comp_income', models.FloatField(verbose_name='其他综合收益')),
                ('oth_eqt_tools', models.FloatField(verbose_name='其他权益工具')),
                ('oth_eqt_tools_p_shr', models.FloatField(verbose_name='其他权益工具(优先股)')),
                ('lending_funds', models.FloatField(verbose_name='融出资金')),
                ('acc_receivable', models.FloatField(verbose_name='应收款项')),
                ('st_fin_payable', models.FloatField(verbose_name='应付短期融资款')),
                ('payables', models.FloatField(verbose_name='应付款项')),
                ('hfs_assets', models.FloatField(verbose_name='持有待售的资产')),
                ('hfs_sales', models.FloatField(verbose_name='持有待售的负债')),
                ('cost_fin_assets', models.FloatField(verbose_name='以摊余成本计量的金融资产')),
                ('fair_value_fin_assets', models.FloatField(verbose_name='以公允价值计量且其变动计入其他综合收益的金融资产')),
                ('cip_total', models.FloatField(verbose_name='在建工程(合计)(元)')),
                ('oth_pay_total', models.FloatField(verbose_name='其他应付款(合计)(元)')),
                ('long_pay_total', models.FloatField(verbose_name='长期应付款(合计)(元)')),
                ('debt_invest', models.FloatField(verbose_name='债权投资(元)')),
                ('oth_debt_invest', models.FloatField(verbose_name='其他债权投资(元)')),
                ('oth_eq_invest', models.FloatField(verbose_name='其他权益工具投资(元)')),
                ('oth_illiq_fin_assets', models.FloatField(verbose_name='其他非流动金融资产(元)')),
                ('oth_eq_ppbond', models.FloatField(verbose_name='其他权益工具:永续债(元)')),
                ('receiv_financing', models.FloatField(verbose_name='应收款项融资')),
                ('use_right_assets', models.FloatField(verbose_name='使用权资产')),
                ('lease_liab', models.FloatField(verbose_name='租赁负债')),
                ('contract_assets', models.FloatField(verbose_name='合同资产')),
                ('contract_liab', models.FloatField(verbose_name='合同负债')),
                ('accounts_receiv_bill', models.FloatField(verbose_name='应收票据及应收账款')),
                ('accounts_pay', models.FloatField(verbose_name='应付票据及应付账款')),
                ('oth_rcv_total', models.FloatField(verbose_name='其他应收款(合计)（元）')),
                ('fix_assets_total', models.FloatField(verbose_name='固定资产(合计)(元)')),
                ('update_flag', models.CharField(max_length=2, verbose_name='更新标识')),
            ],
        ),
    ]