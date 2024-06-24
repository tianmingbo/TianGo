# import pywasm
# import requests
# import time
#
# BAE_URL = 'https://spa14.scrape.center'
# TOTAL_PAGE = 10
# runtime = pywasm.load('Wasm.wasm')
# for i in range(TOTAL_PAGE):
#     offset = i * 10
#     # encrypt是函数名称，后面是参数
#     sign = runtime.exec('encrypt', [offset, int(time.time())])
#     url = f'{BAE_URL}/api/movie/?limit=10&offset={offset}&sign={sign}'
#     res = requests.get(url)
#     print(res.json())
#


# wasmer比pywasm功能强大
from wasmer import Module, Store, Instance, engine
from wasmer_compiler_cranelift import Compiler

store = Store(engine.JIT(Compiler))
module = Module(store, open('Wasm.wasm', 'rb').read())
instance = Instance(module)
res = instance.exports.encrypt(1, 2)
print(res)
