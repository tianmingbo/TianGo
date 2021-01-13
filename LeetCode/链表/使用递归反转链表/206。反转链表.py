# -*- coding: utf-8 -*-
# @Time    : 2020/12/10 14:35
# @Author  : tmb
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


'''
理解：把整个后面的递归当做一个黑盒，整个链表分为两部分，
head 和 head后面的部分。 相信递归，不要去人肉递归
https://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247484467&idx=1&sn=beb3ae89993b812eeaa6bbdeda63c494&chksm=9bd7fa3baca0732dc3f9ae9202ecaf5c925b4048514eeca6ac81bc340930a82fc62bb67681fa&scene=21#wechat_redirect
'''


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head:
            return head
        if head.next is None:
            return head
        last = self.reverseList(head.next)
        head.next.next = head  # 当有两个结点时，就是head.next.next=head   head.next=None
        head.next = None
        return last


'''
// 反转以 a 为头结点的链表 
//迭代
ListNode reverse(ListNode a) {
    ListNode pre, cur, nxt;
    pre = null; cur = a; nxt = a;
    while (cur != null) {
        nxt = cur.next;
        // 逐个结点反转
        cur.next = pre;
        // 更新指针位置
        pre = cur;
        cur = nxt;
    }
    // 返回反转后的头结点
    return pre;
}
'''
