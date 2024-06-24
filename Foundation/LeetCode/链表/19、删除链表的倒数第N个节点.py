# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 16:38
# @Author  : tmb
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


'''
快指针先行n个
'''


class Solution:
    def removeNthFromEnd(self, head, n):
        if not head:
            return
        tmp = ListNode(-1)  # 新建一个头结点
        tmp.next = head
        pre = tmp  # 保存待删除结点的前驱结点
        cur = head  # 待删除的结点
        fast = head  # 双指针，为了找到倒数第n个结点
        while n - 1:
            fast = fast.next  # 和cur指针差距n-1，当fast到终点后，正好cur是倒数第n个
            n -= 1
        while fast.next != None:
            pre = pre.next
            cur = cur.next
            fast = fast.next
        pre.next = cur.next  # 删除节点
        return tmp.next


if __name__ == '__main__':
    a = Solution()
    a.removeNthFromEnd()
