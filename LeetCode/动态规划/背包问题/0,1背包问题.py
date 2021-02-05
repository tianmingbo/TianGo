# -*- coding: utf-8 -*-
# @Time    : 2020/12/4 14:19
# @Author  : tmb
'''
给你一个可装载重量为W的背包和N个物品，每个物品有重量和价值两个属性。其中第i个物品的重量为wt[i]，价值为val[i]，现在让你用这个背包装物品，最多能装的价值是多少？

举个简单的例子，输入如下：

N = 3, W = 4
wt = [2, 1, 3]
val = [4, 2, 3]
'''

from typing import List


def package(n: int, w: int, wt: List, val: List):
    '''
    :param n: n个物品
    :param w:  背包最多装w
    :param wt:
    :param val:
    :return:
    '''
    # dp[i][w]的定义如下：对于前i个物品，当前背包的容量为w，这种情况下可以装的最大价值是dp[i][w]。
    dp = [[0] * (w + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):  # i是哪个物体
        for j in range(1, w + 1):  # j是容量
            # if i == 0:
            #     dp[0][j] = 0
            # elif j == 0:
            #     dp[i][0] = 0
            # else:
            if j - wt[i - 1] < 0:  # 当前容量不够
                dp[i][j] = dp[i - 1][j]
            else:
                # dp[i - 1][j]，i-1不选
                #dp[i - 1][j - wt[i - 1]] + val[i - 1]  选择i-1，容量减去i-1的重量，并加上i-1的价值
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - wt[i - 1]] + val[i - 1])
    return dp[n][w]


if __name__ == '__main__':
    print(package(n=3, w=4,
                  wt=[2, 1, 3],
                  val=[4, 2, 3]))
