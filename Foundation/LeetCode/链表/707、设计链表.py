# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 16:32
# @Author  : tmb
class MyLinkedList:
    node_len = 0

    def __init__(self, val=0, next=None):
        """
        Initialize your data structure here.
        """
        self.val = val
        self.next = next

    def get(self, index: int) -> int:
        """
        Get the value of the index-th node in the linked list. If the index is invalid, return -1.
        """
        if self.node_len == 0 or index > self.node_len - 1:
            return -1



    def addAtHead(self, val: int) -> None:
        """
        Add a node of value val before the first element of the linked list. After the insertion, the new node will be the first node of the linked list.
        """

    def addAtTail(self, val: int) -> None:
        """
        Append a node of value val to the last element of the linked list.
        """

    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted.
        """

    def deleteAtIndex(self, index: int) -> None:
        """
        Delete the index-th node in the linked list, if the index is valid.
        """

# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)
