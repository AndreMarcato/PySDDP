import os
from PySDDP.mddh import mddh

if __name__ == '__main__':
    sistema = mddh(os.path.join(os.getcwd(), 'pmo/'))
