# -*- coding: utf-8 -*-
# @Time    : 2020/9/12 11:12
# @Author  : tmb

class Solution:
    def canJump(self, nums) -> bool:
        if len(nums) <= 1:
            return True
        n = len(nums)
        jump_most = 0
        for i in range(n - 1):
            if i <= jump_most:  # 如果当前索引大于能跳得步数，说明过不去,如[1,1,0,3]到索引2的时候，跳不过去
                jump_most = max(jump_most, i + nums[i])
                if jump_most >= n - 1:
                    return True
            else:
                break
        return False


'''
每一步都计算一下从当前位置最远能够跳到哪里，然后和一个全局最优的最远位置farthest做对比，通过每一步的最优解，更新全局最优解，这就是贪心。
'''

if __name__ == '__main__':
    a = Solution()
    print(a.canJump([1, 0, 2, 3]))
