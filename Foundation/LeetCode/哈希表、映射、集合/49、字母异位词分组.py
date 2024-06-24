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


class Solution2:
    def groupAnagrams(self, strs):
        import collections
        ans = collections.defaultdict(list)
        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord('a')] += 1
            ans[tuple(count)].append(s)
        return ans.values()


if __name__ == '__main__':
    a = Solution2()
    print(a.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
