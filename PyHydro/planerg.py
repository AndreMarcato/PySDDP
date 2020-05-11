import os
from PyHydro.mddh import mddh

if __name__ == '__main__':
    sistema = mddh(os.path.join(os.getcwd(), 'pmo/'))
