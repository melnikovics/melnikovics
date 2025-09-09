import imageio.v2 as imageio
import numpy as np, os

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

# Proper Borat-style ASCII art frames
borat_frames = [
    r'''
    ________________
   |                |
   |    ____________|
   |   |   Very     |
   |   |   Nice!    |
   |   |____________|
   |                |
   |        /\      |
   |       /  \     |
   |      /    \    |
   |     |      |   |
   |     |      |   |
   |      \____/    |
   |    ____________|
   |   |  Great     |
   |   |  Success!  |
   |   |____________|
   |________________|
    ''',
    r'''
    ________________
   |                |
   |    ____________|
   |   |   Very     |
   |   |   Nice!    |
   |   |____________|
   |                |
   |        /\      |
   |       /  \     |
   |      /    \    |
   |     |      |   |
   |     |      |   |
   |      \____/    |
   |    ____________|
   |   |  Great     |
   |   |  Success!  |
   |   |____________|
   |________________|
    ''',
    r'''
    ________________
   |                |
   |    ____________|
   |   |   Very     |
   |   |   Nice!    |
   |   |____________|
   |                |
   |        /\      |
   |       /  \     |
   |      /    \    |
   |     |      |   |
   |     |      |   |
   |      \____/    |
   |    ____________|
   |   |  Great     |
   |   |  Success!  |
   |   |____________|
   |________________|
    '''
]

def make_proper_borat_gif(filename):
    frames = []
    
    # Create multiple frames with text animation effects
    for i in range(20):  # 20 frames
        # Create image
        height = 400
        width = 600
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Fill background with dark blue
        img[:, :] = (20, 25, 40)
        
        # Simple animated effect - make text pulse
        pulse = 0.8 + 0.2 * abs(np.sin(i * 0.3))
        
        # For simplicity, we'll just create a static representation
        # In a real implementation, this would render the ASCII art
        
        # Draw a simple representation of Borat's face
        # Head
        for y in range(150, 250):
            for x in range(250, 350):
                if (x-300)**2 + (y-200)**2 < 50**2:
                    img[y, x] = (int(240*pulse), int(220*pulse), int(180*pulse))  # Skin tone
        
        # Mustache
        for y in range(210, 230):
            for x in range(270, 330):
                img[y, x] = (int(60*pulse), int(40*pulse), int(20*pulse))  # Brown mustache
        
        # Eyes
        for y in range(180, 190):
            for x in range(280, 290):
                img[y, x] = (0, 0, 0)  # Left eye
            for x in range(310, 320):
                img[y, x] = (0, 0, 0)  # Right eye
        
        # Smile
        for angle in range(0, 180):
            rad = np.radians(angle)
            x = int(300 + 20 * np.cos(rad))
            y = int(230 + 10 * np.sin(rad))
            if 0 <= x < width and 0 <= y < height:
                img[y, x] = (int(255*pulse), int(100*pulse), int(100*pulse))
        
        frames.append(img)
    
    # Save as GIF
    imageio.mimsave(os.path.join(OUT_DIR, filename), frames, duration=0.2, loop=0)

make_proper_borat_gif("proper_borat.gif")
print("Proper Borat GIF created in", OUT_DIR)