# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        slow, fast = head, head.next
        while fast:
            if slow.val == fast.val:
                fast = fast.next
                slow.next = fast
            else:
                slow, fast = slow.next, fast.next
        return head
