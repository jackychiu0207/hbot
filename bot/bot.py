
import discord
from discord.ext import commands
from discord.ui import Button,View,Select
from discord import SelectOption
from discord import ButtonStyle
import requests
import json
from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType
import urllib.request
import os
from webserver import keep_alive

intents=discord.Intents.all()


bot = commands.Bot(command_prefix="!",help_command=None,intents=intents)

def getjson(url='https://api.hearthstonejson.com/v1/latest/all/cards.json'):
    req = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    oper = urllib.request.urlopen(req)
    data = oper.read()
    file = open('cards.json','wb')
    file.write(data)
    file.close()

def openjson():
    global cardlib,f
    try:
        with open('cards.json') as f:
            cardlib = json.load(f)
    except:
        return False
getjson()
openjson()

@bot.command()
async def reloadjson(msg,url='https://api.hearthstonejson.com/v1/latest/all/cards.json'):
    try:
        f.close()
        os.remove('cards.json')
    except:
        pass
    getjson(url=url)
    if openjson() is not False:
