'''
hash 表，查询为O(1）
python中dict，set使用hash表
'''


class Solution:
    def isAnagram(self, s, t):
        hash = {}
        for i in s:
            if i in hash.keys():
                hash[i] += 1
            else:
                hash[i] = 1
        for j in t:
            if j in hash.keys():
                hash[j] -= 1
        for k in hash.values():
            if k > 0:
                return False
        return True


class Solution2:
    def isAnagram(self, s, t):
        import collections
        return collections.Counter(s) == collections.Counter(t)


if __name__ == '__main__':
    a = Solution()
    print(a.isAnagram('tian', 'b'))
