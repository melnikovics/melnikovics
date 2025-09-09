from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np, os, math, random

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 700, 150
FR = 40
BG = (10, 15, 25)
PRIMARY_COLOR = (60, 160, 255)
ACCENT_COLOR = (120, 200, 255)
TEXT_COLOR = (240, 245, 255)
GLOW_COLOR = (180, 220, 255)

def make_premium_header(filename):
    frames = []
    particles = []
    
    # Initialize subtle particles
    for _ in range(25):
        x = random.uniform(0, W)
        y = random.uniform(0, H)
        size = random.uniform(0.5, 2)
        speed = random.uniform(0.01, 0.05)
        angle = random.uniform(0, 2*math.pi)
        particles.append([x, y, size, speed, angle])
    
    for t in range(FR):
        im = Image.new("RGB", (W,H), BG)
        d  = ImageDraw.Draw(im)
        
        # Draw subtle particle field
        for p in particles:
            x, y, size, speed, angle = p
            # Update position
            p[0] += math.cos(angle) * speed
            p[1] += math.sin(angle) * speed
            
            # Wrap around edges
            if p[0] < -5: p[0] = W + 5
            if p[0] > W + 5: p[0] = -5
            if p[1] < -5: p[1] = H + 5
            if p[1] > H + 5: p[1] = -5
            
            # Pulsing effect
            pulse = 0.6 + 0.4 * math.sin(t * 0.1 + x * 0.01 + y * 0.01)
            
            # Draw with glow effect
            for glow in range(2, 0, -1):
                glow_alpha = 0.3 * glow * pulse
                glow_color = (int(GLOW_COLOR[0] * glow_alpha), 
                             int(GLOW_COLOR[1] * glow_alpha), 
                             int(GLOW_COLOR[2] * glow_alpha))
                d.ellipse([x-size*glow, y-size*glow, 
                          x+size*glow, y+size*glow], 
                         fill=glow_color)
            
            # Draw main particle
            color = (int(PRIMARY_COLOR[0] * pulse), 
                    int(PRIMARY_COLOR[1] * pulse), 
                    int(PRIMARY_COLOR[2] * pulse))
            d.ellipse([x-size*pulse, y-size*pulse, 
                      x+size*pulse, y+size*pulse], 
                     fill=color)
        
        # Draw premium text with advanced effects
        try:
            f_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
            f_small = ImageFont.truetype("DejaVuSans.ttf", 19)
        except:
            f_big = ImageFont.load_default()
            f_small = ImageFont.load_default()
        
        # Main text with sophisticated glow
        text = "JANIS MELNIKOVICS"
        bbox = d.textbbox((0, 0), text, font=f_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Multi-layer glow effect
        for i in range(5, 0, -1):
            alpha = 0.15 * i
            offset = i * 0.7
            glow_color = (int(ACCENT_COLOR[0] * alpha), 
                         int(ACCENT_COLOR[1] * alpha), 
                         int(ACCENT_COLOR[2] * alpha))
            d.text((W//2 - tw//2 + offset, H//2 - th//2 - 10 + offset), 
                  text, fill=glow_color, font=f_big)
        
        # Main text
        d.text((W//2 - tw//2, H//2 - th//2 - 10), 
              text, fill=TEXT_COLOR, font=f_big)
        
        # Subtitle
        subtitle = "Power Platform Builder & Automation Engineer"
        bbox = d.textbbox((0, 0), subtitle, font=f_small)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Draw subtitle
        d.text((W//2 - sw//2, H//2 + 15), 
              subtitle, fill=ACCENT_COLOR, font=f_small)
        
        # Draw subtle underline with animation
        underline_width = int((t / FR) * sw)
        d.line([(W//2 - sw//2, H//2 + 35), 
               (W//2 - sw//2 + underline_width, H//2 + 35)], 
              fill=PRIMARY_COLOR, width=2)

        frames.append(np.array(im))
    
    # Smooth premium animation
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.15, loop=0)

make_premium_header("premium_header_fixed.gif")
print("Premium header GIF created in", OUT_DIR)