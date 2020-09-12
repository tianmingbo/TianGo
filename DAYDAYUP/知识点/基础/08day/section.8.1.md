# 模块发布


### 模块发布

1.mymodule目录结构体如下：

    .
    ├── setup.py
    ├── suba
    │   ├── aa.py
    │   ├── bb.py
    │   └── __init__.py
    └── subb
        ├── cc.py
        ├── dd.py
        └── __init__.py

2.编辑setup.py文件

py_modules需指明所需包含的py文件

```python
from distutils.core import setup

setup(
name="dongGe", 
version="1.0", 
description="dongGe's module", 
author="dongGe", 
py_modules=['suba.aa', 'suba.bb', 'subb.cc', 'subb.dd']
)
```

3.构建模块

python setup.py build

构建后目录结构

    .
    ├── build
    │   └── lib.linux-i686-2.7
    │       ├── suba
    │       │   ├── aa.py
    │       │   ├── bb.py
    │       │   └── __init__.py
    │       └── subb
    │           ├── cc.py
    │           ├── dd.py
    │           └── __init__.py
    ├── setup.py
    ├── suba
    │   ├── aa.py
    │   ├── bb.py
    │   └── __init__.py
    └── subb
        ├── cc.py
        ├── dd.py
        └── __init__.py


4.生成发布压缩包

python setup.py sdist

打包后,生成最终发布压缩包dongGe-1.0.tar.gz , 目录结构

    .
    ├── build
    │   └── lib.linux-i686-2.7
    │       ├── suba
    │       │   ├── aa.py
    │       │   ├── bb.py
    │       │   └── __init__.py
    │       └── subb
    │           ├── cc.py
    │           ├── dd.py
    │           └── __init__.py
    ├── dist
    │   └── dongGe-1.0.tar.gz
    ├── MANIFEST
    ├── setup.py
    ├── suba
    │   ├── aa.py
    │   ├── bb.py
    │   └── __init__.py
    └── subb
        ├── cc.py
        ├── dd.py
        └── __init__.py

