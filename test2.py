def test():
    print('111')
    yield 'A'
    print('222')
    yield 'B'


res = (x * 3 for x in test())
# print(res)
for i in res:
    print(i)
