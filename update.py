import os
import wget
os.system("kill 1")
try:
    os.remove('main.py')
    os.remove('requirements.txt')
except:pass
wget.download('https://raw.githubusercontent.com/jackychiu0207/hbot/main/main.py',out='main.py')
wget.download('https://raw.githubusercontent.com/jackychiu0207/hbot/main/requirements.txt',out='requirements.txt')
os.system('pip install -r requirements.txt')