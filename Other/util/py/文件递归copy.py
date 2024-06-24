import os
import random
import shutil


def rec_copy(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    file_name = set()
    if os.path.exists(src):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                src_file = os.path.join(root, file)
                if file in file_name:
                    file = str(random.randint(0, 10000000)) + '_' + file
                    shutil.copy(src_file, os.path.join(root, file))
                    continue
                file_name.add(file)
                shutil.copy(src_file, dst)
                print(src_file, dst)


if __name__ == '__main__':
    print('start copy!')
    source_path = os.path.abspath(r'****')
    target_path = os.path.abspath(r'****')
    rec_copy(source_path, target_path)
    print('copy files finished!')
