# # # # # # # # # # # # # # # # # #
# util functions
# Created by Jeff,2025-10-15
# # # # # # # # # # # # # # # # # #

import matplotlib.pyplot as plt

# 所有ETF期权标的
ALL_UNDERLYINGS = ['510050',
                   '510300',
                   '159919',
                   '510500',
                   '159922',
                   '588000',
                   '588080',
                   '159915',
                   '159901']


def fix_chinese_issue():
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.size'] = '12'
    plt.rcParams['font.sans-serif'] = ['Heiti TC']
    plt.rcParams['axes.unicode_minus'] = False
