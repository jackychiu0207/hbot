import os
import wget
try:os.remove('main.py')
except:pass
wget.download('https://raw.githubusercontent.com/jackychiu0207/hbot/main/main.py',out='main.py')