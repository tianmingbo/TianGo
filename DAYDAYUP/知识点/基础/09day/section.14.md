# 工厂模式

# 1. {% em color="#fff700" %}简单工厂模式{% endem %}

## 在上一节中，最后留下的个问题，该怎样解决呢？

### 1.1.使用函数实现

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

# 定义一个函数，来模拟一个汽车厂，目的是创建出具体的汽车对象
def createCar(typeName):
	if typeName == "伊兰特":
		car = YilanteCar()
	elif typeName == "索纳塔":
		car = SuonataCar()
	return car

# 定义一个销售北京现代车的店类
class CarStore(object):
	def order(self, typeName):
		# 让工厂根据类型，生产一辆汽车
		car = createCar(typeName)
		return car

xiandai_store = CarStore()
my_car = xiandai_store.order("索纳塔")
my_car.move()
my_car.stop()
```

### 1.2.使用类来实现

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

# 定义一个生产汽车的工厂，让其根据具体的订单生产车
class CarFactory(object):
	def createCar(self,typeName):
		if typeName == "伊兰特":
			car = YilanteCar()
		elif typeName == "索纳塔":
			car = SuonataCar()
		return car

# 定义一个销售北京现代车的店类
class CarStore(object):
	def __init__(self):
		#设置4s店的指定生产汽车的工厂
		self.carFactory = CarFactory()
	def order(self, typeName):
		# 让工厂根据类型，生产一辆汽车
		car = self.carFactory.createCar(typeName)
		return car

xiandai_store = CarStore()
my_car = xiandai_store.order("索纳塔")
my_car.move()
my_car.stop()
```

> 咋一看来，好像只是把生产环节重新创建了一个类，这确实比较像是一种编程习惯，此种解决方式被称作{% em color="#fff700" %}简单工厂模式{% endem %}
>
> 工厂函数、工厂类对具体的生成环节进行了封装，这样有利于代码的后需扩展，即把功能划分的更具体，4s店只负责销售，汽车厂只负责制造

# 2. {% em color="#fff700" %}工厂方法模式{% endem %}

## 多种品牌的汽车4S店

当买车时，有很多种品牌可以选择，比如北京现代、别克、凯迪拉克、特斯拉等，那么此时程序又该怎样进行设计呢？

```python

# 定义一个基本的4S店类
class CarStore(object):
	#仅仅是定义了这个方法，并没有实现具体功能，这个需要在子类中实现
    def createCar(self, typeName):
        pass

    def xiChe(self):
    	pass
    	# 省略洗车的过程....>> self.car.x()

    def shangBaoXian(self):
    	pass
    	# 省略上保险的过程....>> self.car.xx()

    def shangChePai(self):
    	pass
    	# 省略上车牌的过程....>> self.car.xxx()

    def order(self, typeName):
        # 1. 让工厂根据类型，生产一辆汽车
        self.car = self.createCar(typeName)
        # 2. 洗车
        self.xiChe()
        # 3. 上保险
        self.shangBaoXian()
        # 4. 上车牌
        self.shangChePai()

        # 5. 将车返回给用户
        return self.car

# 定义一个北京现代4S店类
class XiandaiCarStore(CarStore):

	def __init__(self):
		#设置4s店的指定生产汽车的工厂
		self.carFactory = XianDaiFactory()

	# 重写createCar方法，从而完成现代车具体的生成过程，
	# 而其他的像洗车、上牌的功能，都是直接继承自父类，从而让程序更简单了
    def createCar(self, typeName):
        return self.carFactory.createCar(typeName)

# 定义一个生产汽车的工厂，让其根据具体得订单生产车
class XianDaiFactory(object):
    def createCar(self, typeName):
        if typeName == "伊兰特":
            car = YilanteCar()
        elif typeName == "索纳塔":
            car = SuonataCar()
        return car

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



suonata = XiandaiCarStore()
my_car = suonata.order("索纳塔")
my_car.move()
my_car.stop()


```

### 最后来看看`工厂方法模式`的定义

> 定义了一个创建对象的`接口`(可以理解为函数)，但由子类决定要实例化的类是哪一个，{% em color="#fff700" %}工厂方法模式{% endem %}让类的实例化推迟到子类，抽象的CarStore提供了一个创建对象的方法createCar，也叫作`工厂方法`。
>
> 子类真正实现这个createCar方法创建出具体产品。
创建者类不需要直到实际创建的产品是哪一个，选择了使用了哪个子类，自然也就决定了实际创建的产品是什么。
