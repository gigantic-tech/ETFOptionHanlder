# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 演示: 如何获取指定标的、月份的所有call/put，计算隐含波动率曲线并且可视化、
# 实时计算分析，隐波可视化
# Example: how to obtain all call/put options for specified underlying asset and month,
# then calculate & plot the implied volatility curve.
#
# Created by Jeff, 2025-10-15
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import akshare as ak
from util.util import *
from util.option_calculation import *
from Contracts import *



def show_vols( underlying_code, type_str, vols, strike_prices):
    # self.reinit(underlying_code) #一定要先调用，这样后面可以代码简洁些



    fix_chinese_issue()
    # plt.xticks(range(0,len(strike_prices),1)) # 显示范围及间隔
    # import pylab as pl
    # plt.xticks(rotation = 30)
    # plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签

    line_colors = ['#0050f0','#20a0e0','#666666','#aaaaaa','#cccccc']
    line_widths = [2.0, 1.6, 1.2 ,0.8, 0.8]
    # if type_str == 'put':
    #     line_color = '#0000ff'
    n = 0
    # while n < len(self.months):
    # 百分比显示，x100 for %
    plt.plot(strike_prices, [x * 100 for x in vols], 'r-', color=line_colors[n], alpha=1.0, linewidth=line_widths[n], label='202510')
    n += 1

    plt.title('实时：'+underlying_code+'隐含波动率'+type_str)

    plt.xticks(strike_prices)

    # plt.legend(self.months, loc='lower right')

    plt.show()


if __name__ == '__main__':

    months = ak.option_sse_list_sina('50ETF') # 其它的在交易的月份是一样的，获取一次即可
    assert len(months) > 0, ['月份列表不应为空！']

    # 获取到期天数、标的价格、无风险利率
    expire_day = ak.option_sse_expire_day_sina(months[0], '50ETF')
    assert len(expire_day) > 0, ['到期日不应为空！']
    time_to_expire = expire_day[1] /365.0 # 到期时间以年为单位

    df_price = ak.option_sse_underlying_spot_price_sina('sh510050')
    df_price.set_index('字段', inplace=True)
    underlying_price = float(df_price.loc['最近成交价', '值']) # 标的价格

    riskless_rate = 0.018 # 无风险利率，可以用10年国债收益率

    vols = [] # 用于保存隐含波动率
    strike_prices = []

    # 获取上证50（510050）当月 所有认购期权合约
    df_contracts = ak.option_sse_codes_sina('看涨期权', months[0], '510050')
    for contract_id in df_contracts['期权代码']:
        df_price = ak.option_sse_spot_price_sina(contract_id)
        df_price.set_index('字段', inplace=True)
        option_name = df_price.loc['期权合约简称', '值']
        option_price = float(df_price.loc['最新价', '值'])
        option_strike = float(df_price.loc['行权价', '值'])
        print(option_name,'实时价格：',option_price )

        vol = calc_vol(True,
                       option_price,
                       underlying_price,
                       option_strike,
                       time_to_expire,
                       riskless_rate)
        vols.append(vol)
        strike_prices.append(option_strike)


    if len(vols) > 0:
        if len(vols) == len(strike_prices):
            show_vols('上证50','str', vols, strike_prices)
