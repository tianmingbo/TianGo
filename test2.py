import datetime

#
# str_p = '2019-01-30 15:29'
# dateTime_p = datetime.datetime.strptime(str_p, '%Y-%m-%d %H:%M')
print(datetime.datetime.now())

# class Solution:
#     def numDecodings(self, s: str) -> int:
#         if len(s) == 0 or s == '0':
#             return 0
#         dp = [0 for _ in range(len(s) + 1)]
#         dp[0] = 1
#         dp[1] = 0 if s[0] == '0' else 1
#         for i in range(2, len(s) + 1):
#             if 0 < int(s[i - 1:i]) <= 9:
#                 dp[i] += dp[i - 1]
#             if 10 <= int(s[i - 2:i]) <= 26:
#                 dp[i] += dp[i - 2]
#         return dp[len(s)]
#
#
# if __name__ == '__main__':
#     a = Solution()
#     print(a.numDecodings('1022'))
status = 1
print(f'multi period switch to multi period ,{status}', 'tactics')
