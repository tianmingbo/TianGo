from werkzeug.local import Local
import threading

l = Local()


def add_arg(arg, i):
    l.__setattr__(arg, i)


if __name__ == '__main__':
    print(l.__storage__)
    for i in range(3):
        arg = 'arg' + str(i)
        t = threading.Thread(target=add_arg, args=(arg, i))
        t.start()
    print(l.__storage__)
