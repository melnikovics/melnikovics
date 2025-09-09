from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np, os, math, random

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 700, 200
FR = 50
BG = (10, 15, 25)
PRIMARY_COLOR = (40, 150, 255)
ACCENT_COLOR = (100, 220, 255)
TEXT_COLOR = (240, 245, 255)
GLOW_COLOR = (180, 230, 255)

def make_stunning_header(filename):
    frames = []
    circles = []
    lines = []
    
    # Initialize animated elements
    for _ in range(15):
        x = random.uniform(20, W-20)
        y = random.uniform(20, H-40)
        size = random.uniform(2, 8)
        speed = random.uniform(0.02, 0.08)
        circles.append([x, y, size, speed, random.uniform(0, 2*math.pi)])
    
    for _ in range(12):
        x1 = random.uniform(0, W)
        y1 = random.uniform(0, H)
        x2 = x1 + random.uniform(-50, 50)
        y2 = y1 + random.uniform(-50, 50)
        lines.append([x1, y1, x2, y2, random.uniform(0.02, 0.06)])
    
    for t in range(FR):
        im = Image.new("RGB", (W,H), BG)
        d  = ImageDraw.Draw(im)
        
        # Draw subtle animated lines with gradient
        for line in lines:
            x1, y1, x2, y2, speed = line
            # Animate line positions
            line[0] += math.sin(t * speed) * 0.5
            line[2] += math.cos(t * speed) * 0.5
            
            # Draw gradient line
            steps = 20
            for i in range(steps):
                ratio = i / steps
                x = x1 + (x2 - x1) * ratio
                y = y1 + (y2 - y1) * ratio
                alpha = math.sin(ratio * math.pi) * 0.3  # Peak in middle
                color = (int(PRIMARY_COLOR[0] * alpha), 
                        int(PRIMARY_COLOR[1] * alpha), 
                        int(PRIMARY_COLOR[2] * alpha))
                d.ellipse([x-1, y-1, x+1, y+1], fill=color)
        
        # Draw pulsing circles with glow effect
        for circle in circles:
            x, y, size, speed, phase = circle
            pulse = 0.7 + 0.3 * math.sin(phase + t * speed)
            
            # Draw glow
            for glow in range(3, 0, -1):
                glow_alpha = 0.2 * glow * pulse
                glow_color = (int(GLOW_COLOR[0] * glow_alpha), 
                             int(GLOW_COLOR[1] * glow_alpha), 
                             int(GLOW_COLOR[2] * glow_alpha))
                d.ellipse([x-size*glow*0.7, y-size*glow*0.7, 
                          x+size*glow*0.7, y+size*glow*0.7], 
                         fill=glow_color)
            
            # Draw main circle
            color = (int(PRIMARY_COLOR[0] * pulse), 
                    int(PRIMARY_COLOR[1] * pulse), 
                    int(PRIMARY_COLOR[2] * pulse))
            d.ellipse([x-size*pulse, y-size*pulse, 
                      x+size*pulse, y+size*pulse], 
                     fill=color)
            
            # Update phase
            circle[4] += 0.05
        
        # Draw tech-inspired text with subtle effects
        try:
            f_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 38)
            f_small = ImageFont.truetype("DejaVuSans.ttf", 22)
        except:
            f_big = ImageFont.load_default()
            f_small = ImageFont.load_default()
        
        # Main text with subtle animation
        text = "Janis Melnikovics"
        bbox = d.textbbox((0, 0), text, font=f_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Text position animation
        text_offset = 2 * math.sin(t * 0.1)
        
        # Draw text shadow/glow
        for i in range(3, 0, -1):
            alpha = 0.1 * i
            glow_color = (int(ACCENT_COLOR[0] * alpha), 
                         int(ACCENT_COLOR[1] * alpha), 
                         int(ACCENT_COLOR[2] * alpha))
            d.text((W//2 - tw//2 + text_offset + i*0.5, H//2 - th//2 + i*0.5), 
                  text, fill=glow_color, font=f_big)
        
        # Draw main text
        d.text((W//2 - tw//2 + text_offset, H//2 - th//2), 
              text, fill=TEXT_COLOR, font=f_big)
        
        # Subtitle with data stream effect
        subtitle = "Power Platform Builder & Automation Engineer"
        bbox = d.textbbox((0, 0), subtitle, font=f_small)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Animate subtitle with subtle effect
        subtitle_offset = 1 * math.sin(t * 0.15)
        d.text((W//2 - sw//2 + subtitle_offset, H//2 + 30), 
              subtitle, fill=ACCENT_COLOR, font=f_small)

        frames.append(np.array(im))
    
    # Smooth animation
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.15, loop=0)

make_stunning_header("stunning_header.gif")
print("Stunning header GIF created in", OUT_DIR)