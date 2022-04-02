import os
import wget
try:
    os.remove('main.py')
    os.remove('requirements.txt')
    os.remove('discord_r.txt')
except:pass
wget.download('https://raw.githubusercontent.com/jackychiu0207/hbot/main/main.py',out='main.py')
wget.download('https://raw.githubusercontent.com/jackychiu0207/hbot/main/requirements.txt',out='requirements.txt')
os.system('pip install -r requirements.txt')