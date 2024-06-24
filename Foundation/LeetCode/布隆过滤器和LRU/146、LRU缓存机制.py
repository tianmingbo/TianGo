class DLinkNode(object):
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.pre = None  # 双向链表
        self.next = None


'''
用hash表记录在不在，用双向链表进行移动到头和删除尾的操作
'''


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity  # cache大小
        self.size = 0  # 记录当前使用了多少
        self.head = DLinkNode()
        self.tail = DLinkNode()
        self.head.next = self.tail  # 创建头尾结点
        self.tail.pre = self.head
        self.cache = dict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]  # 之前已经使用过
        self.move_to_head(node)  # 移到第一位
        return node.value

    def put(self, key: int, value: int) -> None:
        if key not in self.cache:
            # 如果key不在cache中
            node = DLinkNode(key, value)
            self.cache[key] = node
            self.addnode(node)
            self.size += 1
            if self.size > self.capacity:
                # 如果超出容量，删除双向链表的尾部节点
                removed = self.removeTail()
                # 删除哈希表中对应的项
                self.cache.pop(removed.key)
                self.size -= 1
        else:
            node = self.cache[key]  # 已存在，找到当前结点
            node.value = value
            self.move_to_head(node)

    def move_to_head(self, node):  # 移动结点到第一个结点
        self.remove_node(node)
        self.addnode(node)

    def addnode(self, node):  # 在头结点后增加第一个结点，相当于第一个结点
        node.pre = self.head
        node.next = self.head.next
        self.head.next.pre = node
        self.head.next = node

    def remove_node(self, node):  # 删除一个结点
        node.pre.next = node.next
        node.next.pre = node.pre

    def removeTail(self):  # 删除最后一个结点
        node = self.tail.pre
        self.remove_node(node)
        return node


if __name__ == '__main__':
    a = LRUCache(5)
    a.put(1, 2)
    a.put(2, 3)
    a.put(3, 4)
    a.put(4, 6)
    a.put(6, 7)
    a.put(7, 2)
    print(a.get(1))
