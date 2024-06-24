<<<<<<< HEAD
from accountpool.storages.redis import RedisClient
=======
from storages.redis import RedisClient
>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
import argparse

parser = argparse.ArgumentParser(description='AccountPool')
parser.add_argument('website', type=str, help='website')
args = parser.parse_args()
website = args.website

conn = RedisClient('account', args.website)
start = 1
end = 100
for i in range(start, end + 1):
    username = password = f'admin{i}'
    conn.set(username, password)
