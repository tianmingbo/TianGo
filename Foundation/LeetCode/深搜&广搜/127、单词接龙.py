# -*- coding: utf-8 -*-
# @Time    : 2020/9/11 17:14
# @Author  : tmb
# 广度优先
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList) -> int:
        alpha_possible = list(set(''.join(wordList)))  # 所有可能变化的单词
        wordList = set(wordList)  # 集合in操作O(1)
        if endWord not in wordList:
            return 0
        import collections
        queue = collections.deque()
        queue.append((beginWord, 1))
        while queue:
            word, step = queue.popleft()
            if word == endWord:  # 退出条件
                return step
            for i in range(len(word)):
                for j in alpha_possible:
                    tmp = word[:i] + j + word[i + 1:]  # 变化一个新单词，查看是否在Wordlist中，如果在，就入栈
                    if tmp in wordList:
                        wordList.discard(tmp)  # 如果已经变换过，删除。也可以用一个标志
                        queue.append((tmp, step + 1))  # 存在相应变化，步数+1
        return 0


# 双向bfs
class Solution2(object):
    def ladderLength(self, beginWord, endWord, wordList):
        wordList = set(wordList)
        if endWord not in wordList:
            return 0
        front = {beginWord}
        back = {endWord}
        dist = 1  # 走的步数
        word_len = len(beginWord)

        while front:
            dist += 1
            next_front = set()
            for word in front:
                for i in range(word_len):
                    for c in 'abcdefghijklmnopqrstuvwxyz':
                        if c != word[i]:
                            new_word = word[:i] + c + word[i + 1:]
                            if new_word in front:  # 相交了，front和back相交
                                return dist
                            if new_word in wordList:
                                next_front.add(new_word)
                                wordList.remove(new_word)
            front = next_front
            if len(back) < len(front):  # 如果back的长度更小，互换
                back, front = front, back

        return 0


if __name__ == '__main__':
    a = Solution()
    print(a.ladderLength("hit",
                         "cog",
                         ["tot", "dor", "dog", "lot", "log", "cog"]))
