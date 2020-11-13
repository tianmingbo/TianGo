# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 20:19
# @Author  : tmb

class Solution:
    def isPalindrome(self, s: str) -> bool:
        if not s:
            return True
        left, right = 0, len(s) - 1
        while left <= right:
            if s[left].isalpha() or s[left].isalnum():
                if s[right].isalpha() or s[right].isalnum():
                    if s[left].lower() == s[right].lower():
                        left += 1
                        right -= 1
                    else:
                        return False
                else:
                    right -= 1
            else:
                left += 1
        return True


if __name__ == '__main__':
    a = Solution()
    print(a.isPalindrome("tianai"))
