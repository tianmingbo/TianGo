def slide_window(s: str, t: str):
    need, window = {}, {}
    for i in t:
        if i in need:
            need[i] += 1
        else:
            need[i] = 1
    # valid表示t中所需的字符串，是否在滑动窗口中都拿到了
    left, right, valid = 0, 0, 0
    while right < len(s):
        # c 是将移入窗口的字符
        c = s[right]
        # 右移窗口
        right += 1
        # 进行窗口内数据的一系列更新
        ...
        # 判断左侧窗口是不是收缩
        while valid == len(need):
            # d 是将移出窗口的字符
            d = s[left]
            # 左移窗口
            left += 1
            # 窗口内数据更新
            ...
