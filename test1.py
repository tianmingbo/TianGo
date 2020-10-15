class DLinkNode(object):
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.pre = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.cache = dict()
        self.head = DLinkNode()
        self.tail = DLinkNode()
        self.head.next = self.tail
        self.tail.pre = self.head
        self.capacity = capacity
        self.size = 0

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self.move_node_2_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key not in self.cache:
            node = DLinkNode(key, value)
            self.cache[key] = node  # 添加进哈希表
            self.addToHead(node)
            self.size += 1
            if self.size > self.capacity:
                # 如果超出容量，删除末尾结点
                remove_node = self.remove_tail()
                self.cache.pop(remove_node.key)
                self.size -= 1
        else:
            # 如果存在，就移到头
            node = self.cache[key]
            node.value = value
            self.move_node_2_head(node)

    def move_node_2_head(self, node):
        self.remove_node(node)
        self.addToHead(node)

    def addToHead(self, node):
        node.next = self.head.next
        node.pre = self.head
        self.head.next.pre = node
        self.head.next = node

    def remove_node(self, node):
        node.pre.next = node.next
        node.next.pre = node.pre

    def remove_tail(self):
        node = self.tail.pre
        self.remove_node(node)
        return node


if __name__ == '__main__':
    a = LRUCache(5)
    a.put(1, 2)
    print(a.get(1))
