# Scrapy
### 使用

``` javascript
scrapy startproject news 创建一个项目news
scrapy genspider sina news.sina.com.cn  #spider名称加域名创建一个spider
scrapy crawl quotes #启动爬虫quotes
scrapy crawl quotes -o quotes.jl #输出一行json
```

### 项目结构图

![项目架构图](img.png)

> scrapy.cfg：配置文件，
> items.py：定义了Item数据结构；
> piplines.py：定义了Item Pipeline的实现
> settings.py：项目的全局配置
> middlewares.py：定义了Spider 中间件和下载器中间件；
> spiders：里面包含了一个个Spider的实现，每个Spider对应一个Py文件。

