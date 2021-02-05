# -*- coding: utf-8 -*-
# @Time    : 2020/9/29 9:45
# @Author  : tmb
class Solution:
    # 遍历words，看是否在board中，回溯
    def findWords(self, board, words):
        if not board or not words:
            return []
        res = []
        for word in words:
            in_words = self.helper(board, word)
            res.append(word) if in_words == True else ...
        return res

    def helper(self, board, target):

        raw, col = len(board), len(board[0])
        self.flag = False

        def dfs(word, i, j, visited, path, length):
            if ''.join(path) != word[:length]:  # 提前终止回溯
                return
            if ''.join(path) == word:
                self.flag = True
                return
            if 0 <= i < raw and 0 <= j < col and board[i][j] == word[length] and (
                    i, j) not in visited and not self.flag:
                visited.add((i, j))
                path.append(board[i][j])
                dfs(word, i - 1, j, visited, path, length + 1)
                dfs(word, i + 1, j, visited, path, length + 1)
                dfs(word, i, j - 1, visited, path, length + 1)
                dfs(word, i, j + 1, visited, path, length + 1)
                visited.discard((i, j))
                path.pop()

        for i in range(raw):
            for j in range(col):
                visited = set()
                if board[i][j] == target[0]:
                    dfs(target, i, j, visited, [], 0)
        return self.flag


from typing import List


class Solution2:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        direct = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        r, c, res = len(board), len(board[0]), []

        root = {}
        for word in words:
            node = root
            for i in word:
                if i not in node:
                    node[i] = {}
                node = node[i]
            node['#'] = word

        def dfs(i, j, node):
            if i < 0 or i >= r or j < 0 or j >= c \
                    or board[i][j] not in node:
                return

            tmp, board[i][j] = board[i][j], '$'
            trie = node[tmp]
            if '#' in trie:
                res.append(trie.pop('#'))

            for x, y in direct:
                nx, ny = x + i, y + j
                dfs(nx, ny, trie)
            board[i][j] = tmp
            if not trie:
                node.pop(tmp)

        for i in range(r):
            for j in range(c):
                dfs(i, j, root)
        return res


if __name__ == '__main__':
    a = Solution()
    print(a.findWords([
        ['o', 'a', 'a', 'n'],
        ['e', 't', 'a', 'e'],
        ['i', 'h', 'k', 'r'],
        ['i', 'f', 'l', 'v']
    ],
        ["oath", "pea", "eat", "rain"]))
