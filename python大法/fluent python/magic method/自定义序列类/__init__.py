"""
支持切片操作
"""
import numbers


class Group:
    def __init__(self, group_name, company_name, staffs):
        self.group_name = group_name
        self.company_name = company_name
        self.staffs = staffs

    def __reversed__(self):
        self.staffs.reverse()

    def __getitem__(self, item):
        """
        实现__getitem__，支持切片
        """
        cls = type(self)
        if isinstance(item, slice):
            return cls(group_name=self.group_name, company_name=self.company_name, staffs=self.staffs[item])
        elif isinstance(item, numbers.Integral):
            return cls(group_name=self.group_name, company_name=self.company_name, staffs=[self.staffs[item]])

    def __len__(self):
        return len(self.staffs)

    def __iter__(self):
        return iter(self.staffs)

    def __contains__(self, item):
        if item in self.staffs:
            return True
        else:
            return False


if __name__ == '__main__':
    staffs = ["tian1", "imooc", "tian2", "tian3"]
    group = Group(company_name="imooc", group_name="user", staffs=staffs)
    reversed(group)
    for user in group:
        print(user)
    print(group[:2].staffs)
