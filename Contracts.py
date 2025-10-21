# # # # # # # # # # # # # # # # # # # # # # # # #
# 获取指定标的、某个月份的所有ETF期权合约，并保存
# Obtain all ETF option contracts of a specified underlying asset for a certain month,
# then save the contracts.
#
# Created by Jeff, 2025-10-15
# # # # # # # # # # # # # # # # # # # # # # # # #

import akshare as ak
import pandas as pd
from util.util import *



if __name__ == '__main__':

    # 获取正在某个标的正在交易的月份列表，一般为4个月份
    months = ak.option_sse_list_sina('50ETF')
    print('上证50ETF期权正在交易的月份：',months)

    # 获取2025年12月到期的上证50期权行日（同一月份的其它标的行权日都是相同的）
    expire_day = ak.option_sse_expire_day_sina('202512', '50ETF')
    print(f'上证50ETF期权2025年12月合约行权日：{expire_day[0]}， 距到期日：{expire_day[1]}天')


    # 获取2025年12月到期的上证50（510050）所有认购期权合约
    df_contracts = ak.option_sse_codes_sina('看涨期权', '202512', '510050')
    # print(df_contracts)
    # 获取2025年12月到期的上证50（510050）所有认沽期权合约
    df_contracts = ak.option_sse_codes_sina('看跌期权', '202512', '510050')
    # print(df_contracts)

    # 遍历获取每一个期权合约的实时价格、greeks等信息
    for contract_id in df_contracts['期权代码']:
        # 获取单个期权合约的实时价格
        contract_info=ak.option_sse_spot_price_sina(contract_id)
        # print(contract_info)

        # 获取单个期权合约的各希腊字母值（greeks）
        greeks = ak.option_sse_greeks_sina(contract_id)
        # print(greeks)

    # 获取某个标的实时价格
    df_price = ak.option_sse_underlying_spot_price_sina('sh510050')
    df_price.set_index('字段', inplace=True)
    print('上证50实时价格：', float(df_price.loc['最近成交价', '值']))

