import os
from PySDDP.sistema import PySDDP

if __name__ == '__main__':
    sistema = PySDDP(os.path.join(os.getcwd(), 'pmo/'))
