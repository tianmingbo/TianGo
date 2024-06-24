class CompressionFacade:
    def __init__(self):
        self.zip = ZIPModel()
        self.rar = RARModel()
        self.z = ZModel()

    def operation1(self, filename: str):
        if filename.endswith('.zip'):
            self.zip.compress(filename)
        elif filename.endswith('.rar'):
            self.rar.compress(filename)
        else:
            self.z.compress(filename)


class ZIPModel:
    def compress(self, path):
        print('zip 压缩')

    def decompress(self, path):
        print('zip 解压缩')


class RARModel:
    def compress(self, path):
        print('rar 压缩')

    def decompress(self, path):
        print('rar 解压缩')


class ZModel:
    def compress(self, path):
        print('7z 压缩')

    def decompress(self, path):
        print('7z 解压缩')


if __name__ == '__main__':
    facade = CompressionFacade()
    facade.operation1('1.zip')
