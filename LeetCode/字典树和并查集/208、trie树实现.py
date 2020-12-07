# -*- coding: utf-8 -*-
# @Time    : 2020/9/24 10:24
# @Author  : tmb
class Trie:

    def __init__(self):
        '''
        1.结点本身不存完整单词;
        2.从根结点到某一结点，路径上经过的字符连接起来，为该结点对应的字符串;
        3.每个结点的所有子结点路径代表的字符都不相同。

        '''
        """
        Initialize your data structure here.
        """
        self.trie = {}

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        tree = self.trie
        for a in word:
            # if a not in tree:
            #     tree[a] = {}
            # tree = tree[a]
            # print(self.trie)

            tree = tree.setdefault(a, {})
            print(tree)
        # 单词结束标志
        tree["#"] = "#"

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        tree = self.trie
        for a in word:
            if a not in tree:
                return False
            tree = tree[a]
        if "#" in tree:
            return True
        return False

    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        tree = self.trie
        for a in prefix:
            if a not in tree:
                return False
            tree = tree[a]
        return True


class Trie2:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.trie = {}

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        tmp = self.trie
        for i in word:
            if i not in tmp:
                tmp[i] = {}
            tmp = tmp[i]
        tmp['$'] = '$'

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        tmp = self.trie
        for i in word:
            if i not in tmp:
                return False
            tmp = tmp[i]
        if '$' in tmp:
            return True
        return False

    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        tmp = self.trie
        for i in prefix:
            if i not in tmp:
                return False
            tmp = tmp[i]
        return True


if __name__ == '__main__':
    obj = Trie()
    obj.insert('tian')
    obj.insert('tea')
    print(obj.trie)
    print(obj.search('tian'))
    print(obj.startsWith('ti'))
