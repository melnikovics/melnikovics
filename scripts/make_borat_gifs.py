from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np, os, math, random

OUT_DIR = os.path.join("assets","fun")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 360, 200
FR = 16
BG = (10,12,18)
YELLOW = (255,230,120)
CYAN = (90,200,250)
PINK = (255,120,180)
GREEN = (130,230,130)
ORANGE = (255,170,80)
MOUSTACHE = (35,35,35)

def make_gif(filename, title, subtitle):
    frames = []
    for t in range(FR):
        im = Image.new("RGB", (W,H), BG)
        d  = ImageDraw.Draw(im)

        # confetti + subtle wave
        random.seed(1337+t*11)
        for _ in range(70):
            x = random.randint(0, W-1)
            y = (random.randint(0, H-1) + int(8*math.sin(2*math.pi*t/FR))) % H
            s = random.randint(2,4)
            d.rectangle([x,y,x+s,y+s], fill=random.choice([CYAN,PINK,GREEN,ORANGE,YELLOW]))

        # iconic moustache (two arcs)
        cx, cy, r = W//2, H//2 + 18, 44
        d.pieslice([cx - r*2, cy - r, cx, cy + r], 25, 155, fill=MOUSTACHE)
        d.pieslice([cx, cy - r, cx + r*2, cy + r], 205, 335, fill=MOUSTACHE)

        # fonts
        try:
            f_big   = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
            f_small = ImageFont.truetype("DejaVuSans.ttf", 16)
        except:
            f_big = f_small = ImageFont.load_default()

        # bounce
        dy = int(2*math.sin(2*math.pi*t/FR))
        
        # Use textbbox instead of textsize for newer Pillow versions
        bbox = d.textbbox((0, 0), title, font=f_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - tw//2, 34+dy), title, fill=YELLOW, font=f_big)
        
        bbox = d.textbbox((0, 0), subtitle, font=f_small)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - sw//2, 76+dy), subtitle, fill=(220,220,220), font=f_small)

        frames.append(np.array(im))
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.08, loop=0)

items = [
    ("borat_very_nice.gif",     "Very nice!",       "High five!"),
    ("borat_great_success.gif", "Great success!",   "Technology!"),
    ("borat_high_five.gif",     "High five!",       "Respect."),
    ("borat_king_castle.gif",   "King of the castle!", "Wow-wow-wee-wah!")
]
for fn, t1, t2 in items:
    make_gif(fn, t1, t2)
print("GIFs created in", OUT_DIR)