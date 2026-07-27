from tools import client

res = client.indices.delete(index="book")
print(res)
