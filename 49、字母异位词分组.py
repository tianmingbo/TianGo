'''
hash表
'''


class Solution:
    def groupAnagrams(self, strs):
        if not strs:
            return []
        res = {}
        for i in strs:
            if tuple(sorted(i)) in res.keys():
                res[tuple(sorted(i))].append(i)
            else:
                res[tuple(sorted(i))] = [i]
        return list(res.values())


if __name__ == '__main__':
    a = Solution()
    print(a.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
