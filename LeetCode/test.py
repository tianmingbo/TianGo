def kuohao(n):
    res = []

    def helper(tmp, left, right):
        if left == n and right == n:
            res.append(tmp)
            return
        if left < n:
            helper(tmp + '(', left + 1, right)
        if right < left:
            helper(tmp + ')', left, right + 1)

    helper('', 0, 0)
    return res


if __name__ == '__main__':
    print(kuohao(3))
