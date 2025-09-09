from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np, os, math, random

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 700, 200
FR = 40
BG = (15, 20, 30)
ACCENT_COLOR = (60, 150, 255)
TEXT_COLOR = (230, 240, 255)
HIGHLIGHT_COLOR = (100, 200, 255)

def make_professional_header(filename):
    frames = []
    particles = []
    
    # Initialize subtle particles
    for _ in range(20):
        x = random.uniform(0, W)
        y = random.uniform(0, H)
        vx = random.uniform(-0.3, 0.3)
        vy = random.uniform(-0.3, 0.3)
        size = random.uniform(1, 2)
        particles.append([x, y, vx, vy, size])
    
    for t in range(FR):
        im = Image.new("RGB", (W,H), BG)
        d  = ImageDraw.Draw(im)
        
        # Draw subtle grid lines
        grid_alpha = 0.05 + 0.03 * math.sin(t * 0.2)
        grid_color = (int(ACCENT_COLOR[0] * grid_alpha), 
                     int(ACCENT_COLOR[1] * grid_alpha), 
                     int(ACCENT_COLOR[2] * grid_alpha))
        
        for i in range(0, W, 30):
            d.line([(i, 0), (i, H)], fill=grid_color, width=1)
        for i in range(0, H, 30):
            d.line([(0, i), (W, i)], fill=grid_color, width=1)
        
        # Update and draw subtle particles
        for p in particles:
            p[0] += p[2]
            p[1] += p[3]
            
            # Wrap around edges
            if p[0] < 0: p[0] = W
            if p[0] > W: p[0] = 0
            if p[1] < 0: p[1] = H
            if p[1] > H: p[1] = 0
            
            # Subtle pulsing
            pulse = 0.7 + 0.3 * math.sin(t * 0.1 + p[0] * 0.01)
            color = (int(ACCENT_COLOR[0] * pulse * 0.7), 
                    int(ACCENT_COLOR[1] * pulse * 0.7), 
                    int(ACCENT_COLOR[2] * pulse * 0.7))
            d.ellipse([p[0]-p[4]*pulse, p[1]-p[4]*pulse, 
                      p[0]+p[4]*pulse, p[1]+p[4]*pulse], 
                     fill=color)
        
        # Draw professional text
        try:
            f_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
            f_small = ImageFont.truetype("DejaVuSans.ttf", 20)
        except:
            f_big = ImageFont.load_default()
            f_small = ImageFont.load_default()
        
        # Main text with subtle highlight
        text = "Janis Melnikovics"
        bbox = d.textbbox((0, 0), text, font=f_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Subtle text highlight effect
        highlight_pulse = 0.8 + 0.2 * math.sin(t * 0.15)
        highlight_color = (int(HIGHLIGHT_COLOR[0] * highlight_pulse), 
                          int(HIGHLIGHT_COLOR[1] * highlight_pulse), 
                          int(HIGHLIGHT_COLOR[2] * highlight_pulse))
        d.text((W//2 - tw//2 + 1, H//2 - th//2 + 1), text, fill=highlight_color, font=f_big)
        d.text((W//2 - tw//2, H//2 - th//2), text, fill=TEXT_COLOR, font=f_big)
        
        # Professional subtitle
        subtitle = "Power Platform Builder & Automation Engineer"
        bbox = d.textbbox((0, 0), subtitle, font=f_small)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - sw//2, H//2 + 25), subtitle, fill=ACCENT_COLOR, font=f_small)

        frames.append(np.array(im))
    
    # Smooth professional animation
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.2, loop=0)

make_professional_header("professional_header.gif")
print("Professional header GIF created in", OUT_DIR)