import os
import shutil
import wget
import svn.remote
try:
    os.remove('main.py')
    os.remove('requirements.txt')
    os.remove('discord_r.txt')
    shutil.rmtree('discord')
except:pass
wget.download('https://raw.githubusercontent.com/jackychiu0207/hbot/main/main.py',out='main.py')
wget.download('https://raw.githubusercontent.com/jackychiu0207/hbot/main/requirements.txt',out='requirements.txt')
wget.download('https://raw.githubusercontent.com/Rapptz/discord.py/master/requirements.txt',out='discord_r.txt')
os.system('pip install -r requirements.txt')
os.system('pip install -r discord_r.txt')
r = svn.remote.RemoteClient('https://github.com/Rapptz/discord.py/trunk/discord')
r.checkout('')