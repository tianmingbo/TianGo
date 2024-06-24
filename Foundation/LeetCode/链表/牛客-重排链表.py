# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

#
#
# @param head ListNode类
# @return void
#
'''
找到中间节点，反转后半部分节点，然后合并节点
'''


class Solution:
    def reorderList(self, head):
        # write code here
        if not head:
            return head
        l1 = head
        mid_node = self.find_mid_node(head)  # 找到中间节点
        l2 = mid_node.next
        mid_node.next = None
        l2 = self.reverse(l2)  # 反转后半部分节点

        while l1 and l2:  # 合并节点
            t1 = l1.next
            t2 = l2.next
            l1.next = l2
            l1 = t1
            l2.next = l1
            l2 = t2
        return head

    def find_mid_node(self, head):
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def reverse(self, head):
        p = None
        while head:
            p, head, head.next = head, head.next, p
        return p

class Solution:
    def reorderList(self, head):
        # write code here
        if head == None:
            return None
        l1 = head
        mid_node = self.midnode(head)
        l2 = mid_node.next
        mid_node.next = None
        l2 = self.reverse(l2)

        while l1 and l2:
            t1 = l1.next
            t2 = l2.next
            l1.next = l2
            l1 = t1
            l2.next = l1
            l2 = t2
        return head

    def midnode(self, head):
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def reverse(self, head):
        cur = None
        while head:
            head.next, cur, head = cur, head, head.next
        return cur

