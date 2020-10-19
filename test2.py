def merge_sort(li):
    if len(li) <= 1:  # 递归退出条件
        return li
    mid = len(li) >> 1
    left = merge_sort(li[:mid])
    right = merge_sort(li[mid:])

    def merge(left, right):  # 合并两个有序数组
        res = []
        l, r = 0, 0
        while l < len(left) and r < len(right):
            if left[l] < right[r]:
                res.append(left[l])
                l += 1
            else:
                res.append(right[r])
                r += 1
        res += left[l:]
        res += right[r:]
        return res

    return merge(left, right)


if __name__ == '__main__':
    nums = [89, 3, 3, 2, 5, 45, 33, 67]  # [2, 3, 3, 5, 33, 45, 67, 89]
    c = merge_sort(nums)
    print(c)
