from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np, os, math, random

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 700, 200
FR = 40
BG = (8, 10, 20)
NODE_COLOR = (60, 180, 250)
CONNECTION_COLOR = (30, 120, 200)
TEXT_COLOR = (220, 230, 255)
ACCENT_COLOR = (100, 220, 255)

def make_ai_header(filename):
    frames = []
    nodes = []
    
    # Initialize nodes with random positions
    for _ in range(15):
        x = random.randint(20, W-20)
        y = random.randint(20, H-60)
        nodes.append([x, y, random.uniform(0, 2*math.pi)])
    
    for t in range(FR):
        im = Image.new("RGB", (W,H), BG)
        d  = ImageDraw.Draw(im)
        
        # Draw neural network connections
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                dx = nodes[i][0] - nodes[j][0]
                dy = nodes[i][1] - nodes[j][1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Only draw connections for nearby nodes
                if distance < 120:
                    alpha = max(0, 1 - distance/120)
                    color = (int(CONNECTION_COLOR[0]*alpha*0.3), 
                            int(CONNECTION_COLOR[1]*alpha*0.3), 
                            int(CONNECTION_COLOR[2]*alpha*0.3))
                    d.line([(nodes[i][0], nodes[i][1]), (nodes[j][0], nodes[j][1])], 
                          fill=color, width=1)
        
        # Draw nodes with pulsing effect
        for i, node in enumerate(nodes):
            pulse = 0.7 + 0.3 * math.sin(2*math.pi*t/FR + node[2])
            size = 4 + 2 * pulse
            color = (int(NODE_COLOR[0]*pulse), int(NODE_COLOR[1]*pulse), int(NODE_COLOR[2]*pulse))
            d.ellipse([node[0]-size, node[1]-size, node[0]+size, node[1]+size], 
                     fill=color, outline=ACCENT_COLOR, width=1)
            
            # Update node positions slightly
            node[0] = max(20, min(W-20, node[0] + 0.3 * math.sin(node[2] + t*0.1)))
            node[1] = max(20, min(H-60, node[1] + 0.3 * math.cos(node[2] + t*0.1)))
        
        # Add text with subtle animation
        try:
            f_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
            f_small = ImageFont.truetype("DejaVuSans.ttf", 20)
        except:
            f_big = ImageFont.load_default()
            f_small = ImageFont.load_default()
        
        # Main text with subtle glow effect
        text = "Janis Melnikovics"
        bbox = d.textbbox((0, 0), text, font=f_big)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Draw text glow
        for i in range(3):
            alpha = 0.2 - 0.05 * i
            glow_color = (int(ACCENT_COLOR[0]*alpha), int(ACCENT_COLOR[1]*alpha), int(ACCENT_COLOR[2]*alpha))
            d.text((W//2 - tw//2 - i, H//2 - th//2 - i), text, fill=glow_color, font=f_big)
            d.text((W//2 - tw//2 + i, H//2 - th//2 + i), text, fill=glow_color, font=f_big)
        
        d.text((W//2 - tw//2, H//2 - th//2), text, fill=TEXT_COLOR, font=f_big)
        
        # Subtitle with circuit board effect
        subtitle = "AI Automation Engineer"
        bbox = d.textbbox((0, 0), subtitle, font=f_small)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((W//2 - sw//2, H//2 + 25), subtitle, fill=ACCENT_COLOR, font=f_small)

        frames.append(np.array(im))
    
    # Slow, smooth animation
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.3, loop=0)

make_ai_header("ai_neural_header.gif")
print("AI-themed header GIF created in", OUT_DIR)