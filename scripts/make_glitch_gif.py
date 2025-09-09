from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np, os, math, random

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 700, 200
FR = 20
BG = (10,12,18)
TEXT_COLOR = (220,220,220)
GLITCH_COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0)]

def make_glitch_gif(filename):
    frames = []
    for t in range(FR):
        im = Image.new("RGB", (W,H), BG)
        d  = ImageDraw.Draw(im)

        # Create glitch effect
        for _ in range(20):
            x = random.randint(0, W-1)
            y = random.randint(0, H-1)
            w = random.randint(5, 50)
            h = random.randint(1, 3)
            color = random.choice(GLITCH_COLORS)
            d.rectangle([x, y, x+w, y+h], fill=color)
        
        # Add static lines
        for i in range(0, H, 4):
            if random.random() > 0.7:
                d.line([(0, i), (W, i)], fill=(50,50,50), width=1)

        # Add text with glitch effect
        try:
            f_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        except:
            f_big = ImageFont.load_default()
        
        # Main text with slight movement
        dy = int(3*math.sin(2*math.pi*t/FR))
        text = "Janis Melnikovics"
        bbox = d.textbbox((0, 0), text, font=f_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - tw//2 + dy, H//2 - th//2), text, fill=TEXT_COLOR, font=f_big)
        
        # Subtitle
        try:
            f_small = ImageFont.truetype("DejaVuSans.ttf", 20)
        except:
            f_small = ImageFont.load_default()
        
        subtitle = "Automate | Innovate"
        bbox = d.textbbox((0, 0), subtitle, font=f_small)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - sw//2, H//2 + 20), subtitle, fill=TEXT_COLOR, font=f_small)

        frames.append(np.array(im))
    # Slow down the animation by increasing the duration between frames
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.2, loop=0)

make_glitch_gif("control_room_glitch.gif")
print("Glitch GIF created in", OUT_DIR)