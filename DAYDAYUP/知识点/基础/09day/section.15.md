# 练习：设计类

## 1. 设计一个卖车的4S店，该怎样做呢？

```python

# 定义车类
class Car(object):
	# 定义车的方法
	def move(self):
		print("---车在移动---")
	def stop(self):
		print("---停车---")

# 定义一个销售车的店类
class CarStore(object):
	def order(self):
		car = Car() #找一辆车
		return car

# 1. 先的有个销售汽车的店铺
car_store = CarStore()
# 2. 通过这家店铺，订购车
my_car = car_store.order()
# 3. 开车爽。。。
my_car.move()
my_car.stop()

```

### 说明
> 上面的4s店，只能销售一种类型的车
>
> 如果这个是个销售北京现代品牌的车，比如伊兰特、索纳塔等，该怎样做呢？


## 2. 设计一个卖北京现代车的4S店


```python
# 定义伊兰特车类
class YilanteCar(object):
	# 定义车的方法
	def move(self):
		print("---车在移动---")
	def stop(self):
		print("---停车---")

# 定义索纳塔车类
class SuonataCar(object):
	# 定义车的方法
	def move(self):
		print("---车在移动---")
	def stop(self):
		print("---停车---")

# 定义一个销售北京现代车的店类
class CarStore(object):
	def order(self, typeName):
		#根据客户的不同要求，生成不同的类型的车
		if typeName == "伊兰特":
			car = YilanteCar()
		elif typeName == "索纳塔":
			car = SuonataCar()
		return car

xiandai_store = CarStore()
my_car = xiandai_store.order("索纳塔")
my_car.move()
my_car.stop()
```
> 这样做，不太好，因为当北京现代又生产一种新类型的车时，那么又得在CarStore类中修改，有没有好的解决办法呢？