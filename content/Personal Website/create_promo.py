import sys
import subprocess
import os

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFilter

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def add_shadow(im, offset=(0,15), shadow_blur=25, shadow_color=(0,0,0,60)):
    shadow = Image.new('RGBA', (im.width + shadow_blur*4, im.height + shadow_blur*4 + offset[1]), (0,0,0,0))
    
    # create solid rectangle for shadow
    shadow_rect = Image.new('RGBA', im.size, shadow_color)
    shadow_rect = add_corners(shadow_rect, 15)
    
    shadow.paste(shadow_rect, (shadow_blur*2 + offset[0], shadow_blur*2 + offset[1]), shadow_rect)
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))
    
    # Paste original image on top
    shadow.paste(im, (shadow_blur*2, shadow_blur*2), im)
    return shadow

def create_gradient_bg(width, height, color1, color2):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        # linear gradient
        c = int(255 * (y / height))
        mask_data.extend([c] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def main():
    files_img1 = ['Service HEalth Map.png', 'Service HEalth Map-1.png']
    files_img2 = ['Container Status (Real-time).png', 'Container Status (Real-time)-1.png']
    
    img1_path = next((f for f in files_img1 if os.path.exists(f)), None)
    img2_path = next((f for f in files_img2 if os.path.exists(f)), None)
    
    if not img1_path or not img2_path:
        print("Images not found!")
        return

    img1 = Image.open(img1_path).convert('RGBA')
    img2 = Image.open(img2_path).convert('RGBA')
    
    # Make sure both images have consistent styling (rounded corners)
    img1 = add_corners(img1, 20)
    img2 = add_corners(img2, 20)

    # Add drop shadows
    img1_shadow = add_shadow(img1)
    img2_shadow = add_shadow(img2)

    padding_x = 120
    padding_y = 120
    spacing = 80
    
    max_width = max(img1_shadow.width, img2_shadow.width)
    total_height = img1_shadow.height + spacing + img2_shadow.height
    
    bg_width = max_width + padding_x * 2
    bg_height = total_height + padding_y * 2
    
    # Create a nice gradient background (LinkedIn friendly dark/slate blue or soft gray)
    # Let's go with a soft tech-blue gradient
    bg = create_gradient_bg(bg_width, bg_height, (226, 232, 240), (241, 245, 249))
    bg = bg.convert('RGBA')
    
    # Center x
    x1 = (bg_width - img1_shadow.width) // 2
    y1 = padding_y
    
    x2 = (bg_width - img2_shadow.width) // 2
    y2 = y1 + img1_shadow.height + spacing
    
    bg.paste(img1_shadow, (x1, y1), img1_shadow)
    bg.paste(img2_shadow, (x2, y2), img2_shadow)
    
    output_path = 'linkedin_promo_combined.png'
    bg.convert("RGB").save(output_path, quality=95)
    print(f"Successfully created {output_path}")

if __name__ == "__main__":
    main()
