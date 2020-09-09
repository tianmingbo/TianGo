'''
重点是对临界数值进行求值，如999，得出1000
'''


class Solution:
    def plusOne(self, digits):
        if not digits:
            return
        digits.insert(0, 0)  # 插入一个值，在999时，防止溢出
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                break
            if digits[i] == 9 or digits[i] == 10:
                digits[i] = 0
        if digits[0] == 0:
            digits.pop(0)  # 没用到，就删除
        return digits


if __name__ == '__main__':
    a = Solution()
    print(a.plusOne([1, 9, 9]))
