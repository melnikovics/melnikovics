from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np, os, math, random

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 700, 200
FR = 30
BG = (10,12,18)
TEXT_COLOR = (220,220,220)
ACCENT_COLOR = (90,150,255)

def make_professional_header(filename):
    frames = []
    for t in range(FR):
        im = Image.new("RGB", (W,H), BG)
        d  = ImageDraw.Draw(im)

        # Add subtle grid lines
        for i in range(0, W, 20):
            alpha = 0.1 + 0.05 * math.sin(2*math.pi*t/FR + i/W)
            color = (int(ACCENT_COLOR[0]*alpha), int(ACCENT_COLOR[1]*alpha), int(ACCENT_COLOR[2]*alpha))
            d.line([(i, 0), (i, H)], fill=color, width=1)
        
        for i in range(0, H, 20):
            alpha = 0.1 + 0.05 * math.cos(2*math.pi*t/FR + i/H)
            color = (int(ACCENT_COLOR[0]*alpha), int(ACCENT_COLOR[1]*alpha), int(ACCENT_COLOR[2]*alpha))
            d.line([(0, i), (W, i)], fill=color, width=1)

        # Add text with subtle animation
        try:
            f_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
            f_small = ImageFont.truetype("DejaVuSans.ttf", 20)
        except:
            f_big = ImageFont.load_default()
            f_small = ImageFont.load_default()
        
        # Main text with subtle zoom effect
        scale = 1 + 0.02 * math.sin(2*math.pi*t/FR)
        text = "Janis Melnikovics"
        
        # Draw text shadow
        bbox = d.textbbox((0, 0), text, font=f_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - tw//2 + 2, H//2 - th//2 + 2), text, fill=(0,0,0,100), font=f_big)
        d.text((W//2 - tw//2, H//2 - th//2), text, fill=TEXT_COLOR, font=f_big)
        
        # Subtitle
        subtitle = "Automate | Innovate"
        bbox = d.textbbox((0, 0), subtitle, font=f_small)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - sw//2, H//2 + 20), subtitle, fill=ACCENT_COLOR, font=f_small)

        frames.append(np.array(im))
    
    # Much slower animation with longer duration between frames
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.5, loop=0)

make_professional_header("control_room_glitch.gif")
print("Professional header GIF created in", OUT_DIR)