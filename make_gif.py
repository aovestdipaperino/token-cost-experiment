# -*- coding: utf-8 -*-
# Builds the side-by-side token-cost GIF. Reads en.json/it.json if present
# (produced by run.sh), otherwise falls back to the committed sample numbers.
import json, os
from PIL import Image, ImageDraw, ImageFont

def load(path, default):
    try:
        with open(path) as f: return json.load(f)["usage"]["output_tokens"]
    except Exception: return default
EN = load("en.json", 387); IT = load("it.json", 640)
delta = (IT-EN)/EN*100.0

W,H=1280,720
BG=(0x18,0x18,0x1B); BORDER=(0x3F,0x3F,0x46); WHITE=(0xFA,0xFA,0xFA)
MUTE=(0xA1,0xA1,0xAA); FAINT=(0x71,0x71,0x71); BLUE=(0x60,0xA5,0xFA); CLAY=(0xD9,0x77,0x57); GREEN=(0x4A,0xDE,0x80)
def font(sz,bold=False,mono=False):
    for p in ([ "/System/Library/Fonts/Menlo.ttc"] if mono else
              (["/System/Library/Fonts/Supplemental/Arial Bold.ttf","C:/Windows/Fonts/arialbd.ttf"] if bold
               else ["/System/Library/Fonts/Supplemental/Arial.ttf","C:/Windows/Fonts/arial.ttf"])):
        if os.path.exists(p): return ImageFont.truetype(p,sz)
    return ImageFont.load_default()
f_title=font(44,True); f_sub=font(24); f_num=font(64,mono=True); f_lbl=font(30,True)
f_small=font(20); f_delta=font(40,True); f_foot=font(18,mono=True)
BASE_Y=588; MAXH=285; scale=MAXH/max(EN,IT); BARW=150; CX_EN=440; CX_IT=780
def ease(t): return 1-(1-t)**3
def draw(en_v,it_v,show):
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    d.text((80,54),"Same task, two languages",font=f_title,fill=WHITE)
    d.text((80,116),"Tokens Claude generated for the identical request",font=f_sub,fill=MUTE)
    d.line([(120,BASE_Y),(W-120,BASE_Y)],fill=BORDER,width=2)
    for cx,val,color,lang in [(CX_EN,en_v,BLUE,"English"),(CX_IT,it_v,CLAY,"Italiano")]:
        bh=int(val*scale); y0=BASE_Y-bh
        if bh>0: d.rounded_rectangle([cx-BARW//2,y0,cx+BARW//2,BASE_Y],radius=8,fill=color)
        num=str(int(round(val))); tw=d.textbbox((0,0),num,font=f_num)[2]
        d.text((cx-tw/2,max(150,y0-84)),num,font=f_num,fill=color)
        tw2=d.textbbox((0,0),"tokens",font=f_small)[2]; d.text((cx-tw2/2,max(150,y0-84)+70),"tokens",font=f_small,fill=FAINT)
        lw=d.textbbox((0,0),lang,font=f_lbl)[2]; d.text((cx-lw/2,BASE_Y+18),lang,font=f_lbl,fill=WHITE)
    if show:
        t=f"+{delta:.0f}% more tokens in Italian"; tw=d.textbbox((0,0),t,font=f_delta)[2]
        d.text((W/2-tw/2,150),t,font=f_delta,fill=GREEN)
    d.text((80,H-32),"same meaning, more tokens - measured with claude -p --output-format json",font=f_foot,fill=FAINT)
    return img
frames=[draw(EN*ease(i/34),IT*ease(i/34),False) for i in range(35)]
frames+=[draw(EN,IT,False)]*10 + [draw(EN,IT,True)]*28
frames[0].save("token-cost-en-vs-it.gif",save_all=True,append_images=frames[1:],duration=60,loop=0,disposal=2)
print(f"EN={EN} IT={IT} (+{delta:.0f}%) -> token-cost-en-vs-it.gif")
