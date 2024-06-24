from typing import List

'''
解题思路：实际上就是统计每个字符的个数，是元素个数的整数倍
'''


class Solution:
    def makeEqual(self, words: List[str]) -> bool:
        tmp = {}
        for word in words:
            for j in range(len(word)):
                if word[j] not in tmp:
                    tmp[word[j]] = 1
                else:
                    tmp[word[j]] += 1
        for k, v in tmp.items():
            if v % len(words) != 0:
                return False
        return True


if __name__ == '__main__':
    a = Solution()
    print(a.makeEqual(["abc", "aab", "bc"]))
