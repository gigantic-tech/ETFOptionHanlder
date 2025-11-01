# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 演示: 如何实时计算一组期权合约的希腊字母
# 以上证50（510050）期权合约为例
# 代码演示了对跨式（Straddle）、宽跨式（Strangle）、牛市价差（Spread）策略组合的Delta计算（注意：卖出应乘以-1）
# 更多的合约组合和其它希腊字母计算，可采用类似方法
#
# Example: How to calculate the Greeks of option contracts in real time
# The code demonstrates how to calculate Delta of option portfolio for Straddle, Strangle, and Bull Spread (Note: For selling, multiply by -1).
# More contracts and other greeks calculations can be carried out using a similar approach.
#
# Created by Jeff, 2025-11-1
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import akshare as ak
import pandas as pd
import os

# 以上证50（510050）期权合约为例
file_path_call = "SZ50_call.csv"
file_path_put = "SZ50_put.csv"


def _cache_contract(option_type,month_str,file_path):
    type_str = ''
    if option_type == 'call':
        type_str = '看涨期权'
    elif option_type == 'put':
        type_str = '看跌期权'
    else:
        print('参数应该为\'看涨期权\'或\'看跌期权\'')
        return

    df = pd.DataFrame()
    df_contracts = ak.option_sse_codes_sina(type_str, month_str, '510050')
    df['contract_id'] = df_contracts['期权代码']
    prices = []
    for contract_id in df['contract_id']:
        df_price = ak.option_sse_spot_price_sina(contract_id)
        df_price.set_index('字段', inplace=True)
        prices.append(float(df_price.loc['行权价', '值']))

    df['strike_price'] = prices
    df.to_csv(file_path,index=False)

def cache_contracts(file_path_call,file_path_put):

    months = ak.option_sse_list_sina('50ETF') # 其它的在交易的月份是一样的，获取其中一个即可
    assert len(months) > 0, ['月份列表不应为空！']

    # 获取并保存上证50（510050）当月 所有认购期权合约
    _cache_contract('call',months[0],file_path_call)

    # 获取并保存上证50（510050）当月 所有认沽期权合约
    _cache_contract('put',months[0],file_path_put)


# 通过期权类型、行权价获取contract id
def get_contract_id(option_type,strike_price):
    file_path = ''
    if option_type == 'call':
        file_path = file_path_call
    elif option_type == 'put':
        file_path = file_path_put
    else:
        print('参数应该为\'看涨期权\'或\'看跌期权\'')
        return None

    df = pd.read_csv(file_path)
    result = df.query(f'strike_price == {strike_price}')['contract_id'].tolist()
    if len(result) > 0:
        return result[0]

    return None


def greeks_of_contract(option_type,strike_price):
    contract_id = get_contract_id(option_type,strike_price)
    df_greeks = ak.option_sse_greeks_sina(contract_id)
    df_greeks.set_index('字段', inplace=True)

    # 转化为字典，方便后续使用
    greeks = {'Delta': float(df_greeks.loc['Delta', '值']),
              'Gamma': float(df_greeks.loc['Gamma', '值']),
              'Theta': float(df_greeks.loc['Theta', '值']),
              'Vega': float(df_greeks.loc['Vega', '值']),
              'Price': float(df_greeks.loc['最新价', '值'])}

    return greeks


if __name__ == '__main__':

    # 检查是否已存期权合约数据，后续从文件读取即可，提高程序效率
    if os.path.isfile(file_path_call) and os.path.isfile(file_path_put):
        print(f"从缓存期权合约文件 {file_path_call}、{file_path_put} 读取...")
    else:
        cache_contracts(file_path_call,file_path_put)

#--------------------- 在我写这个代码的时侯上证50最新收盘价为3.160 ---------------------
    # 跨式（Straddle）策略组合，计算组合的Delta
    # 例如：买入行权价为3.1的call和put各一张
    greeks1 = greeks_of_contract('call',3.1)
    greeks2 = greeks_of_contract('put',3.1)
    print('行权价为3.1的跨式策略（Straddle）组合Delta为：',greeks1.get('Delta')+greeks2.get('Delta'))

    # 宽跨式（Strangle）策略组合
    # 例如：买入行权价为3.2的call和行权价为3.1的put各一张
    greeks1 = greeks_of_contract('call',3.2)
    greeks2 = greeks_of_contract('put',3.1)
    print('call行权价为3.2、put行权价为3.1的宽跨式策略（Strangle）组合Delta为：',greeks1.get('Delta')+greeks2.get('Delta'))

    # 牛市价差（Spread）策略组合
    # 例如：买入行权价为3.0，卖出行权价为3.2各一张，形成牛市价差策略
    greeks1 = greeks_of_contract('call',3.2)
    greeks2 = greeks_of_contract('put',3.1)
    print('买入行权价为3.0、卖出行权价为3.2的的牛市价差策略（Spread）组合Delta为：',greeks1.get('Delta')-greeks2.get('Delta'))

