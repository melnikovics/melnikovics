from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np, os, math, random

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 700, 200
FR = 60
BG = (5, 5, 15)
NODE_CORE = (100, 200, 255)
NODE_GLOW = (180, 230, 255)
MATRIX_COLOR = (0, 200, 100)
TEXT_COLOR = (240, 245, 255)
ACCENT_COLOR = (120, 240, 255)

def make_futuristic_header(filename):
    frames = []
    nodes = []
    matrix_chars = []
    
    # Initialize neural network nodes
    for _ in range(20):
        x = random.uniform(30, W-30)
        y = random.uniform(30, H-70)
        pulse_speed = random.uniform(0.05, 0.15)
        nodes.append([x, y, pulse_speed, random.uniform(0, 2*math.pi)])
    
    # Initialize matrix code characters
    for _ in range(80):
        char = random.choice("01ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        x = random.uniform(0, W)
        y = random.uniform(0, H)
        speed = random.uniform(0.5, 2)
        matrix_chars.append([char, x, y, speed])
    
    for t in range(FR):
        im = Image.new("RGB", (W,H), BG)
        d  = ImageDraw.Draw(im)
        
        # Draw matrix code rain
        for i, char_data in enumerate(matrix_chars):
            char, x, y, speed = char_data
            # Move character down
            char_data[2] += speed
            if char_data[2] > H + 20:
                char_data[2] = -20
                char_data[0] = random.choice("01ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            
            # Fade effect based on position
            alpha = max(0, min(1, 1 - (char_data[2] + 20) / (H + 40)))
            brightness = int(255 * alpha)
            color = (0, int(min(255, brightness * 0.8)), int(min(255, brightness)))
            try:
                f_small = ImageFont.truetype("DejaVuSans-Bold.ttf", 14)
            except:
                f_small = ImageFont.load_default()
            d.text((char_data[1], char_data[2]), char, fill=color, font=f_small)
        
        # Draw neural network with pulsing nodes
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                dx = nodes[i][0] - nodes[j][0]
                dy = nodes[i][1] - nodes[j][1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Draw connections with gradient effect
                if distance < 100:
                    alpha = max(0, 1 - distance/100)
                    # Create gradient along the connection line
                    steps = 10
                    for s in range(steps):
                        ratio = s / steps
                        x = nodes[i][0] + (nodes[j][0] - nodes[i][0]) * ratio
                        y = nodes[i][1] + (nodes[j][1] - nodes[i][1]) * ratio
                        local_alpha = alpha * math.sin(ratio * math.pi)  # Peak in the middle
                        color = (int(NODE_CORE[0]*local_alpha*0.3), 
                                int(NODE_CORE[1]*local_alpha*0.3), 
                                int(NODE_CORE[2]*local_alpha*0.3))
                        d.ellipse([x-1, y-1, x+1, y+1], fill=color)
        
        # Draw pulsing nodes with glow effect
        for node in nodes:
            pulse = 0.7 + 0.3 * math.sin(node[3] + t * node[2])
            size = 3 + 2 * pulse
            
            # Draw glow
            for glow in range(3, 0, -1):
                glow_alpha = 0.2 * glow
                glow_color = (int(NODE_GLOW[0]*glow_alpha), 
                             int(NODE_GLOW[1]*glow_alpha), 
                             int(NODE_GLOW[2]*glow_alpha))
                d.ellipse([node[0]-size*glow*0.5, node[1]-size*glow*0.5, 
                          node[0]+size*glow*0.5, node[1]+size*glow*0.5], 
                         fill=glow_color)
            
            # Draw core
            d.ellipse([node[0]-size, node[1]-size, node[0]+size, node[1]+size], 
                     fill=NODE_CORE)
            
            # Update node pulse phase
            node[3] += 0.05
        
        # Draw futuristic text with holographic effect
        try:
            f_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
            f_small = ImageFont.truetype("DejaVuSans.ttf", 20)
        except:
            f_big = ImageFont.load_default()
            f_small = ImageFont.load_default()
        
        # Main text with holographic effect
        text = "JANIS MELNIKOVICS"
        bbox = d.textbbox((0, 0), text, font=f_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Draw multiple layers for holographic effect
        for layer in range(5):
            offset = layer * 0.5
            alpha = 0.15 * (5 - layer)
            color = (int(ACCENT_COLOR[0]*alpha), 
                    int(ACCENT_COLOR[1]*alpha), 
                    int(ACCENT_COLOR[2]*alpha))
            d.text((W//2 - tw//2 + offset, H//2 - th//2 + offset), text, fill=color, font=f_big)
        
        # Draw main text
        d.text((W//2 - tw//2, H//2 - th//2), text, fill=TEXT_COLOR, font=f_big)
        
        # Subtitle with scanning line effect
        subtitle = "DIGITAL ARCHITECT & FUTURE ENGINEER"
        bbox = d.textbbox((0, 0), subtitle, font=f_small)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Draw scanning line
        scan_pos = int((t / FR) * (sw + 20)) - 10
        if 0 <= scan_pos <= sw:
            d.line([(W//2 - sw//2 + scan_pos, H//2 + 25), 
                   (W//2 - sw//2 + scan_pos, H//2 + 25 + sh)], 
                  fill=ACCENT_COLOR, width=2)
        
        d.text((W//2 - sw//2, H//2 + 25), subtitle, fill=ACCENT_COLOR, font=f_small)

        frames.append(np.array(im))
    
    # Smooth, futuristic animation
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.15, loop=0)

make_futuristic_header("futuristic_header.gif")
print("Futuristic header GIF created in", OUT_DIR)