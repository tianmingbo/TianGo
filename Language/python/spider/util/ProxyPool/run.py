<<<<<<< HEAD
from proxypool.scheduler import Scheduler
=======
from scheduler import Scheduler
>>>>>>> 3bd9a02e0b0537a70c1b67d45c712c56bdb002f0
import argparse


parser = argparse.ArgumentParser(description='ProxyPool')
parser.add_argument('--processor', type=str, help='processor to run')
args = parser.parse_args()

if __name__ == '__main__':
    # if processor set, just run it
    if args.processor:
        getattr(Scheduler(), f'run_{args.processor}')()
    else:
        Scheduler().run()
