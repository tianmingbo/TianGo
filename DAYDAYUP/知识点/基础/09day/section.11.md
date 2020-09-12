# 综合应用:射击

#### 小明拿着枪向老王开了2枪

```python

import random

class Person(object):
	def __init__(self, name):
		self.__name = name
		self.__gun = None
		self.__blood = 100

	def __str__(self):
		msg = self.__name + " 的生命值为: " + str(self.__blood)

		if self.__gun:
			msg += " 先拥有一把 " + self.__gun.getName() + "枪"
			clip = self.__gun.getClip()
			if clip:
				msg += " ，枪里有弹夹，弹夹的子弹数为:" + str(clip.getBulletNum())

		return msg

	def zhuangzidan(self, clip, bullet):
		clip.addBullet(bullet)

	def bugGun(self, gun):
		self.__gun = gun

	def zhuangdanjia(self, clip):
		self.__gun.addClip(clip)

	def shoot(self, person):
		shootFlag = random.randint(0,1)
		if shootFlag == 1:
			if self.__gun:
				clip = self.__gun.getClip()
				if clip.getBulletNum()>0:
					person.dropBlood(self.__gun.getLethality())
					clip.removeBullet()

	def dropBlood(self, dropBloodNum):
		self.__blood -= dropBloodNum

class Gun(object):
	def __init__(self, name, lethality):
		self.__name = name
		self.__lethality = lethality
		self.__Clip = None

	def getName(self):
		return self.__name

	def addClip(self, clip):
		self.__Clip = clip

	def getClip(self):
		return self.__Clip

	def getLethality(self):
		return self.__lethality



class Clip(object):
	def __init__(self, name, capacity):
		self.__name = name
		self.__capacity = capacity
		self.__containsBullet = []

	def __str__(self):
		msg = "弹夹 " + self.__name + " 现拥有 " + str(len(self.__containsBullet)) + " 发子弹"
		return msg

	def addBullet(self, bullet):
		if len(self.__containsBullet) < self.__capacity:
			self.__containsBullet.append(bullet)

	def getBulletNum(self):
		return len(self.__containsBullet)


	def removeBullet(self):
		self.__containsBullet.pop()

class Bullet(object):
	def __init__(self, name):
		self.__name = name



b1 = Bullet("子弹1")
clip1 = Clip("弹夹1", 20)
gun1 = Gun("MP5", 30)
xiaoming = Person("小明")
xiaoming.zhuangzidan(clip1, b1)
print(clip1)
b2 = Bullet("子弹2")
xiaoming.zhuangzidan(clip1, b2)
print(clip1)
xiaoming.bugGun(gun1)
print(xiaoming)
xiaoming.zhuangdanjia(clip1)
print(xiaoming)


laowang = Person("老王")
xiaoming.shoot(laowang)
print(laowang)
print(xiaoming)
xiaoming.shoot(laowang)
print(laowang)
print(xiaoming)

```