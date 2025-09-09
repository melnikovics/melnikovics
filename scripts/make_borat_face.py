import imageio.v2 as imageio
import numpy as np, os, math

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

def make_borat_face_gif(filename):
    frames = []
    
    # Create 30 frames for smooth animation
    for frame in range(30):
        # Create image
        height = 300
        width = 400
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Fill background with dark blue
        img[:, :] = (20, 25, 40)
        
        # Animation parameters
        time = frame * 0.3
        head_bob = 5 * math.sin(time)
        smile_width = 30 + 10 * math.sin(time * 2)
        eye_blink = max(0, 1 - 5 * abs(math.sin(time * 3)))  # Blink periodically
        
        # Draw face (oval shape)
        center_x, center_y = 200, 150
        for y in range(center_y - 80, center_y + 80):
            for x in range(center_x - 60, center_x + 60):
                # Oval equation
                if ((x - center_x) ** 2) / (60 ** 2) + ((y - center_y) ** 2) / (80 ** 2) <= 1:
                    # Skin tone with slight variation
                    skin_variation = 0.9 + 0.1 * math.sin(time + x * 0.1)
                    img[y, x] = (int(240 * skin_variation), int(220 * skin_variation), int(180 * skin_variation))
        
        # Draw eyes (with blinking effect)
        eye_height = int(8 * eye_blink)
        if eye_height > 0:
            # Left eye
            for y in range(int(center_y - 20 - eye_height/2), int(center_y - 20 + eye_height/2)):
                for x in range(center_x - 25, center_x - 15):
                    img[y, x] = (0, 0, 0)
            # Right eye
            for y in range(int(center_y - 20 - eye_height/2), int(center_y - 20 + eye_height/2)):
                for x in range(center_x + 15, center_x + 25):
                    img[y, x] = (0, 0, 0)
        
        # Draw iconic mustache
        mustache_y = center_y + 5
        for y in range(mustache_y - 15, mustache_y + 15):
            for x in range(center_x - 40, center_x + 40):
                # Mustache shape - two curved sections
                left_curve = ((x - (center_x - 20)) ** 2) / (20 ** 2) + ((y - mustache_y) ** 2) / (15 ** 2) <= 1
                right_curve = ((x - (center_x + 20)) ** 2) / (20 ** 2) + ((y - mustache_y) ** 2) / (15 ** 2) <= 1
                
                if left_curve or right_curve:
                    img[y, x] = (60, 40, 20)  # Brown mustache
        
        # Draw smile (animated width)
        smile_center_y = center_y + 30
        for angle in range(-60, 60):
            rad = np.radians(angle)
            x = int(center_x + smile_width * np.cos(rad))
            y = int(smile_center_y + 15 * np.sin(rad))
            if 0 <= x < width and 0 <= y < height:
                img[y, x] = (255, 100, 100)  # Red smile
        
        # Draw "Very Nice!" text with animation
        text_y_offset = int(10 * math.sin(time * 1.5))
        # We'll represent text with colored rectangles for simplicity
        text_color = (255, 255, 200)  # Light yellow
        for y in range(30 + text_y_offset, 50 + text_y_offset):
            for x in range(150, 250):
                img[y, x] = text_color
        
        frames.append(img)
    
    # Save as GIF
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.15, loop=0)

make_borat_face_gif("borat_face.gif")
print("Borat face GIF created in", OUT_DIR)