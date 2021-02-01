from typing import List


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        if not lists or len(lists) == 0:
            return None
        tmp_val = []  # 保存所有的链表值
        for i in lists:
            while i:
                tmp_val.append(i.val)  # 取出所有链表的值
                i = i.next
        tmp_val = sorted(tmp_val)  # 排序
        dummy = ListNode(0)
        cur = dummy
        for j in tmp_val:  # 新建链表
            new_node = ListNode(j)
            cur.next = new_node
            cur = cur.next
        return dummy.next


import heapq


class Solution2:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        n = len(lists)
        for i in range(n - 1, -1, -1):  # 首先剔除掉空的链表行
            if not lists[i]:
                lists.pop(i)
                n -= 1
        if not lists:  # 处理完是空就直接返回了
            return None
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>堆>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        pq = [(lists[i].val, i) for i in range(len(lists))]  # 把几个链表头的值和层数放进堆里
        for i in range(n):
            lists[i] = lists[i].next  # 头节点都放进去了，那就指向下一个
        heapq.heapify(pq)  # 用值建立最小堆，存节点不存值建不了最小堆
        res = ListNode(0)  # 存储结果双人组
        cur = res
        while n > 0:
            value, lays = heapq.heappop(pq)  # 取最小的数和他所在的链表层出来
            cur.next = ListNode(value)
            cur = cur.next  # 把这个结果链表加进里面
            if lists[lays]:  # 如果不是最后一个节点还要继续往堆里面放东西
                heapq.heappush(pq, (lists[lays].val, lays))
                lists[lays] = lists[lays].next
            else:
                n -= 1  # 已经有一整层处理完成了
        return res.next
