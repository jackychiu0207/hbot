#2022/4/3 17:34
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

def openjson():
    global cardlib,cardlibm,f,fm
    try:
        with open('cards.json') as f:
            cardlib = json.load(f)
        with open('mercenaries.json') as fm:
            cardlibm = json.load(fm)
    except:
        return False
getjson()
openjson()

@bot.command()
async def reloadjson(msg):
    try:
        f.close()
        fm.close()
        os.remove('cards.json')
        os.remove('mercenaries.json')
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
    embed = discord.Embed(title="指令列表",description="dbfId及id說明:dbfId為純數字、id為文字+數字。\n使用 使用多數指令會將dbfId及id寫在左下方，以逗號分隔;\n**t!deck** 指令則會將dbfId及id寫在卡片名稱後方括號內，以逗號分隔;\n在爐石戰記官網(hsreplay)的卡牌庫中點開一張牌後，網址會變為`https://playhearthstone.com/zh-tw/cards/...(https://hsreplay.net/cards/...)`，「...」中數字的部分即為dbfId。\n指令中語言參數皆為選填，常見zhTW(預設)、zhCN、enUS …\n",color=0xff0000)
    embed.add_field(name="t!id",value="使用方法:\"t!id dbfId或id 語言(選填)\"\n例子1(使用dbfId):`t!id 38833`\n例子2(使用id):`t!id OG_272`", inline=False)
    embed.add_field(name="t!card",value="使用方法:\"t!card 卡牌名稱 語言(選填)\"\n例子:`t!card 暮光召喚師`", inline=False)
    embed.add_field(name="t!deck",value="使用方法:\"t!deck 牌組代碼 牌組名稱(選填) \"\n例子1(無套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA`\n例子2(有套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA 無限潛行`", inline=False)
    embed.add_field(name="t!merc",value="使用方法:\"t!merc 傭兵、裝備、技能名稱 語言(選填)\"\n例子1(傭兵):`t!merc 餅乾大廚`\n例子2(裝備):`t!merc 養好的鍋子`\n例子3(技能):`t!merc 魚肉大餐`", inline=False)
    await msg.reply(embed=embed)


#def
def get_token():
    BZTOKEN = os.environ['BZTOKEN']
    BZSECRET = os.environ['BZSECRET']
    data = {'grant_type':'client_credentials'}
    response = requests.post('https://apac.battle.net/oauth/token', data=data, auth=(BZTOKEN, BZSECRET))
    token=json.loads(response.text)['access_token']
    return token

def change_text(text:str):
    tlist=[['\n',''],['<b>','**'],['</b>','**'],['<i>','*'],['</i>','*'],["。","。\n"],['****',""]]
    for txt in tlist:
        if txt[0] in text:text=text.replace(txt[0],txt[1])
    return(text)





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


#cmds


@bot.command()
async def id(msg,cardid=None,lang="zhTW"):
    if cardid==None:
        await msg.reply("該指令使用方法:\"t!id dbfId或id 語言(選填)\"\n例子1(使用dbfId):`t!id 38833`\n例子2(使用id):`t!id OG_272`")
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
            title=data['name'][lang]
            text=""
            if 'text' in data:text+=change_text(data["text"][lang])+"\n"
            if 'flavor' in data:text+=change_text(data['flavor'][lang])
            imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".png"
            cardview=f"https://playhearthstone.com/cards/"+str(data["dbfId"])
            if data["set"]=="BATTLEGROUNDS":
                token=get_token()
                bzlang=lang[0:2]+"_"+lang[2:4]
                url=f'https://tw.api.blizzard.com/hearthstone/cards/{data["dbfId"]}?locale={bzlang}&gameMode=battlegrounds&access_token={token}'
                cardview=f"https://playhearthstone.com/battlegrounds/"+str(data["dbfId"])
                if 'battlegroundsBuddyDbfId' in data:
                    text+="\n夥伴dbfId:"+str(data['battlegroundsBuddyDbfId'])
                try:
                    if "battlegroundsNormalDbfId" in data:
                        imgurl=json.loads(requests.request('GET',url).text)['battlegrounds']['imageGold']
                    else:
                        imgurl=json.loads(requests.request('GET',url).text)['battlegrounds']['image']
                except:pass
            elif data["set"]=="LETTUCE":cardview=f"https://playhearthstone.com/zh-tw/mercenaries/"+str(data["dbfId"])
            if requests.request('GET',imgurl).status_code==404:
                imgurl=f"https://art.hearthstonejson.com/v1/512x/"+data["id"]+".jpg"
                if requests.request('GET',imgurl).status_code==404:
                    imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
                    text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
            embed = discord.Embed(title=title,url=cardview,description=text, color=0xff0000)
            embed.set_image(url=imgurl)
            embed.set_footer(text=str(data["dbfId"])+","+data["id"])
            await msg.reply(embed=embed)
        else:await msg.reply("查無此卡!")

@bot.command()
async def card(msg,cardname=None,lang="zhTW"):
    if cardname==None:
        await msg.reply("該指令使用方法:\"t!card 卡牌名稱 語言(選填)\"\n例子:`t!card 暮光召喚師`")
    else:
        def embed(data:dict):
            title=data['name'][lang]
            text=""
            if 'text' in data:text+=change_text(data["text"][lang])+"\n"
            elif 'flavor' in data:text+=change_text(data['flavor'][lang])
            imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".png"
            cardview=f"https://playhearthstone.com/cards/"+str(data["dbfId"])
            if data["set"]=="BATTLEGROUNDS":
                cardview=f"https://playhearthstone.com/battlegrounds/"+str(data["dbfId"])
                token=get_token()
                bzlang=lang[0:2]+"_"+lang[2:4]
                url=f'https://tw.api.blizzard.com/hearthstone/cards/{data["dbfId"]}?locale={bzlang}&gameMode=battlegrounds&access_token={token}'
                if 'battlegroundsBuddyDbfId' in data:
                    text+="\n夥伴dbfId:"+str(data['battlegroundsBuddyDbfId'])
                try:  
                    if "battlegroundsNormalDbfId" in data:
                        imgurl=json.loads(requests.request('GET',url).text)['battlegrounds']['imageGold']
                    else:
                        imgurl=json.loads(requests.request('GET',url).text)['battlegrounds']['image']
                except:pass
            elif data["set"]=="LETTUCE":cardview=f"https://playhearthstone.com/zh-tw/mercenaries/"+str(data["dbfId"])
            if requests.request('GET',imgurl).status_code==404:
                imgurl=f"https://art.hearthstonejson.com/v1/256x/"+data["id"]+".jpg"
                if requests.request('GET',imgurl).status_code==404:
                    imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
                    text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
            embed = discord.Embed(title=title,url=cardview,description=text, color=0xff0000)
            embed.set_image(url=imgurl)
            embed.set_footer(text=str(data["dbfId"])+","+data["id"])
            return embed
        find=[]
        for data in cardlib:
            if "type" in data:
                if data["type"]!="ENCHANTMENT":
                    if cardname in data["name"][lang]:find.append(data)
                    elif 'text' in data:
                        if cardname in data["text"][lang].replace("\n",""):find.append(data)
        if len(find)==0:await msg.reply("查無卡牌！")
        elif len(find)==1:await msg.reply(embed=embed(find[0]))
        elif len(find)>24:
            async def button_callback(interaction):
              await interaction.response.edit_message(content="已發送至私人訊息",view=None)
              for data in find:
                        await msg.author.send(embed=embed(data))
            button=Button(style=ButtonStyle.success,label="發送所有卡牌至私人訊息")
            button.callback=button_callback
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
                        await msg.author.send(embed=embed(data))
                else:
                    await interaction.response.edit_message(content="",embed=embed(find[int(dict(interaction.data)['values'][0])]),view=None)
            select.callback=select_callback
            view=View()
            view.add_item(select)
            await msg.reply("選擇你想找的卡牌",view=view)



@bot.command()
async def merc(msg,cardname=None,lang="zhTW"):
    if cardname==None:
        await msg.reply("該指令使用方法:\"t!merc 傭兵、裝備、技能名稱 語言(選填)\"\n例子1(傭兵):`t!merc 餅乾大廚`\n例子2(裝備):`t!merc 養好的鍋子`\n例子3(技能):`t!merc 魚肉大餐`")
    else:
        def embed_m(data:dict):
            view=View()
            title=data['name'][lang]
            text=""
            if 'text' in data:text+=change_text(data["text"][lang])+"\n"
            elif 'flavor' in data:text+=change_text(data['flavor'][lang])+"\n"
            imgurl=f"https://art.hearthstonejson.com/v1/render/latest/{lang}/512x/"+data["id"]+".png"
            cardview=f"https://playhearthstone.com/zh-tw/mercenaries/"+str(data["dbfId"])
            if requests.request('GET',imgurl).status_code==404:
                imgurl=f"https://art.hearthstonejson.com/v1/256x/"+data["id"]+".jpg"
                if requests.request('GET',imgurl).status_code==404:
                    imgurl="https://cdn.discordapp.com/attachments/913009861967626310/935811318768885810/PlaceholderCard.png"
                    text+="\n※此卡牌確實存在於爐石戰記中的某個角落，但沒有任何圖片"
            #傭兵子父卡牌功能
            async def select_callback(interaction):
                for data in cardlib:
                    if data["dbfId"]==int(dict(interaction.data)['values'][0]):
                        embed,view=embed_m(data)
                        await interaction.response.edit_message(embed=embed,view=view)
            if data["cost"]==0 and data["type"]=="LETTUCE_ABILITY" and "hideCost" in data:
                for h_data in cardlibm:
                    if "equipment" in h_data:
                        for e_data in h_data["equipment"]:
                            if "tiers" in e_data:
                                for e in e_data["tiers"]:
                                    if e["dbf_id"]==data["dbfId"]:
                                        for ownerdata in cardlib:
                                            if ownerdata["dbfId"]==h_data["defaultSkinDbfId"]:
                                                text+="此為 **"+ownerdata['name'][lang]+"**("+str(ownerdata['dbfId'])+","+str(ownerdata['id'])+") 的裝備。\n"
                                                if len(e_data['tiers'])>1:text+="該裝備其他等級的dbfId:\n"
                                                async def button_callback(interaction):
                                                    for data in cardlib:
                                                        if data["dbfId"]==int(dict(interaction.data)['custom_id']):
                                                            embed,view=embed_m(data)
                                                            await interaction.response.edit_message(embed=embed,view=view)
                                                            break
                                                for otd in e_data['tiers']:
                                                    if otd["dbf_id"]!=data["dbfId"]:
                                                        text+="等級"+str(otd["tier"])+":"+str(otd["dbf_id"])+"\n"
                                                        button=Button(style=ButtonStyle.gray,label="查看等級"+str(otd["tier"]),custom_id=str(otd["dbf_id"]))
                                                        button.callback=button_callback
                                                        view.add_item(button)
                                                button=Button(style=ButtonStyle.success,label="查看傭兵",custom_id=str(ownerdata['dbfId']))
                                                button.callback=button_callback
                                                view.add_item(button)
                                                break
            elif data["cost"]!=0 and data["type"]=="LETTUCE_ABILITY":
                for h_data in cardlibm:
                    if "specializations" in h_data:
                        if len(h_data["specializations"])>0:
                            if "abilities" in h_data["specializations"][0]:
                                for p_data in h_data["specializations"][0]["abilities"]:
                                    if "tiers" in p_data:
                                        for p in p_data["tiers"]:
                                            if p["dbf_id"]==data["dbfId"]:
                                                for ownerdata in cardlib:
                                                    if ownerdata["dbfId"]==h_data["defaultSkinDbfId"]:
                                                        text+="此為 **"+ownerdata['name'][lang]+"**("+str(ownerdata['dbfId'])+","+str(ownerdata['id'])+") 的技能。\n"
                                                        if len(p_data['tiers'])>1:text+="該技能其他等級的dbfId:\n"
                                                        async def button_callback(interaction):
                                                            for data in cardlib:
                                                                if data["dbfId"]==int(dict(interaction.data)['custom_id']):
                                                                    embed,view=embed_m(data)
                                                                    await interaction.response.edit_message(embed=embed,view=view)
                                                                    break
                                                        for otd in p_data['tiers']:
                                                            if otd["dbf_id"]!=data["dbfId"]:
                                                                text+="等級"+str(otd["tier"])+":"+str(otd["dbf_id"])+"\n"
                                                                button=Button(style=ButtonStyle.gray,label="查看等級"+str(otd["tier"]),custom_id=str(otd["dbf_id"]))
                                                                button.callback=button_callback
                                                                view.add_item(button)
                                                        button=Button(style=ButtonStyle.success,label="查看傭兵",custom_id=str(ownerdata['dbfId']))
                                                        button.callback=button_callback
                                                        view.add_item(button)
                                                        break
            elif data["type"]=="MINION":
                for h_data in cardlibm:
                    if data["dbfId"] in h_data["skinDbfIds"]:
                        text+="(下方可選擇查看造型、裝備、技能)\n"
                        if "skinDbfIds" in h_data:
                            skins=[]
                            for i,skin in enumerate(h_data["skinDbfIds"],1):
                                skins.append(SelectOption(label=f"造型{i}",value=str(skin),description=skin))
                            select_s=Select(placeholder="選擇要查看的造型",options=skins,min_values=1,max_values=1)
                            select_s.callback=select_callback
                            view.add_item(select_s)
                        if "equipment" in h_data:
                            if len(h_data["equipment"])>=1:
                                options_e=[]
                                text+="**該傭兵所有裝備:**\n"
                                for i,e_data in enumerate(h_data["equipment"],1):
                                    for tiers in e_data["tiers"]:
                                        for c_data in cardlib:
                                            if tiers["dbf_id"] == c_data["dbfId"]:
                                                text+=f"裝備{str(i)}等級{tiers['tier']}({c_data['name'][lang]},{c_data['dbfId']})\n"
                                                options_e.append(SelectOption(label=f"{c_data['name'][lang]}({c_data['dbfId']},{c_data['id']})\n",value=str(c_data['dbfId']),description=f"裝備{str(i)}等級{tiers['tier']}"))
                                select_e=Select(placeholder="選擇要查看的裝備",options=options_e,min_values=1,max_values=1)
                                select_e.callback=select_callback
                                view.add_item(select_e)
                        if "specializations" in h_data:
                            if len(h_data["specializations"])>0:
                                if "abilities" in h_data["specializations"][0]:
                                    if len(h_data["equipment"])>=1:
                                        options_p=[]
                                        text+="**該傭兵所有技能:**\n"
                                        for i,p_data in enumerate(h_data["specializations"][0]["abilities"],1):
                                            if "tiers" in p_data: 
                                                for tiers in p_data["tiers"]:
                                                    for c_data in cardlib:
                                                        if tiers["dbf_id"] == c_data["dbfId"]:
                                                            text+=f"技能{str(i)}等級{tiers['tier']}({c_data['name'][lang]},{c_data['dbfId']})\n"
                                                            options_p.append(SelectOption(label=f"{c_data['name'][lang]}({c_data['dbfId']},{c_data['id']})\n",value=str(c_data['dbfId']),description=f"技能{str(i)}等級{tiers['tier']}"))
                                select_p=Select(placeholder="選擇要查看的技能",options=options_p,min_values=1,max_values=1)
                                select_p.callback=select_callback
                                view.add_item(select_p)
                        

                        
                        
                        
                        
                        
                        
                                        

            embed = discord.Embed(title=title,url=cardview,description=text, color=0xff0000)
            embed.set_image(url=imgurl)
            embed.set_footer(text=str(data["dbfId"])+","+data["id"])
            return embed,view
        find=[]
        for data in cardlib:
            if "type" in data and "set" in data:
                if data["type"]!="ENCHANTMENT" and data["set"]=="LETTUCE":
                    if cardname in data["name"][lang]:find.append(data)
                    elif 'text' in data:
                        if cardname in data["text"][lang].replace("\n",""):find.append(data)
        if len(find)==0:await msg.reply("查無卡牌！")
        elif len(find)==1:
            embed,view=embed_m(find[0])
            await msg.reply(embed=embed,view=view)
        elif len(find)>24:
            async def button_callback(interaction):
                await interaction.response.edit_message(content="已發送至私人訊息",view=None)
                for data in find:
                        await msg.author.send(embed=embed_m(data))
            button=Button(style=ButtonStyle.success,label="發送所有卡牌至私人訊息")
            button.callback=button_callback
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
                        embed,view=embed_m(data)
                        await msg.author.send(embed=embed,view=view)
                else:
                    embed,view=embed_m(find[int(dict(interaction.data)['values'][0])])
                    await interaction.response.edit_message(content="",embed=embed,view=view)
            select.callback=select_callback
            view=View()
            view.add_item(select)
            await msg.reply("選擇你想找的卡牌",view=view)



@bot.command()
async def deck(msg,deckcode=None,deckname=None,lang="zhTW"):
    if deckcode==None:
        await msg.reply("該指令使用方法:\"t!deck 牌組代碼 牌組名稱(選填) \"\n例子1(無套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA`\n例子2(有套牌名稱):\n`t!deck AAEBAaIHDpoC+AfpEZfBAt/jArvvAuvwAoSmA6rLA4/OA/bWA4PkA72ABJWfBAi0AcQB7QL1uwLi3QPn3QOS5AP+7gMA 無限潛行`")
    else:
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
                if heroID[5:7]=="01":heroclass="戰士"
                elif heroID[5:7]=="02":heroclass="薩滿"
                elif heroID[5:7]=="03":heroclass="盜賊"
                elif heroID[5:7]=="04":heroclass="聖騎士"
                elif heroID[5:7]=="05":heroclass="獵人"
                elif heroID[5:7]=="06":heroclass="德魯伊"
                elif heroID[5:7]=="07":heroclass="術士"
                elif heroID[5:7]=="08":heroclass="法師"
                elif heroID[5:7]=="09":heroclass="牧師"
                elif heroID[5:7]=="10":heroclass="惡魔獵人"
                else:heroclass="未知"

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
            txt+=str(data["count"]) +"×" +"("+str(data["cost"])+")**"+ data["name"][lang]+ "**(" + str(data["dbfId"])+","+data["id"]+")\n"
            count+=data["count"]
            if "CORE"!=data["set"] and "rarity" in data:
                if data["rarity"]=="COMMON":cost+=40*data["count"]
                elif data["rarity"]=="RARE":cost+=100*data["count"]
                elif data["rarity"]=="EPIC":cost+=400*data["count"]
                elif data["rarity"]=="LEGENDARY":cost+=1600*data["count"]
        embed=discord.Embed(title=deckname, description=f'{mode} 職業:{heroclass}(英雄:{deckhero})\n共{str(count)}張牌\n\n'+txt,url=f'https://playhearthstone.com/zh-tw/deckbuilder?deckcode={deckcode}',color=0xff0000)
        embed.set_thumbnail(url="https://art.hearthstonejson.com/v1/orig/"+heroID+".png")
        embed.set_footer(text="所需塵魔:"+str(cost))
        await msg.reply(embed=embed)
        if deckname!=None:
            await msg.reply(f"###{deckname}\n{deckcode}\n# 若要使用此套牌，請先複製此訊息，然後在爐石戰記中建立一副新的套牌")
        else:
            await msg.reply(f"{deckcode}\n# 若要使用此套牌，請先複製此訊息，然後在爐石戰記中建立一副新的套牌")





DCTOKEN=os.environ['DISCORD_BOT_SECRET']
#loop
if __name__=="__main__":
    keep_alive()
    bot.run(DCTOKEN)

