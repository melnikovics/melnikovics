from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np, os, math, random

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 700, 150
FR = 30
BG = (15, 20, 30)
TEXT_COLOR = (230, 240, 255)
ACCENT_COLOR = (60, 150, 255)

def make_clean_header(filename):
    frames = []
    
    for t in range(FR):
        im = Image.new("RGB", (W,H), BG)
        d  = ImageDraw.Draw(im)
        
        # Draw subtle animated line
        line_progress = (t / FR) * W
        d.line([(0, H-20), (line_progress, H-20)], fill=ACCENT_COLOR, width=2)
        
        # Draw clean text
        try:
            f_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
            f_small = ImageFont.truetype("DejaVuSans.ttf", 18)
        except:
            f_big = ImageFont.load_default()
            f_small = ImageFont.load_default()
        
        # Main text
        text = "Janis Melnikovics"
        bbox = d.textbbox((0, 0), text, font=f_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - tw//2, H//2 - th//2 - 10), text, fill=TEXT_COLOR, font=f_big)
        
        # Subtitle with subtle animation
        subtitle = "Power Platform Builder & Automation Engineer"
        bbox = d.textbbox((0, 0), subtitle, font=f_small)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - sw//2, H//2 + 15), subtitle, fill=ACCENT_COLOR, font=f_small)

        frames.append(np.array(im))
    
    # Smooth animation
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.2, loop=0)

make_clean_header("clean_header.gif")
print("Clean header GIF created in", OUT_DIR)