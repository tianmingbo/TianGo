# -*- coding: utf-8 -*-
# @Time    : 2020/11/21 18:18
# @Author  : tmb
class CombinationIterator:

    def __init__(self, characters: str, combinationLength: int):
        self.characters = characters
        self.combinationLength = combinationLength
        self.res = []

        def dfs(characters, tmp):
            if len(tmp) == self.combinationLength:
                self.res.append(''.join(tmp[:]))
                return
            for i in range(len(characters)):
                tmp.append(characters[i])
                dfs(characters[i + 1:], tmp)
                tmp.pop()

        dfs(self.characters, [])

    def next(self) -> str:
        if self.res:
            return self.res.pop(0)

    def hasNext(self) -> bool:
        return self.res != []


# Your CombinationIterator object will be instantiated and called as such:
# obj = CombinationIterator(characters, combinationLength)
# param_1 = obj.next()
# param_2 = obj.hasNext()
if __name__ == '__main__':
    a = CombinationIterator('abc', 2)
    print(a.next())
    print(a.next())
    print(a.next())
    print(a.hasNext())
