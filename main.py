from pydub import AudioSegment
import discord
from discord import File
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
import wget

intents=discord.Intents.all()


bot = commands.Bot(command_prefix="t!",help_command=None,intents=intents)


classdict={"DEATHKNIGHT":"死亡騎士","DEMONHUNTER":"惡魔獵人","DREAM":"伊瑟拉","DRUID":"德魯伊","HUNTER":"獵人","INVALID":"未知/不適用職業","MAGE":"法師","NEUTRAL":"中立","PALADIN":"聖騎士","PRIEST":"牧師","ROGUE": 7,"SHAMAN":"薩滿","WARLOCK":"術士","WARRIOR":"戰士","WHIZBANG":"威茲幫"}
langlist=["deDE","enUS","esES","esMX","frFR","itIT","jaJP","koKR","plPL","ptBR","ruRU","thTH","zhCN","zhTW"]
def getfile():
    url='https://api.hearthstonejson.com/v1/latest/all/cards.json'
    req = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    oper = urllib.request.urlopen(req)
    data = oper.read()
    file = open('cards.json','wb')
    file.write(data)
    file.close()
    url='https://api.hearthstonejson.com/v1/latest/all/mercenaries.json'
    req = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    oper = urllib.request.urlopen(req)
    data = oper.read()
    file = open('mercenaries.json','wb')
    file.write(data)
    file.close()
    try:
        os.remove('group.json')
        os.remove('audio.json')
    except:pass
    wget.download('https://raw.githubusercontent.com/jackychiu0207/hbot/main/group.json',"group.json")
    wget.download('https://raw.githubusercontent.com/Zero-to-Heroes/hs-reference-data/master/src/cards/cards_zhTW.json',"audio.json")

def openfile():
    global cardlib,cardlibm,group,audiolib
    try:
        cardlib=json.load(open('cards.json'))
        cardlibm=json.load(open('mercenaries.json'))
        group=json.load(open('group.json'))
        audiolib=json.load(open('audio.json'))
    except:
        return False
getfile()
openfile()
try:env=json.load(open('.env'))
except:pass
@bot.command()
async def reload(msg):
    try:
        cardlibm.close()
        cardlib.close()
        group.close()
        audiolib.close()
        os.remove('cards.json')
        os.remove('mercenaries.json')
        os.remove('group.json')
        os.remove('audio.json')
    except:
        pass
    getfile()
    if openfile() is not False:
        await msg.reply("完成")
    else:
        await msg.reply("錯誤")

#help command
@bot.command()
async def help(msg):
    embed = discord.Embed(title="指令列表",description="指令中語言參數皆為選填，常見zhTW(預設)、zhCN、enUS …\n",color=0xff0000)
    embed.add_field(name="t!id",value="※不推薦新手使用該指令\n使用方法:\"t!id dbfId或id 語言(選填)\"\n例子1(使用dbfId):`t!id 38833`\n例子2(使用id):`t!id OG_272`\n\n", inline=False)
    embed.add_field(name="t!card",value="空格請用下滑線\'_\'代替\n使用方法:\"t!card 卡牌名稱 語言(選填)\"\n例子:`t!card 暮光召喚師`", inline=False)
    embed.add_field(name="t!merc",value="空格請用下滑線\'_\'代替\n使用方法:\"t!merc 傭兵、裝備、技能名稱 語言(選填)\"\n例子1(傭兵):`t!merc 餅乾大廚`\n例子2(裝備):`t!merc 養好的鍋子`\n例子3(技能):`t!merc 魚肉大餐`", inline=False)
    embed.add_field(name="t!bg",value="空格請用下滑線\'_\'代替\n使用方法:\"t!bg 戰場卡牌 語言(選填)\"\n例子:`t!bg 餅乾大廚`", inline=False)
    embed.add_field(name="t!deck",value="使用方法:\"t!deck 牌組代碼 牌組名稱(選填) 語言(選填)\"\n例子1(無套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA`\n例子2(有套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA 無限潛行`", inline=False)
    embed.add_field(name="t!reload",value="直接輸入，機器人會更新資料庫。當找不到覺得存在的卡牌時，可以使用此指令。", inline=False)
    embed.add_field(name="t!stop",value="直接輸入，機器人會直接停止。只有在緊急狀況才可使用，勿隨意使用", inline=False)
    await msg.reply(embed=embed)


#def
def get_token():
    BZTOKEN = env['BZTOKEN']
    BZSECRET = env['BZSECRET']
    data = {'grant_type':'client_credentials'}
    response = requests.post('https://apac.battle.net/oauth/token', data=data, auth=(BZTOKEN, BZSECRET))
    token=json.loads(response.text)['access_token']
    return token

def change_text(text:str):
    tlist=[['\n',''],['<b>','**'],['</b>','**'],['<i>','*'],['</i>','*'],["。","。\n"],['****',""],['[x]','']]
    for txt in tlist:
        if txt[0] in text:text=text.replace(txt[0],txt[1])
    return text





#stop
@bot.command()
async def stop(msg):
    await msg.reply("stop!")
    exit()
#event
@bot.event
async def on_ready():
    print('BOT IS ONLINE!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("召喚惡魔!"))
    
@bot.event
async def on_command_error(ctx,error):
    await ctx.message.reply("錯誤:\n`"+str(error)+"`\n請檢查指令是否輸入錯誤！")

async def get_audio(interaction):
    await interaction.response.defer()
    audioname=audiolib[int(dict(interaction.data)['values'][0].split(",")[0])]["audio"][dict(interaction.data)['values'][0].split(",")[1]]
    if len(audioname)==1:
        try:
            await interaction.followup.send(file=File("audiofile/"+audioname[0].split(".")[0]+".wav"))
        except:
            await interaction.followup.send("尚無該語音檔案")
    else:
        out=AudioSegment.empty().silent(duration=100000)
        def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
            trim_ms = 0
            assert chunk_size > 0
            while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
                trim_ms += chunk_size
            return trim_ms
        try:
            for name in audioname:
                out=out.overlay(AudioSegment.from_wav("audiofile/"+name.split(".")[0]+".wav"))
            start_trim = detect_leading_silence(out)
            end_trim = detect_leading_silence(out.reverse())
            duration = len(out)    
            out = out[start_trim:duration-end_trim]
            out.export(audioname[0].split(".")[0]+".wav",format="wav")
            await interaction.followup.send(file=File(audioname[0].split(".")[0]+".wav"))
            os.remove(audioname[0].split(".")[0]+".wav")
        except:await interaction.followup.send("尚無該語音檔案")

async def audiobtn_callback(interaction:discord.Interaction):
    await interaction.response.defer()
    view=View()
    options=[]
    for i,data in enumerate(audiolib):
        if data["dbfId"]==int(dict(interaction.data)['custom_id']):
            if "audio" in data:
                if len(data["audio"])==0:await interaction.followup.send("抱歉，找不到任何語音：(")
                else:
                    for name in data["audio"]:
                        if "BASIC_PLAY" == name.upper():options.append(SelectOption(label="入場",description=name,value=str(i)+","+name))
                        elif "" == name:options.append(SelectOption(label="被選中",description=name,value=str(i)+","+name))
                        elif "BASIC_ATTACK" == name.upper():options.append(SelectOption(label="攻擊",description=name,value=str(i)+","+name))
                        elif "BASIC_DEATH" == name.upper():options.append(SelectOption(label="死亡",description=name,value=str(i)+","+name))
                        elif "CONCEDE" in name.upper():options.append(SelectOption(label="投降",description=name,value=str(i)+","+name))
                        elif "ERROR_FULL_MINIONS" in name.upper():options.append(SelectOption(label="滿場",description=name,value=str(i)+","+name))
                        elif "ERROR_GENERIC" in name.upper():options.append(SelectOption(label="無法這麼做",description=name,value=str(i)+","+name))
                        elif "ERROR_HAND_FULL" in name.upper():options.append(SelectOption(label="爆牌",description=name,value=str(i)+","+name))
                        elif "ERROR_I_ATTACKED" in name.upper():options.append(SelectOption(label="我已經攻擊過了",description=name,value=str(i)+","+name))
                        elif "ERROR_JUST_PLAYED" in name.upper():options.append(SelectOption(label="那個手下還不能攻擊",description=name,value=str(i)+","+name))
                        elif "ERROR_SUMMON_SICKNESS" in name.upper():options.append(SelectOption(label="那個手下還不能攻擊",description=name,value=str(i)+","+name))
                        elif "ERROR_MINION_ATTACKED" in name.upper():options.append(SelectOption(label="手下已經攻擊過了",description=name,value=str(i)+","+name))
                        elif "ERROR_NEED_MANA" in name.upper():options.append(SelectOption(label="我需要法力",description=name,value=str(i)+","+name))
                        elif "ERROR_NEED_WEAPON" in name.upper():options.append(SelectOption(label="我需要武器",description=name,value=str(i)+","+name))
                        elif "ERROR_PLAY" in name.upper():options.append(SelectOption(label="我無法打出這張牌",description=name,value=str(i)+","+name))
                        elif "ERROR_STEALTH" in name.upper():options.append(SelectOption(label="我無法指定潛行的目標",description=name,value=str(i)+","+name))
                        elif "PICKED" in name.upper():options.append(SelectOption(label="被選中",description=name,value=str(i)+","+name))
                        elif "ERROR_TARGET" in name.upper():options.append(SelectOption(label="我無法指定那個目標",description=name,value=str(i)+","+name))
                        elif "ERROR_TAUNT" in name.upper():options.append(SelectOption(label="必須先攻擊有嘲諷的手下",description=name,value=str(i)+","+name))
                        elif "FIRE_FESTIVAL" in name.upper():options.append(SelectOption(label="仲夏火焰節快樂",description=name,value=str(i)+","+name))
                        elif "LUNAR_NEW_YEAR" in name.upper():options.append(SelectOption(label="新春愉快",description=name,value=str(i)+","+name))
                        elif "GREETINGS_RESPONSE" in name.upper():options.append(SelectOption(label="你好(鏡像)",description=name,value=str(i)+","+name))
                        elif "MIRROR_GREETINGS" in name.upper():options.append(SelectOption(label="你好(鏡像)",description=name,value=str(i)+","+name))
                        elif "WINTERVEIL_GREETINGS" in name.upper():options.append(SelectOption(label="冬幕節快樂",description=name,value=str(i)+","+name))
                        elif "GREETINGS" in name.upper():options.append(SelectOption(label="你好",description=name,value=str(i)+","+name))
                        elif "HALLOWS_END" in name.upper():options.append(SelectOption(label="萬鬼節快樂",description=name,value=str(i)+","+name))
                        elif "HALLOWEEN" in name.upper():options.append(SelectOption(label="萬鬼節快樂",description=name,value=str(i)+","+name))
                        elif "LOW_CARDS" in name.upper():options.append(SelectOption(label="我快沒有牌了",description=name,value=str(i)+","+name))
                        elif "LOWCARDS" in name.upper():options.append(SelectOption(label="我快沒有牌了",description=name,value=str(i)+","+name))
                        elif "MIRROR_START" in name.upper():options.append(SelectOption(label="開場(鏡像)",description=name,value=str(i)+","+name))
                        elif "NOBLEGARDEN" in name.upper():options.append(SelectOption(label="歡慶貴族花園節",description=name,value=str(i)+","+name))
                        elif "NO_CARDS" in name.upper():options.append(SelectOption(label="我沒有牌了",description=name,value=str(i)+","+name))
                        elif "NOCARDS" in name.upper():options.append(SelectOption(label="我沒有牌了",description=name,value=str(i)+","+name))
                        elif "OOPS" in name.upper():options.append(SelectOption(label="唉呀",description=name,value=str(i)+","+name))
                        elif "PIRATE_DAY" in name.upper():options.append(SelectOption(label="海盜節快樂",description=name,value=str(i)+","+name))
                        elif "SORRY" in name.upper():options.append(SelectOption(label="抱歉",description=name,value=str(i)+","+name))
                        elif "START" in name.upper():options.append(SelectOption(label="開場",description=name,value=str(i)+","+name))
                        elif "THANKS" in name.upper():options.append(SelectOption(label="謝謝",description=name,value=str(i)+","+name))
                        elif "THINK1" in name.upper():options.append(SelectOption(label="思考1",description=name,value=str(i)+","+name))
                        elif "THINK2" in name.upper():options.append(SelectOption(label="思考2",description=name,value=str(i)+","+name))
                        elif "THINK3" in name.upper():options.append(SelectOption(label="思考3",description=name,value=str(i)+","+name))
                        elif "THINKING_1" in name.upper():options.append(SelectOption(label="思考1",description=name,value=str(i)+","+name))
                        elif "THINKING_2" in name.upper():options.append(SelectOption(label="思考2",description=name,value=str(i)+","+name))
                        elif "THINKING_3" in name.upper():options.append(SelectOption(label="思考3",description=name,value=str(i)+","+name))
                        elif "THINKING_01" in name.upper():options.append(SelectOption(label="思考1",description=name,value=str(i)+","+name))
                        elif "THINKING_02" in name.upper():options.append(SelectOption(label="思考2",description=name,value=str(i)+","+name))
                        elif "THINKING_03" in name.upper():options.append(SelectOption(label="思考3",description=name,value=str(i)+","+name))
                        elif "THREATEN" in name.upper():options.append(SelectOption(label="威脅",description=name,value=str(i)+","+name))
                        elif "TIME" in name.upper():options.append(SelectOption(label="時間快不夠了",description=name,value=str(i)+","+name))
                        elif "WELL_PLAYED" in name.upper():options.append(SelectOption(label="玩得不錯",description=name,value=str(i)+","+name))
                        elif "HOLIDAYS" in name.upper():options.append(SelectOption(label="冬幕節快樂",description=name,value=str(i)+","+name))
                        elif "WOW" in name.upper():options.append(SelectOption(label="厲害",description=name,value=str(i)+","+name))
                        elif "YEAR" in name.upper():options.append(SelectOption(label="新年快樂",description=name,value=str(i)+","+name))
                        else:options.append(SelectOption(label=name,description=name,value=str(i)+","+name))
                    if len(options)<=25:
                        select=Select(placeholder="選擇語音",options=options,min_values=1,max_values=1)
                        select.callback=get_audio
                        view.add_item(select)
                    elif len(options)>25 and len(options)<=50:
                        select1=Select(placeholder="選擇語音",options=options[:25],min_values=1,max_values=1)
                        select2=Select(placeholder="選擇語音",options=options[25:],min_values=1,max_values=1)
                        select1.callback=get_audio
                        view.add_item(select1)
                        select2.callback=get_audio
                        view.add_item(select2)
                    elif len(options)>25 and len(options)<=50:
                        select1=Select(placeholder="選擇語音",options=options[:25],min_values=1,max_values=1)
                        select2=Select(placeholder="選擇語音",options=options[25:50],min_values=1,max_values=1)
                        select3=Select(placeholder="選擇語音",options=options[50:],min_values=1,max_values=1)
                        select1.callback=get_audio
                        view.add_item(select1)
                        select2.callback=get_audio
                        view.add_item(select2)
                        select3.callback=get_audio
                        view.add_item(select3)
                    await interaction.followup.send("選擇語音",view=view)
    
#cmds
def embed_n(data:dict,lang:str):
    title=data['name'][lang]
    text=""
    view=View()
    if 'text' in data:text+=change_text(data["text"][lang])+"\n\n"
    if 'flavor' in data:text+=change_text(data['flavor'][lang])
    imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".png"
    cardview=f"https://playhearthstone.com/cards/"+str(data["dbfId"])
    if requests.request('GET',imgurl).status_code==404:
        imgurl=f"https://art.hearthstonejson.com/v1/512x/"+data["id"]+".jpg"
        if requests.request('GET',imgurl).status_code==404:
            imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
            text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
    embed = discord.Embed(title=title,url=cardview,description=text, color=0xff0000)
    embed.set_image(url=imgurl)
    embed.set_footer(text=str(data["dbfId"])+","+data["id"])
    audiobtn=Button(style=ButtonStyle.success,label="查看語音(繁中)",custom_id=str(data["dbfId"]))
    audiobtn.callback=audiobtn_callback
    view.add_item(audiobtn)
    return embed,view
def embed_bg(data:dict,lang):
#    async def select_new_embed(interaction):
#        for data in cardlib:
#            if data["dbfId"]==int(dict(interaction.data)['values'][0]):
#                embed,view=embed_bg(data,lang)
#                await interaction.response.edit_message(embed=embed,view=view)
    async def button_new_embed(interaction):
        await interaction.response.defer()
        for data in cardlib:
            if data["dbfId"]==int(dict(interaction.data)['custom_id']):
                embed,view=embed_bg(data,lang)
                await interaction.followup.edit_message(interaction.message.id,embed=embed,view=view)
    view=View()
    title=data['name'][lang]
    text=""
    imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".png"
    cardview=f"https://playhearthstone.com/battlegrounds/"+str(data["dbfId"])
    token=get_token()
    bzlang=lang[0:2]+"_"+lang[2:4]
    url=f'https://tw.api.blizzard.com/hearthstone/cards/{data["dbfId"]}?locale={bzlang}&gameMode=battlegrounds&access_token={token}'
    if data["type"]=="HERO":
        try:
            imgurl=json.loads(requests.request('GET',url).text)['battlegrounds']['image']
        except:
            imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".jpg"
            if requests.request('GET',imgurl).status_code==404:
                imgurl=f"https://art.hearthstonejson.com/v1/512x/"+data["id"]+".jpg"
                if requests.request('GET',imgurl).status_code==404:
                    imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
                    text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
        if 'battlegroundsBuddyDbfId' in data:
            text+="\n夥伴dbfId:"+str(data['battlegroundsBuddyDbfId'])
            button=Button(style=ButtonStyle.success,label="查看夥伴",custom_id=str(data['battlegroundsBuddyDbfId']))
            button.callback=button_new_embed
            view.add_item(button)
    elif data["type"]=="MINION":
        if "techLevel" in data:text+=f"旅店等級{data['techLevel']}"
        if "health" and "attack" in data:f"體質:{data['health']}/{data['health']}"
        if 'text' in data:text+="\n"+change_text(data["text"][lang])+"\n"
        if "battlegroundsPremiumDbfId" in data:
            try:
                imgurl=json.loads(requests.request('GET',url).text)['battlegrounds']['image']
            except:
                imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".jpg"
                if requests.request('GET',imgurl).status_code==404:
                    imgurl=f"https://art.hearthstonejson.com/v1/512x/"+data["id"]+".jpg"
                    if requests.request('GET',imgurl).status_code==404:
                        imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
                        text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
            text+="\n金卡dbfId:"+str(data['battlegroundsPremiumDbfId'])
            button=Button(style=ButtonStyle.success,label="查看金卡",custom_id=str(data['battlegroundsPremiumDbfId']))
            button.callback=button_new_embed
            view.add_item(button)
        elif "battlegroundsNormalDbfId" in data:
            try:
                imgurl=json.loads(requests.request('GET',url).text)['battlegrounds']['imageGold']
            except:
                imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".jpg"
                if requests.request('GET',imgurl).status_code==404:
                    imgurl=f"https://art.hearthstonejson.com/v1/512x/"+data["id"]+".jpg"
                    if requests.request('GET',imgurl).status_code==404:
                        imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
                        text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
            text+="\n普卡dbfId:"+str(data['battlegroundsNormalDbfId'])
            button=Button(style=ButtonStyle.success,label="查看普卡",custom_id=str(data['battlegroundsNormalDbfId']))
            button.callback=button_new_embed
            view.add_item(button)
        if "isBattlegroundsBuddy" in data:
            for hero in cardlib:
                if 'battlegroundsBuddyDbfId' in hero:
                    if hero['battlegroundsBuddyDbfId']==data["dbfId"]:
                        text+="\n夥伴dbfId:"+str(hero["dbfId"])
                        button=Button(style=ButtonStyle.success,label="查看夥伴",custom_id=str(hero["dbfId"]))
                        button.callback=button_new_embed
                        view.add_item(button)
                    if "battlegroundsNormalDbfId" in data:
                        if hero['battlegroundsBuddyDbfId']==data["battlegroundsNormalDbfId"]:
                            text+="\n夥伴dbfId:"+str(hero["dbfId"])
                            button=Button(style=ButtonStyle.success,label="查看夥伴",custom_id=str(hero["dbfId"]))
                            button.callback=button_new_embed
                            view.add_item(button)
    else:
        imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".jpg"
        if requests.request('GET',imgurl).status_code==404:
            imgurl=f"https://art.hearthstonejson.com/v1/512x/"+data["id"]+".jpg"
            if requests.request('GET',imgurl).status_code==404:
                imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
                text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
    embed = discord.Embed(title=title,url=cardview,description=text, color=0xff0000)
    embed.set_image(url=imgurl)
    embed.set_footer(text=str(data["dbfId"])+","+data["id"])
    audiobtn=Button(style=ButtonStyle.success,label="查看語音(繁中)",custom_id=str(data["dbfId"]))
    audiobtn.callback=audiobtn_callback
    view.add_item(audiobtn)
    return embed,view

def embed_m(data:dict,lang):
    view=View()
    title=data['name'][lang]
    text=""
    imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".png"
    cardview=f"https://playhearthstone.com/zh-tw/mercenaries/"+str(data["dbfId"])
    if requests.request('GET',imgurl).status_code==404:
        imgurl=f"https://art.hearthstonejson.com/v1/512x/"+data["id"]+".jpg"
        if requests.request('GET',imgurl).status_code==404:
            imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
            text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
    #傭兵子父卡牌功能
    async def select_new_embed(interaction):
        await interaction.response.defer()
        for data in cardlib:
            if data["dbfId"]==int(dict(interaction.data)['values'][0]):
                embed,view=embed_m(data,lang)
                await interaction.followup.edit_message(interaction.message.id,embed=embed,view=view)
    async def button_new_embed(interaction):
        await interaction.response.defer()
        for data in cardlib:
            if data["dbfId"]==int(dict(interaction.data)['custom_id']):
                embed,view=embed_m(data,lang)
                await interaction.followup.edit_message(interaction.message.id,embed=embed,view=view)
    if data["type"]=="LETTUCE_ABILITY":
        if data["cost"]==0:
            if 'text' in data:text+=change_text(data["text"][lang])+"\n"
            run=False
            for h_data in cardlibm:
                if "equipment" in h_data:
                    for e_data in h_data["equipment"]:
                        if "tiers" in e_data:
                            for e in e_data["tiers"]:
                                if e["dbf_id"]==data["dbfId"]:
                                    for ownerdata in cardlib:
                                        if ownerdata["dbfId"]==h_data["defaultSkinDbfId"] and run is False:
                                            text+="此為 **"+ownerdata['name'][lang]+"**("+str(ownerdata['dbfId'])+","+str(ownerdata['id'])+") 的裝備。\n"
                                            if len(e_data['tiers'])>1:
                                                text+="\n該裝備其他等級的dbfId:\n"
                                                options_e=[]
                                                for otd in e_data['tiers']:
                                                    if otd["dbf_id"]!=data["dbfId"]:
                                                        text+="等級"+str(otd["tier"])+":"+str(otd["dbf_id"])+"\n"
                                                        options_e.append(SelectOption(label="等級"+str(otd["tier"]),value=str(otd["dbf_id"]),description=str(otd["dbf_id"])))
                                                select=Select(placeholder="該裝備其他等級",options=options_e,min_values=1,max_values=1)
                                                select.callback=select_new_embed
                                                view.add_item(select)
                                            button=Button(style=ButtonStyle.success,label="查看傭兵",custom_id=str(ownerdata['dbfId']))
                                            button.callback=button_new_embed
                                            view.add_item(button)
                                            run=True 
        elif data["cost"]!=0:
            if "cost" in data:text+="速度:"+str(data['cost'])
            if "mercenariesAbilityCooldown" in data:text+=" 冷卻時間:"+str(data['mercenariesAbilityCooldown'])
            if text in data:text+="\n"+change_text(data["text"][lang])+"\n"
            run=False
            for h_data in cardlibm:
                if "specializations" in h_data:
                    if len(h_data["specializations"])>0:
                        if "abilities" in h_data["specializations"][0]:
                            for p_data in h_data["specializations"][0]["abilities"]:
                                if "tiers" in p_data:
                                    for p in p_data["tiers"]:
                                        if p["dbf_id"]==data["dbfId"]:
                                            for ownerdata in cardlib:
                                                if ownerdata["dbfId"]==h_data["defaultSkinDbfId"] and run is False:
                                                    text+="\n此為 **"+ownerdata['name'][lang]+"**("+str(ownerdata['dbfId'])+","+str(ownerdata['id'])+") 的技能。\n"
                                                    if len(p_data['tiers'])>1:
                                                        options_p=[]
                                                        text+="\n該技能其他等級的dbfId:\n"
                                                        for otd in p_data['tiers']:
                                                            if otd["dbf_id"]!=data["dbfId"]:
                                                                text+="等級"+str(otd["tier"])+":"+str(otd["dbf_id"])+"\n"
                                                                options_p.append(SelectOption(label="等級"+str(otd["tier"]),value=str(otd["dbf_id"]),description=str(otd["dbf_id"])))
                                                        select=Select(placeholder="該技能其他等級",options=options_p,min_values=1,max_values=1)
                                                        select.callback=select_new_embed
                                                        view.add_item(select)
                                                    button=Button(style=ButtonStyle.success,label="查看傭兵",custom_id=str(ownerdata['dbfId']))
                                                    button.callback=button_new_embed
                                                    view.add_item(button)
                                                    run=True
        else:
            if text in data:text+=change_text(data['text'][lang])
    elif data["type"]=="MINION":
        if 'text' in data:text+=change_text(data['text'][lang])
        for h_data in cardlibm:
            if data["dbfId"] in h_data["skinDbfIds"]:
                text+="(下方可選擇查看造型、裝備、技能)\n"
                if "skinDbfIds" in h_data:
                    skins=[]
                    for i,skin in enumerate(h_data["skinDbfIds"],1):
                        skins.append(SelectOption(label=f"造型{i}",value=str(skin),description=skin))
                    select_s=Select(placeholder="選擇要查看的造型",options=skins,min_values=1,max_values=1)
                    select_s.callback=select_new_embed
                    view.add_item(select_s)
                if "equipment" in h_data:
                    if len(h_data["equipment"])>=1:
                        options_e=[]
                        text+="**該傭兵裝備:**\n"
                        for i,e_data in enumerate(h_data["equipment"],1):
                            for tiers in e_data["tiers"]:
                                for c_data in cardlib:
                                    if tiers["dbf_id"] == c_data["dbfId"]:
                                        if tiers['tier']==1:text+=f"裝備{str(i)}等級1:{c_data['name'][lang]}({c_data['dbfId']})\n"
                                        d=change_text(c_data['text'][lang]).replace('*','').replace('\n','')
                                        if len(d)>80:d=d[0:75]+"..."
                                        options_e.append(SelectOption(label=f"{c_data['name'][lang]}(裝備{str(i)}等級{tiers['tier']})\n",value=str(c_data['dbfId']),description=d))
                        select_e=Select(placeholder="選擇要查看的裝備",options=options_e,min_values=1,max_values=1)
                        select_e.callback=select_new_embed
                        view.add_item(select_e)
                        if "specializations" in h_data:
                            if len(h_data["specializations"])>0:
                                if "abilities" in h_data["specializations"][0]:
                                    if len(h_data["specializations"][0]["abilities"])>=1:
                                        options_p=[]
                                        text+="**該傭兵技能:**\n"
                                        for i,p_data in enumerate(h_data["specializations"][0]["abilities"],1):
                                            if "tiers" in p_data: 
                                                for tiers in p_data["tiers"]:
                                                    for c_data in cardlib:
                                                        if tiers["dbf_id"] == c_data["dbfId"]:
                                                             if tiers['tier']==1:text+=f"技能{str(i)}等級1:{c_data['name'][lang]}({c_data['dbfId']})\n"
                                                             d=change_text(c_data['text'][lang]).replace('*','').replace('\n','')
                                                             if len(d)>80:d=d[0:75]+"..."
                                                             options_p.append(SelectOption(label=f"{c_data['name'][lang]}(技能{str(i)}等級{tiers['tier']})\n",value=str(c_data['dbfId']),description=d))
                                        select_p=Select(placeholder="選擇要查看的技能",options=options_p,min_values=1,max_values=1)
                                        select_p.callback=select_new_embed
                                        view.add_item(select_p)
    else:
        text=change_text(data["text"][lang])
    embed = discord.Embed(title=title,url=cardview,description=text, color=0xff0000)
    embed.set_image(url=imgurl)
    embed.set_footer(text=str(data["dbfId"])+","+data["id"])
    audiobtn=Button(style=ButtonStyle.success,label="查看語音(繁中)",custom_id=str(data["dbfId"]))
    audiobtn.callback=audiobtn_callback
    view.add_item(audiobtn)
    return embed,view

@bot.command()
async def id(msg,cardid=None,lang="zhTW"):
    if cardid==None:
        await msg.reply("※不推薦新手使用該指令\n該指令使用方法:\"t!id dbfId或id 語言(選填)\"\n例子1(使用dbfId):`t!id 38833`\n例子2(使用id):`t!id OG_272`")
    else:
        if lang in langlist:
            find=False
            if cardid.isdigit() is True:
                for data in cardlib:
                    if data["dbfId"]==int(cardid):
                        find=True
                        break
            else:
                for data in cardlib:
                    if data["id"]==cardid:
                        find=True
                        break
            if find is True:
                if data["set"]=="LETTUCE":
                    embed,view=embed_m(data,lang)
                    await msg.reply(embed=embed,view=view)
                elif data["set"]=="BATTLEGROUNDS":
                    embed,view=embed_bg(data,lang)
                    await msg.reply(embed=embed,view=view)
                else:
                    embed,view=embed_n(data,lang)
                    await msg.reply(embed=embed,view=view)
            else:await msg.reply("查無此卡!")
        else:await msg.reply("語系錯誤!全部的語系:\n"+",".join(langlist))

@bot.command()
async def card(msg,cardname=None,lang="zhTW"):
    if cardname==None:
        await msg.reply("空格請用下滑線\'_\'代替\n該指令使用方法:\"t!card 卡牌名稱 語言(選填)\"\n例子:`t!card 暮光召喚師`")
    else:
        if lang in langlist:
            cardname=cardname.replace('_',' ')
            find=[]
            view=View()
            for data in cardlib:
                if "type" in data:
                    if data["type"]!="ENCHANTMENT":
                        if cardname in data["name"][lang]:find.append(data)
                        elif cardname in group:
                            if group[cardname] in data["name"][lang]:
                                find.append(data)
                        elif 'text' in data:
                            if cardname in data["text"][lang].replace("\n",""):find.append(data)
            if len(find)==0:await msg.reply("查無卡牌！")
            elif len(find)==1:
                if find[0]["set"]=="LETTUCE":
                    embed,view=embed_m(find[0],lang)
                    await msg.reply(embed=embed,view=view)
                elif find[0]["set"]=="BATTLEGROUNDS":
                    embed,view=embed_bg(find[0],lang)
                    await msg.reply(embed=embed,view=view)
                else:
                    embed,view=embed_n(find[0],lang)
                    await msg.reply(embed=embed,view=view)
            elif len(find)>49:
                await msg.reply("由於數量過多，請更改關鍵字縮小範圍。",view=view)
            else:
                options=[]
                options.append(SelectOption(label="全部發送到私人訊息",value="-1",description="可搭配 t!id 指令"))
                for i,data in enumerate(find):
                    text=""
                    if 'text' in data:text=change_text(data["text"][lang]).replace("*","").replace("\n","").replace("[x]","")
                    if len(text)>95:text=text[0:94]+"..."
                    options.append(SelectOption(label=f'{data["name"][lang]}({data["dbfId"]},{data["id"]})',value=str(i),description=text))
                async def select_callback(interaction):
                    if int(dict(interaction.data)['values'][0])==-1:
                        await interaction.response.edit_message(content="已發送至私人訊息",view=None)
                        for data in find:
                            if data["set"]=="LETTUCE":
                                embed,view=embed_m(data,lang)
                                await msg.author.send(embed=embed,view=view)
                            elif data["set"]=="BATTLEGROUNDS":
                                embed,view=embed_bg(data,lang)
                                await msg.author.send(embed=embed,view=view)
                            else:
                                embed,view=embed_n(data,lang)
                                await msg.author.send(embed=embed,view=view)
                    else:
                        await interaction.response.defer()
                        if find[int(dict(interaction.data)['values'][0])]["set"]=="LETTUCE":
                            embed,view=embed_m(find[int(dict(interaction.data)['values'][0])],lang)
                            await interaction.followup.edit_message(interaction.message.id,content="",embed=embed,view=view)
                        elif find[int(dict(interaction.data)['values'][0])]["set"]=="BATTLEGROUNDS":
                            embed,view=embed_bg(find[int(dict(interaction.data)['values'][0])],lang)
                            await interaction.followup.edit_message(interaction.message.id,content="",embed=embed,view=view)
                        else:
                            embed,view=embed_n(find[int(dict(interaction.data)['values'][0])],lang)
                            await interaction.followup.edit_message(interaction.message.id,content="",embed=embed,view=view)
                if len(options)<=25:
                    select=Select(min_values=1,max_values=1,options=options)
                    select.callback=select_callback
                    view.add_item(select)
                else:
                    select1=Select(min_values=1,max_values=1,options=options[:25])
                    select1.callback=select_callback
                    view.add_item(select1)
                    select2=Select(min_values=1,max_values=1,options=options[25:])
                    select2.callback=select_callback
                    view.add_item(select2)
                await msg.reply("選擇你想找的卡牌",view=view)
        else:await msg.reply("語系錯誤!全部的語系:\n"+",".join(langlist))



@bot.command()
async def merc(msg,cardname=None,lang="zhTW"):
    if cardname==None:
        await msg.reply("該指令使用方法:\"t!merc 傭兵、裝備、技能名稱 語言(選填)\"\n例子1(傭兵):`t!merc 餅乾大廚`\n例子2(裝備):`t!merc 養好的鍋子`\n例子3(技能):`t!merc 魚肉大餐`")
    else:
        if lang in langlist:
            cardname=cardname.replace('_',' ')
            find=[]
            view=View()
            for data in cardlib:
                if "type" in data and "set" in data:
                    if data["type"]!="ENCHANTMENT" and data["set"]=="LETTUCE":
                        if cardname in data["name"][lang]:find.append(data)
                        elif cardname in group:
                            if group[cardname] in data["name"][lang]:
                                find.append(data)
                        elif 'text' in data:
                            if cardname in data["text"][lang].replace("\n",""):find.append(data)
            if len(find)==0:await msg.reply("查無卡牌！")
            elif len(find)==1:
                embed,view=embed_m(find[0],lang)
                await msg.reply(embed=embed,view=view)
            elif len(find)>49:
                await msg.reply("由於數量過多，請更改關鍵字縮小範圍。",view=view)
            else:
                options=[]
                options.append(SelectOption(label="全部發送到私人訊息",value="-1",description="可搭配 t!id 指令"))
                for i,data in enumerate(find):
                    text=""
                    if 'text' in data:text=change_text(data["text"][lang]).replace("*","").replace("[x]","")
                    if len(text)>95:text=text[0:94]+"..."
                    options.append(SelectOption(label=f'{data["name"][lang]}({data["dbfId"]},{data["id"]})',value=str(i),description=text))
                async def select_callback(interaction):
                    if int(dict(interaction.data)['values'][0])==-1:
                        await interaction.response.edit_message(content="已發送至私人訊息",view=None)
                        for data in find:
                            embed,view=embed_m(data,lang)
                            await msg.author.send(embed=embed,view=view)
                    else:
                        await interaction.response.defer()
                        embed,view=embed_m(find[int(dict(interaction.data)['values'][0])],lang)
                        await interaction.followup.edit_message(interaction.message.id,content="",embed=embed,view=view)
                if len(options)<=25:
                    select=Select(min_values=1,max_values=1,options=options)
                    select.callback=select_callback
                    view.add_item(select)
                else:
                    select1=Select(min_values=1,max_values=1,options=options[:25])
                    select1.callback=select_callback
                    view.add_item(select1)
                    select2=Select(min_values=1,max_values=1,options=options[25:])
                    select2.callback=select_callback
                    view.add_item(select2)
                await msg.reply("選擇你想找的卡牌",view=view)
        else:await msg.reply("語系錯誤!全部的語系:\n"+",".join(langlist))

@bot.command()
async def bg(msg,cardname=None,lang="zhTW"):
    if cardname==None:
        await msg.reply("該指令使用方法:\"t!bg 戰場卡牌 語言(選填)\"\n例子:`t!bg 餅乾大廚`")
    else:
        if lang in langlist:
            cardname=cardname.replace('_',' ')
            find=[]
            view=View()
            for data in cardlib:
                if "type" in data and "set" in data:
                    if data["type"]!="ENCHANTMENT":
                        if "isBattlegroundsPoolMinion" in data or data["set"]=="BATTLEGROUNDS":
                            if cardname in data["name"][lang]:find.append(data)
                            elif cardname in group:
                                if group[cardname] in data["name"][lang]:
                                    find.append(data)
                            elif 'text' in data:
                                if cardname in data["text"][lang].replace("\n",""):find.append(data)
            if len(find)==0:await msg.reply("查無卡牌！")
            elif len(find)==1:
                embed,view=embed_bg(find[0],lang)
                await msg.reply(embed=embed,view=view)
            elif len(find)>49:
                await msg.reply("由於數量過多，請更改關鍵字縮小範圍。",view=view)
            else:
                options=[]
                options.append(SelectOption(label="全部發送到私人訊息",value="-1",description="可搭配 t!id 指令"))
                for i,data in enumerate(find):
                    text=""
                    if 'text' in data:text=change_text(data["text"][lang]).replace("*","").replace("[x]","")
                    if len(text)>95:text=text[0:94]+"..."
                    options.append(SelectOption(label=f'{data["name"][lang]}({data["dbfId"]},{data["id"]})',value=str(i),description=text))
                async def select_callback(interaction):
                    if int(dict(interaction.data)['values'][0])==-1:
                        await interaction.response.edit_message(content="已發送至私人訊息",view=None)
                        for data in find:
                            embed,view=embed_bg(data,lang)
                            await msg.author.send(embed=embed,view=view)
                    else:
                        await interaction.response.defer()
                        embed,view=embed_bg(find[int(dict(interaction.data)['values'][0])],lang)
                        await interaction.followup.edit_message(interaction.message.id,content="",embed=embed,view=view)
                if len(options)<=25:
                    select=Select(min_values=1,max_values=1,options=options)
                    select.callback=select_callback
                    view.add_item(select)
                else:
                    select1=Select(min_values=1,max_values=1,options=options[:25])
                    select1.callback=select_callback
                    view.add_item(select1)
                    select2=Select(min_values=1,max_values=1,options=options[25:])
                    select2.callback=select_callback
                    view.add_item(select2)
                await msg.reply("選擇你想找的卡牌",view=view)
        else:await msg.reply("語系錯誤!全部的語系:\n"+",".join(langlist))

def deck_embed(msg,deckcode,deckname,lang,m):
    heroclass=""
    deck = Deck.from_deckstring(deckcode)
    if deck.format==FormatType.FT_WILD:mode="開放模式(wild)"
    elif deck.format==FormatType.FT_STANDARD:mode="標準模式(standard)"
    elif deck.format==FormatType.FT_CLASSIC:mode="經典模式(classic)"
    else: mode="其他模式(other)"
    unfind=deck.cards.copy()
    find=[]
    deckhero=""
    heroID=""
    for data in cardlib:
        if deckhero=="" and deck.heroes[0]==data["dbfId"]:
            deckhero=data["name"][lang]
            heroID=data["id"]
            heroclass=classdict[data['cardClass']]
        for i,cardid in enumerate(unfind):
            if cardid[0]==data["dbfId"]:
                card=data.copy()
                card.update({"count":cardid[1]})
                find.append(card)
                del unfind[i]
                break
    txt=""
    count=0
    cost=0
    find.sort(key=lambda x:x["cost"])
    for data in find:
        if m==0:
            txt+=str(data["count"]) +" × " +"("+str(data["cost"])+") "+ data["name"][lang]+"\n"
        elif m==1:
            txt+=str(data["count"]) +" × " +"("+str(data["cost"])+") **"+ data["name"][lang]+ "** (" + str(data["dbfId"])+","+data["id"]+")\n"
        count+=data["count"]
        if "CORE"!=data["set"] and "rarity" in data:
            if data["rarity"]=="COMMON":cost+=40*data["count"]
            elif data["rarity"]=="RARE":cost+=100*data["count"]
            elif data["rarity"]=="EPIC":cost+=400*data["count"]
            elif data["rarity"]=="LEGENDARY":cost+=1600*data["count"]
    if deckname is None:title=msg.author.name+" 的套牌"
    else:title=deckname
    embed=discord.Embed(title=title, description=f'{mode} 職業:{heroclass}(英雄:{deckhero})\n共{str(count)}張牌\n\n'+txt,url=f'https://playhearthstone.com/zh-tw/deckbuilder?deckcode={deckcode}',color=0xff0000)
    embed.set_thumbnail(url="https://art.hearthstonejson.com/v1/orig/"+heroID+".png")
    embed.set_footer(text="所需魔塵:"+str(cost))
    async def advanced(interaction):
        await interaction.response.defer()
        if dict(interaction.data)['custom_id']=="0":
            embed,view=deck_embed(msg,deckcode,deckname,lang,1)
            await interaction.followup.edit_message(interaction.message.id,embed=embed,view=view)
        elif dict(interaction.data)['custom_id']=="1":
            embed,view=deck_embed(msg,deckcode,deckname,lang,0)
            await interaction.followup.edit_message(interaction.message.id,embed=embed,view=view)
    view=View()
    if m==0:
        button=Button(style=ButtonStyle.red,label="顯示進階資訊",custom_id="0")
    elif m==1:
        button=Button(style=ButtonStyle.green,label="隱藏進階資訊",custom_id="1")
    button.callback=advanced
    view.add_item(button)

    return embed,view
    

@bot.command()
async def deck(msg,deckcode=None,deckname=None,lang="zhTW"):
    if deckcode==None:
        await msg.reply("該指令使用方法:\"t!deck 牌組代碼 牌組名稱(選填) 語言(選填)\"\n例子1(無套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA`\n例子2(有套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA 無限潛行`")
    else:
        if lang in langlist:
            embed,view=deck_embed(msg,deckcode,deckname,lang,0)
            await msg.reply(embed=embed,view=view)
            if deckname!=None:
                await msg.reply(f"###{deckname}\n{deckcode}\n# 若要使用此套牌，請先複製此訊息，然後在爐石戰記中建立一副新的套牌")
            else:
                await msg.reply(f"{deckcode}\n# 若要使用此套牌，請先複製此訊息，然後在爐石戰記中建立一副新的套牌")
        else:await msg.reply("語系錯誤!全部的語系:\n"+",".join(langlist))



DCTOKEN=env['DCTOKEN']
#loop
if __name__=="__main__":
    bot.run(DCTOKEN)
