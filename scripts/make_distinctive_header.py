from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np, os, math, random

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 700, 200
FR = 50
BG = (12, 15, 25)
PARTICLE_COLOR = (80, 190, 255)
TEXT_COLOR = (230, 240, 255)
ACCENT_COLOR = (120, 230, 255)

def make_distinctive_header(filename):
    frames = []
    particles = []
    
    # Initialize particles with random positions and properties
    for _ in range(30):
        x = random.uniform(0, W)
        y = random.uniform(0, H)
        vx = random.uniform(-0.5, 0.5)
        vy = random.uniform(-0.5, 0.5)
        size = random.uniform(1, 3)
        life = random.uniform(0, 2*math.pi)
        particles.append([x, y, vx, vy, size, life])
    
    for t in range(FR):
        im = Image.new("RGB", (W,H), BG)
        d  = ImageDraw.Draw(im)
        
        # Update and draw particles with proper layering
        for i, p in enumerate(particles):
            # Update particle positions
            p[0] += p[2] + 0.3 * math.sin(p[5] + t*0.1)
            p[1] += p[3] + 0.3 * math.cos(p[5] + t*0.1)
            
            # Wrap around edges
            if p[0] < 0: p[0] = W
            if p[0] > W: p[0] = 0
            if p[1] < 0: p[1] = H
            if p[1] > H: p[1] = 0
            
            # Pulsing effect
            pulse = 0.6 + 0.4 * math.sin(p[5] + t*0.2)
            alpha = int(150 * pulse)
            
            # Draw particle with proper color and transparency
            color = (int(PARTICLE_COLOR[0]*pulse), int(PARTICLE_COLOR[1]*pulse), int(PARTICLE_COLOR[2]*pulse))
            d.ellipse([p[0]-p[4]*pulse, p[1]-p[4]*pulse, p[0]+p[4]*pulse, p[1]+p[4]*pulse], 
                     fill=color)
            
            # Occasionally draw connections between nearby particles
            if t % 5 == 0 and i < len(particles)-1:
                next_p = particles[i+1]
                dx = p[0] - next_p[0]
                dy = p[1] - next_p[1]
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < 80:
                    alpha = max(0, 1 - distance/80) * 50
                    color = (int(PARTICLE_COLOR[0]*alpha/100), 
                            int(PARTICLE_COLOR[1]*alpha/100), 
                            int(PARTICLE_COLOR[2]*alpha/100))
                    d.line([(p[0], p[1]), (next_p[0], next_p[1])], 
                          fill=color, width=1)
        
        # Add text with multiple layers for depth
        try:
            f_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 38)
            f_small = ImageFont.truetype("DejaVuSans.ttf", 22)
        except:
            f_big = ImageFont.load_default()
            f_small = ImageFont.load_default()
        
        # Main text with gradient effect
        text = "Janis Melnikovics"
        bbox = d.textbbox((0, 0), text, font=f_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Draw text with multiple layers for glow effect
        for i in range(5, 0, -1):
            alpha = 0.1 * i
            glow_color = (int(ACCENT_COLOR[0]*alpha), int(ACCENT_COLOR[1]*alpha), int(ACCENT_COLOR[2]*alpha))
            d.text((W//2 - tw//2 - i/2, H//2 - th//2 - i/2), text, fill=glow_color, font=f_big)
        
        d.text((W//2 - tw//2, H//2 - th//2), text, fill=TEXT_COLOR, font=f_big)
        
        # Subtitle with typing effect
        full_subtitle = "Building Digital Solutions"
        # Typing effect - show more characters over time
        chars_to_show = min(len(full_subtitle), int(t * len(full_subtitle) / (FR/2)))
        subtitle = full_subtitle[:chars_to_show] + ("|" if t % 4 < 2 and chars_to_show < len(full_subtitle) else "")
        
        bbox = d.textbbox((0, 0), subtitle, font=f_small)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - sw//2, H//2 + 30), subtitle, fill=ACCENT_COLOR, font=f_small)

        frames.append(np.array(im))
    
    # Smooth animation
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.2, loop=0)

make_distinctive_header("distinctive_header.gif")
print("Distinctive header GIF created in", OUT_DIR)