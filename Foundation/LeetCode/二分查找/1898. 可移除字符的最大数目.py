from typing import List


class Solution:
    def maximumRemovals(self, s: str, p: str, removable: List[int]) -> int:
        ns, np = len(s), len(p)
        n = len(removable)

        # 辅助函数，用来判断移除 k 个下标后 p 是否是 s_k 的子序列
        def check(k: int) -> bool:
            state = [True] * ns  # s 中每个字符的状态
            for i in range(k):
                state[removable[i]] = False
            # 匹配 s_k 与 p
            j = 0
            for i in range(ns):
                # s[i] 未被删除且与 p[j] 相等时，匹配成功，增加 j
                if state[i] and s[i] == p[j]:
                    j += 1
                    if j == np:
                        return True
            return False

        # 二分查找
        l, r = 0, n + 1
        while l < r:
            mid = l + (r - l) // 2
            if check(mid):
                l = mid + 1
            else:
                r = mid
        return l - 1


if __name__ == '__main__':
    a = Solution()
    print(a.maximumRemovals(s="abcacb", p="ab", removable=[3, 1, 0]))
