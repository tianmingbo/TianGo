"""
实现租房中介功能,
中介实现了在房东和租客之间的沟通
"""


class House:
    def __init__(self, area, price, owner):
        self.__area = area
        self.__price = price
        self.__owner = owner

    def get_area(self):
        return self.__area

    def get_owner_name(self):
        return self.__owner.get_name()

    def show_info(self):
        print(f'area:{self.__area},price:{self.__price},owner:{self.__owner.get_name()}')


class HouseOwner:
    def __init__(self, name):
        self.__name = name
        self.__house = None

    def get_name(self):
        return self.__name

    def set_house_info(self, area, price):
        self.__house = House(area, price, self)

    def public_house_info(self, meditor):
        meditor.add_house(self.__house)
        print(f'{self.get_name()}在{meditor.get_name()}发布房源')
        self.__house.show_info()


class Meditor:
    def __init__(self, name):
        self.__name = name
        self.__house_infos = []

    def get_name(self):
        return self.__name

    def add_house(self, house):
        self.__house_infos.append(house)

    def remove_house(self, house):
        for info in self.__house_infos:
            if info == house:
                self.__house_infos.remove(info)

    def get_match_house(self, condition):
        return self.__house_infos  # 返回所有

    def sign_contracts(self, period):
        for i in self.__house_infos:
            print(f'{self.get_name()}与{i.get_owner_name()}签订了{period}年的合同，房子在{i.get_area()}')


class Customer:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def find_house(self, desc, meditor):
        print(f'{self.get_name()}想找{desc}的房子')
        return meditor.get_match_house(desc)

    def see_house(self, house_info):
        return house_info[0]

    def sign_contracts(self, house, meditor, period):
        print(f'{self.get_name()}与{meditor.get_name()}签订了{period}年的合同，房子在{house.get_area()}')


if __name__ == '__main__':
    meditor = Meditor('lj')
    zs = HouseOwner('zs')
    zs.set_house_info('bj', 20000)
    zs.public_house_info(meditor)
    meditor.sign_contracts(3)
    tmb = Customer('tmb')
    house_l = tmb.find_house('20ping', meditor)
    like_house = tmb.see_house(house_l)
    tmb.sign_contracts(like_house, meditor, 3)
