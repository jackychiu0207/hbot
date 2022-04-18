from PIL import ImageFont
from PIL import ImageDraw 
from PIL import Image
i_tem=Image.open("中立.png")
draw = ImageDraw.Draw(i_tem)
numfont = ImageFont.truetype("Number_font.ttf",100)
mana=input("mana:")
x,y=40-((len(mana)-1)*25),-10
draw.text((x -3, y),text=mana,fill=(1,1,1),font=numfont)
draw.text((x + 3, y),text=mana,fill=(1,1,1),font=numfont)
draw.text((x, y - 3),text=mana,fill=(1,1,1),font=numfont)
draw.text((x, y + 3),text=mana,fill=(1,1,1),font=numfont)
draw.text((x - 3, y - 3),text=mana,fill=(1,1,1),font=numfont)
draw.text((x + 3, y - 3),text=mana,fill=(1,1,1),font=numfont)
draw.text((x - 3, y + 3),text=mana,fill=(1,1,1),font=numfont)
draw.text((x + 3, y + 3),text=mana,fill=(1,1,1),font=numfont)
draw.text(xy=(x,y),text=mana,fill=(255,255,255),font=numfont)
i_tem.save('test.png','png')