



from scipy.stats import norm
import numpy as np


def __calculate_call(S, K, r, t, sigma):
    """
     S: 标的价格 - Price of underlying asset
     K: 行权价 - Strike price
     r: 无风险利率 - riskless interest rate
     sigma: 隐含波动率 - volatility
     t: 到期时间（年）- period to take

    返回：期权价格 - return: price of option
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)

    # print("norm.cdf(d1):",norm.cdf(d1))
    return S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)

def __calculate_put(S, K, r, t, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    return -S * norm.cdf(-d1) + K * np.exp(-r * t) * norm.cdf(-d2)



def calc_vol(isCall,p, S, K, T, r):
    '''
    二分法计算隐含波动率
    ----------
    p:float,期权市价
    S:float,标的资产价格
    K:float,行权价格
    T:float,剩余期限（折算成年）
    r:float,连续复利无风险利率
    -------
    '''

    # 若时间价值为负，常见于深度实值，直接返回0
    if isCall and (p > 0.2) and (abs(S-K) > p):
    # if (abs(p) > 0.01) and (abs(S-K) > abs(p)):
        return 0.0

    max_vol = 2
    min_vol = 0
    test_value = 0
    test_vol = (max_vol + min_vol) / 2
    n = 0

    if isCall:
        test_value = __calculate_call(S, K, r, T, test_vol)
    else:
        test_value = __calculate_put(S, K, r, T, test_vol)

    while abs(test_value - p) > 0.00001:
        # print(test_vol, abs(test_value - p))

        if test_value - p > 0:
            max_vol = test_vol
            test_vol = (max_vol + min_vol) / 2
        else:
            min_vol = test_vol
            test_vol = (max_vol + min_vol) / 2

        if isCall:
            test_value = __calculate_call( S, K,r, T, test_vol)
        else:
            test_value = __calculate_put(S,K,r,T,test_vol)


        n += 1
        # print("迭代次数：",n, "  Vol：", test_vol," test_value:", test_value)

        if n > 20:
            print("迭代次数超过上限：", n)
            if abs(test_vol) < 0.0001:
                return 0.0
            return test_vol
            # break

    implied_volatility = round(test_vol, 4)
    return implied_volatility
