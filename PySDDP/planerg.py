import os
from PySDDP.PowerSystem import importa_pmo

if __name__ == '__main__':
    sistema = importa_pmo(os.path.join(os.getcwd(), 'pmo/'))
