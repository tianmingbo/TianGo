# 滑动窗口
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        need, window = {}, {}
        for i in s1:
            if i in need:
                need[i] += 1
            else:
                need[i] = 1
        left, right, valid = 0, 0, 0
        while right < len(s2):
            c = s2[right]
            right += 1
            if c in need:
                if c in window:
                    window[c] += 1
                else:
                    window[c] = 1
                if window[c] == need[c]:
                    valid += 1
            while valid == len(need):
                if right - left == len(s1):  # 判断长度
                    return True
                d = s2[left]
                left += 1
                if d in need:
                    if window[d] == need[d]:
                        valid -= 1
                    window[d] -= 1
        return False


if __name__ == '__main__':
    a = Solution()
    print(a.checkInclusion(s1="ab", s2="abdeaooo"))
