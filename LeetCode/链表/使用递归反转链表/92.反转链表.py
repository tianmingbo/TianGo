# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def reverseBetween(self, head: ListNode, m: int, n: int) -> ListNode:
        if not head:
            return
        if m == 1:
            return self.reverseList(head, n)
        else:
            head.next = self.reverseBetween(head.next, m - 1, n - 1)
        return head

    def reverseList(self, head: ListNode, n) -> ListNode:
        if not head:
            return None
        if not n:
            return head
        if n == 1:
            self.next_normal = head.next
            return head
        last = self.reverseList(head.next, n - 1)
        head.next.next = head
        head.next = self.next_normal
        return last


'''
/** 反转区间 [a, b) 的元素，注意是左闭右开 */
ListNode reverse(ListNode a, ListNode b) {
    ListNode pre, cur, nxt;
    pre = null; cur = a; nxt = a;
    // while 终止的条件改一下就行了
    while (cur != b) {
        nxt = cur.next;
        cur.next = pre;
        pre = cur;
        cur = nxt;
    }
    // 返回反转后的头结点
    return pre;
}
'''
