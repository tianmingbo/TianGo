from abc import ABCMeta, abstractmethod


# 抽象类或接口
class FileSystemComponent(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name

    def add(self, component):
        pass

    def remove(self, component):
        pass

    @abstractmethod
    def display(self, depth):
        pass


# 叶子节点类——文件
class File(FileSystemComponent):
    def display(self, depth):
        print("*" * depth + self.name)


# 容器节点类——目录
class Directory(FileSystemComponent):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def display(self, depth):
        print("-" * depth + "+" + self.name)
        for child in self.children:
            child.display(depth + 2)  # depth + 2 输出美化而已


# 客户端代码
if __name__ == '__main__':
    file1 = File("file1.txt")
    file2 = File("file2.txt")

    sub_dir1 = Directory("subdir1")
    sub_dir1.add(file1)

    root_dir = Directory("root")
    root_dir.add(sub_dir1)
    root_dir.add(file2)

    root_dir.display(0)
