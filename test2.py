class Solution:
    def LCS(self, str1, str2):
        m, n = len(str1), len(str2)
        max_len, end = 0, 0
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        for i in range(1, m + 1):  # 遍历每行
            for j in range(1, n + 1):  # 遍历每列
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = 0
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end = j - 1
        if not max_len and not end:
            return -1
        return str2[end - max_len + 1:end + 1]





if __name__ == '__main__':
    a = Solution2()
    print(a.LCS(
        "bbbbbbbbbbbbbbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabba",
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))

'''

class Solution {
public:
    /**
     * longest common substring
     * @param str1 string字符串 the string
     * @param str2 string字符串 the string
     * @return string字符串
     */
    string LCS(string str1, string str2) {
        // write code here
        int m = str1.size();
        int n = str2.size();
        // dp[i][j] str1前i个字符和str2前j个字符（以其为尾字符）的最长公共子串长度
        int dp[m+1][n+1];
        int maxlen = 0, end = 0;
        //base case
        for(int i = 0; i <= m; ++i) dp[i][0] = 0;
        for(int j = 0; j <= n; ++j) dp[0][j] = 0;
        for(int i = 1; i <= m; ++i) {
            for(int j = 1; j <= n; ++j) {
                if(str1[i-1] == str2[j-1]) dp[i][j] = dp[i-1][j-1] + 1;
                else dp[i][j] = 0;
                if(dp[i][j] > maxlen) {
                    maxlen = dp[i][j];
                    end = j - 1;
                }
            }
        }
        string r;
        if(res == 0) return "-1";
        else r = str2.substr(end-maxlen+1, res);
        return r;
    }
};
'''
