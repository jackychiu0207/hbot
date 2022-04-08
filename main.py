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


bot = commands.Bot(command_prefix="t!",help_command=None,intents=intents)


classdict={"DEATHKNIGHT":"死亡騎士","DEMONHUNTER":"惡魔獵人","DREAM":"伊瑟拉","DRUID":"德魯伊","HUNTER":"獵人","INVALID":"未知/不適用職業","MAGE":"法師","NEUTRAL":"中立","PALADIN":"聖騎士","PRIEST":"牧師","ROGUE": 7,"SHAMAN":"薩滿","WARLOCK":"術士","WARRIOR":"戰士","WHIZBANG":"威茲幫"}

def getjson():
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
    url='https://raw.githubusercontent.com/jackychiu0207/hbot/main/group.json'
    req = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    oper = urllib.request.urlopen(req)
    data = oper.read()
    file = open('group.json','wb')
    file.write(data)
    file.close()

def openjson():
    global cardlib,cardlibm,group
    try:
        cardlib=json.load(open('cards.json'))
        cardlibm=json.load(open('mercenaries.json'))
        group=json.load(open('group.json'))
        env=json.load(open('.env'))
    except:
        return False
getjson()
openjson()

@bot.command()
async def reloadjson(msg):
    try:
        cardlibm.close()
        cardlib.close()
        group.close()
        os.remove('cards.json')
        os.remove('mercenaries.json')
        os.remove('group.json')
    except:
        pass
    getjson()
    if openjson() is not False:
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
    embed.add_field(name="t!deck",value="使用方法:\"t!deck 牌組代碼 牌組名稱(選填) \"\n例子1(無套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA`\n例子2(有套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA 無限潛行`", inline=False)
    embed.add_field(name="t!reloadjson",value="直接輸入，機器人會更新資料庫。當找不到覺得存在的卡牌時，可以使用此指令。")
    embed.add_field(name="t!stop",value="直接輸入，機器人會直接停止。只有在緊急狀況才可使用，勿隨意使用")
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


#cmds
def embed_n(data:dict,lang):
    title=data['name'][lang]
    text=""
    if 'text' in data:text+=change_text(data["text"][lang])+"\n\n"
    if 'flavor' in data:text+=change_text(data['flavor'][lang])
    imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".png"
    cardview=f"https://playhearthstone.com/cards/"+str(data["dbfId"])
    if requests.request('GET',imgurl).status_code==404:
        imgurl=f"https://art.hearthstonejson.com/v1/256x/"+data["id"]+".jpg"
        if requests.request('GET',imgurl).status_code==404:
            imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
            text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
    embed = discord.Embed(title=title,url=cardview,description=text, color=0xff0000)
    embed.set_image(url=imgurl)
    embed.set_footer(text=str(data["dbfId"])+","+data["id"])
    return embed
def embed_bg(data:dict,lang):
#    async def select_new_embed(interaction):
#        for data in cardlib:
#            if data["dbfId"]==int(dict(interaction.data)['values'][0]):
#                embed,view=embed_bg(data,lang)
#                await interaction.response.edit_message(embed=embed,view=view)
    async def button_new_embed(interaction):
        for data in cardlib:
            if data["dbfId"]==int(dict(interaction.data)['custom_id']):
                embed,view=embed_bg(data,lang)
                await interaction.response.edit_message(embed=embed,view=view)
    view=View()
    title=data['name'][lang]
    text=""
    imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".png"
    cardview=f"https://playhearthstone.com/battlegrounds/"+str(data["dbfId"])
    token=get_token()
    bzlang=lang[0:2]+"_"+lang[2:4]
    url=f'https://tw.api.blizzard.com/hearthstone/cards/{data["dbfId"]}?locale={bzlang}&gameMode=battlegrounds&access_token={token}'
    if data["type"]=="HERO":
        if 'battlegroundsBuddyDbfId' in data:
            imgurl=json.loads(requests.request('GET',url).text)['battlegrounds']['image']
            text+="\n夥伴dbfId:"+str(data['battlegroundsBuddyDbfId'])
            button=Button(style=ButtonStyle.success,label="查看夥伴",custom_id=str(data['battlegroundsBuddyDbfId']))
            button.callback=button_new_embed
            view.add_item(button)
    elif data["type"]=="MINION":
        if "techLevel" in data:text+=f"旅店等級{data['techLevel']}"
        if "health" and "attack" in data:f"體質:{data['health']}/{data['health']}"
        if 'text' in data:text+="\n"+change_text(data["text"][lang])+"\n"
        if "battlegroundsPremiumDbfId" in data:
            imgurl=json.loads(requests.request('GET',url).text)['battlegrounds']['image']
            text+="\n金卡dbfId:"+str(data['battlegroundsPremiumDbfId'])
            button=Button(style=ButtonStyle.success,label="查看金卡",custom_id=str(data['battlegroundsPremiumDbfId']))
            button.callback=button_new_embed
            view.add_item(button)
        elif "battlegroundsNormalDbfId" in data:
            imgurl=json.loads(requests.request('GET',url).text)['battlegrounds']['imageGold']
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
    if requests.request('GET',imgurl).status_code==404:
        imgurl=f"https://art.hearthstonejson.com/v1/256x/"+data["id"]+".jpg"
        if requests.request('GET',imgurl).status_code==404:
            imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
            text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
    embed = discord.Embed(title=title,url=cardview,description=text, color=0xff0000)
    embed.set_image(url=imgurl)
    embed.set_footer(text=str(data["dbfId"])+","+data["id"])
    return embed,view

def embed_m(data:dict,lang):
    view=View()
    title=data['name'][lang]
    text=""
    imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".png"
    cardview=f"https://playhearthstone.com/zh-tw/mercenaries/"+str(data["dbfId"])
    if requests.request('GET',imgurl).status_code==404:
        imgurl=f"https://art.hearthstonejson.com/v1/256x/"+data["id"]+".jpg"
        if requests.request('GET',imgurl).status_code==404:
            imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
            text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
    #傭兵子父卡牌功能
    async def select_new_embed(interaction):
        for data in cardlib:
            if data["dbfId"]==int(dict(interaction.data)['values'][0]):
                embed,view=embed_m(data,lang)
                await interaction.response.edit_message(embed=embed,view=view)
    async def button_new_embed(interaction):
        for data in cardlib:
            if data["dbfId"]==int(dict(interaction.data)['custom_id']):
                embed,view=embed_m(data,lang)
                await interaction.response.edit_message(embed=embed,view=view)
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
                                            if len(e_data['tiers'])>1:text+="\n該裝備其他等級的dbfId:\n"
                                            for otd in e_data['tiers']:
                                                if otd["dbf_id"]!=data["dbfId"]:
                                                    text+="等級"+str(otd["tier"])+":"+str(otd["dbf_id"])+"\n"
                                                    button=Button(style=ButtonStyle.gray,label="查看等級"+str(otd["tier"]),custom_id=str(otd["dbf_id"]))
                                                    button.callback=button_new_embed
                                                    view.add_item(button)
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
                                                    if len(p_data['tiers'])>1:text+="\n該技能其他等級的dbfId:\n"
                                                    for otd in p_data['tiers']:
                                                        if otd["dbf_id"]!=data["dbfId"]:
                                                            text+="等級"+str(otd["tier"])+":"+str(otd["dbf_id"])+"\n"
                                                            button=Button(style=ButtonStyle.gray,label="查看等級"+str(otd["tier"]),custom_id=str(otd["dbf_id"]))
                                                            button.callback=button_new_embed
                                                            view.add_item(button)
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
    return embed,view

@bot.command()
async def id(msg,cardid=None,lang="zhTW"):
    if cardid==None:
        await msg.reply("※不推薦新手使用該指令\n該指令使用方法:\"t!id dbfId或id 語言(選填)\"\n例子1(使用dbfId):`t!id 38833`\n例子2(使用id):`t!id OG_272`")
    else:
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
            else:await msg.reply(embed=embed_n(data,lang))
        else:await msg.reply("查無此卡!")

@bot.command()
async def card(msg,cardname=None,lang="zhTW"):
    if cardname==None:
        await msg.reply("空格請用下滑線\'_\'代替\n該指令使用方法:\"t!card 卡牌名稱 語言(選填)\"\n例子:`t!card 暮光召喚師`")
    else:
        cardname=cardname.replace('_',' ')
        find=[]
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
            else:await msg.reply(embed=embed_n(find[0],lang))
        elif len(find)>24:
            async def callback_allcards(interaction):
              await interaction.response.edit_message(content="已發送至私人訊息",view=None)
              for data in find:
                    if data["set"]=="LETTUCE":
                        embed,view=embed_m(data,lang)
                        await msg.author.send(embed=embed,view=view)
                    elif data["set"]=="BATTLEGROUNDS":
                        embed,view=embed_bg(data,lang)
                        await msg.author.send(embed=embed,view=view)
                    else:await msg.author.send(embed=embed_n(data,lang))
            button=Button(style=ButtonStyle.success,label="發送所有卡牌至私人訊息")
            button.callback=callback_allcards
            view=View()
            view.add_item(button)
            await msg.reply("由於數量過多，請更改關鍵字縮小範圍。",view=view)
        else:
            options=[]
            options.append(SelectOption(label="全部發送到私人訊息",value="-1",description="可搭配 t!id 指令"))
            for i,data in enumerate(find):
                text=""
                if 'text' in data:text=change_text(data["text"][lang]).replace("*","").replace("\n","").replace("[x]","")
                if len(text)>95:text=text[0:94]+"..."
                options.append(SelectOption(label=f'{data["name"][lang]}({data["dbfId"]},{data["id"]})',value=str(i),description=text))
            select=Select(min_values=1,max_values=1,options=options)
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
                        else:await msg.author.send(embed=embed_n(data,lang))
                else:
                    if find[int(dict(interaction.data)['values'][0])]["set"]=="LETTUCE":
                        embed,view=embed_m(find[int(dict(interaction.data)['values'][0])],lang)
                        await interaction.response.edit_message(content="",embed=embed,view=view)
                    elif find[int(dict(interaction.data)['values'][0])]["set"]=="BATTLEGROUNDS":
                        embed,view=embed_bg(find[int(dict(interaction.data)['values'][0])],lang)
                        await interaction.response.edit_message(content="",embed=embed,view=view)
                    else:await interaction.response.edit_message(content="",embed=embed_n(find[int(dict(interaction.data)['values'][0])],lang),view=None)
            select.callback=select_callback
            view=View()
            view.add_item(select)
            await msg.reply("選擇你想找的卡牌",view=view)



@bot.command()
async def merc(msg,cardname=None,lang="zhTW"):
    if cardname==None:
        await msg.reply("該指令使用方法:\"t!merc 傭兵、裝備、技能名稱 語言(選填)\"\n例子1(傭兵):`t!merc 餅乾大廚`\n例子2(裝備):`t!merc 養好的鍋子`\n例子3(技能):`t!merc 魚肉大餐`")
    else:
        cardname=cardname.replace('_',' ')
        find=[]
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
        elif len(find)>24:
            async def callback_allcards(interaction):
                await interaction.response.edit_message(content="已發送至私人訊息",view=None)
                for data in find:
                        embed,view=embed_m(data,lang)
                        await msg.author.send(embed=embed,view=view)
            button=Button(style=ButtonStyle.success,label="發送所有卡牌至私人訊息")
            button.callback=callback_allcards
            view=View()
            view.add_item(button)
            await msg.reply("由於數量過多，請更改關鍵字縮小範圍。",view=view)
        else:
            options=[]
            options.append(SelectOption(label="全部發送到私人訊息",value="-1",description="可搭配 t!id 指令"))
            for i,data in enumerate(find):
                text=""
                if 'text' in data:text=change_text(data["text"][lang]).replace("*","").replace("[x]","")
                if len(text)>95:text=text[0:94]+"..."
                options.append(SelectOption(label=f'{data["name"][lang]}({data["dbfId"]},{data["id"]})',value=str(i),description=text))
            select=Select(min_values=1,max_values=1,options=options)
            async def select_callback(interaction):
                if int(dict(interaction.data)['values'][0])==-1:
                    await interaction.response.edit_message(content="已發送至私人訊息",view=None)
                    for data in find:
                        embed,view=embed_m(data,lang)
                        await msg.author.send(embed=embed,view=view)
                else:
                    embed,view=embed_m(find[int(dict(interaction.data)['values'][0])],lang)
                    await interaction.response.edit_message(content="",embed=embed,view=view)
            select.callback=select_callback
            view=View()
            view.add_item(select)
            await msg.reply("選擇你想找的卡牌",view=view)

@bot.command()
async def bg(msg,cardname=None,lang="zhTW"):
    if cardname==None:
        await msg.reply("該指令使用方法:\"t!bg 戰場卡牌 語言(選填)\"\n例子:`t!bg 餅乾大廚`")
    else:
        cardname=cardname.replace('_',' ')
        find=[]
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
        elif len(find)>24:
            async def callback_allcards(interaction):
                await interaction.response.edit_message(content="已發送至私人訊息",view=None)
                for data in find:
                        embed,view=embed_bg(data,lang)
                        await msg.author.send(embed=embed,view=view)
            button=Button(style=ButtonStyle.success,label="發送所有卡牌至私人訊息")
            button.callback=callback_allcards
            view=View()
            view.add_item(button)
            await msg.reply("由於數量過多，請更改關鍵字縮小範圍。",view=view)
        else:
            options=[]
            options.append(SelectOption(label="全部發送到私人訊息",value="-1",description="可搭配 t!id 指令"))
            for i,data in enumerate(find):
                text=""
                if 'text' in data:text=change_text(data["text"][lang]).replace("*","").replace("[x]","")
                if len(text)>95:text=text[0:94]+"..."
                options.append(SelectOption(label=f'{data["name"][lang]}({data["dbfId"]},{data["id"]})',value=str(i),description=text))
            select=Select(min_values=1,max_values=1,options=options)
            async def select_callback(interaction):
                if int(dict(interaction.data)['values'][0])==-1:
                    await interaction.response.edit_message(content="已發送至私人訊息",view=None)
                    for data in find:
                        embed,view=embed_bg(data,lang)
                        await msg.author.send(embed=embed,view=view)
                else:
                    embed,view=embed_bg(find[int(dict(interaction.data)['values'][0])],lang)
                    await interaction.response.edit_message(content="",embed=embed,view=view)
            select.callback=select_callback
            view=View()
            view.add_item(select)
            await msg.reply("選擇你想找的卡牌",view=view)

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
        if dict(interaction.data)['custom_id']=="0":
            embed,view=deck_embed(msg,deckcode,deckname,lang,1)
            await interaction.response.edit_message(embed=embed,view=view)
        elif dict(interaction.data)['custom_id']=="1":
            embed,view=deck_embed(msg,deckcode,deckname,lang,0)
            await interaction.response.edit_message(embed=embed,view=view)
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
        await msg.reply("該指令使用方法:\"t!deck 牌組代碼 牌組名稱(選填) \"\n例子1(無套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA`\n例子2(有套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA 無限潛行`")
    else:
        embed,view=deck_embed(msg,deckcode,deckname,lang,0)
        await msg.reply(embed=embed,view=view)
        if deckname!=None:
            await msg.reply(f"###{deckname}\n{deckcode}\n# 若要使用此套牌，請先複製此訊息，然後在爐石戰記中建立一副新的套牌")
        else:
            await msg.reply(f"{deckcode}\n# 若要使用此套牌，請先複製此訊息，然後在爐石戰記中建立一副新的套牌")





DCTOKEN=env['DISCORD_BOT_SECRET']
#loop
if __name__=="__main__":
    bot.run(DCTOKEN)
