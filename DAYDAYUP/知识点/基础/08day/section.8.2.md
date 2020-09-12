# 模块安装、使用

## 1.安装的方式

1. 找到模块的压缩包
2. 解压
3. 进入文件夹
4. 执行命令`python setup.py install`

注意：

* 如果在install的时候，执行目录安装，可以使用`python setup.py install --prefix=安装路径`

## 2.模块的引入

在程序中，使用from import 即可完成对安装的模块使用

`from 模块名 import 模块名或者*`