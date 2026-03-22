"""
Generate أذان وحكاية App Icons & Splash Screens
Branding: Deep Emerald (#064e3b) + Gold (#d4a843)
Design: Crescent Moon with Star (Islamic motif)
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

# Brand colors
BG_COLOR = (6, 78, 59)        # #064e3b - Deep Emerald
GOLD = (212, 168, 67)          # #d4a843 - Islamic Gold
GOLD_LIGHT = (232, 198, 107)   # lighter gold for star
WHITE = (255, 255, 255)
DARK_BG = (12, 26, 20)        # #0c1a14

def draw_crescent_and_star(draw, cx, cy, radius, color, star_color):
    """Draw an Islamic crescent moon with an 8-pointed star"""
    # Outer circle (full moon)
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=color
    )
    # Inner circle (cutout for crescent) - shifted right
    cut_radius = radius * 0.82
    cut_offset = radius * 0.38
    draw.ellipse(
        [cx - cut_radius + cut_offset, cy - cut_radius,
         cx + cut_radius + cut_offset, cy + cut_radius],
        fill=BG_COLOR
    )
    # 8-pointed star
    star_cx = cx + radius * 0.55
    star_cy = cy - radius * 0.15
    star_r = radius * 0.22
    # Draw two overlapping squares rotated 45 degrees
    points_sq1 = []
    points_sq2 = []
    for i in range(4):
        angle1 = math.radians(i * 90 - 45)
        points_sq1.append((
            star_cx + star_r * math.cos(angle1),
            star_cy + star_r * math.sin(angle1)
        ))
        angle2 = math.radians(i * 90)
        points_sq2.append((
            star_cx + star_r * math.cos(angle2),
            star_cy + star_r * math.sin(angle2)
        ))
    draw.polygon(points_sq1, fill=star_color)
    draw.polygon(points_sq2, fill=star_color)


def generate_icon(size, output_path, round_mask=False):
    """Generate app icon at given size"""
    img = Image.new('RGBA', (size, size), (*BG_COLOR, 255))
    draw = ImageDraw.Draw(img)
    
    # Add subtle gradient effect with concentric circles
    center = size // 2
    for i in range(20):
        r = size // 2 - i * 2
        if r <= 0:
            break
        opacity = max(0, 255 - i * 3)
        c = (
            min(255, BG_COLOR[0] + i),
            min(255, BG_COLOR[1] + i * 2),
            min(255, BG_COLOR[2] + i)
        )
        draw.ellipse([center-r, center-r, center+r, center+r], fill=(*c, opacity))
    
    # Draw crescent and star
    moon_radius = int(size * 0.30)
    draw_crescent_and_star(draw, center - int(size*0.05), center, moon_radius, GOLD, GOLD_LIGHT)
    
    if round_mask:
        # Create circular mask
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, size, size], fill=255)
        img.putalpha(mask)
    
    # Convert to RGB for PNG without alpha issues
    final = Image.new('RGB', (size, size), BG_COLOR)
    final.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final.save(output_path, 'PNG', quality=95)
    print(f"  ✅ Generated: {output_path} ({size}x{size})")


def generate_foreground(size, output_path):
    """Generate adaptive icon foreground (with safe zone padding)"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Safe zone is 66% of the icon (center area)
    safe_size = int(size * 0.66)
    offset = (size - safe_size) // 2
    center = size // 2
    
    moon_radius = int(safe_size * 0.32)
    draw_crescent_and_star(
        draw, center - int(safe_size * 0.05), center, 
        moon_radius, GOLD, GOLD_LIGHT
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"  ✅ Generated foreground: {output_path} ({size}x{size})")


def generate_splash(width, height, output_path):
    """Generate splash screen with centered branding"""
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Subtle radial gradient
    cx, cy = width // 2, height // 2
    max_r = max(width, height) // 2
    for i in range(0, max_r, 4):
        r = max_r - i
        brightness = max(0, i * 0.08)
        c = (
            max(0, int(BG_COLOR[0] - brightness)),
            max(0, int(BG_COLOR[1] - brightness)),
            max(0, int(BG_COLOR[2] - brightness))
        )
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)
    
    # Draw crescent + star
    icon_size = min(width, height) * 0.18
    draw_crescent_and_star(draw, cx - int(icon_size*0.1), cy - int(icon_size*0.3), int(icon_size), GOLD, GOLD_LIGHT)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG', quality=90)
    print(f"  ✅ Generated splash: {output_path} ({width}x{height})")


def main():
    base = "/app/frontend/android/app/src/main/res"
    
    print("\n🎨 Generating App Icons...")
    # Standard icons (square)
    icon_sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192,
    }
    for folder, size in icon_sizes.items():
        generate_icon(size, f"{base}/{folder}/ic_launcher.png")
        generate_icon(size, f"{base}/{folder}/ic_launcher_round.png", round_mask=True)
    
    print("\n🎨 Generating Adaptive Icon Foregrounds...")
    fg_sizes = {
        'mipmap-mdpi': 108,
        'mipmap-hdpi': 162,
        'mipmap-xhdpi': 216,
        'mipmap-xxhdpi': 324,
        'mipmap-xxxhdpi': 432,
    }
    for folder, size in fg_sizes.items():
        generate_foreground(size, f"{base}/{folder}/ic_launcher_foreground.png")
    
    print("\n🎨 Generating Splash Screens...")
    # Portrait splash screens
    portrait_sizes = {
        'drawable-port-mdpi': (320, 480),
        'drawable-port-hdpi': (480, 800),
        'drawable-port-xhdpi': (720, 1280),
        'drawable-port-xxhdpi': (960, 1600),
        'drawable-port-xxxhdpi': (1280, 1920),
    }
    for folder, (w, h) in portrait_sizes.items():
        generate_splash(w, h, f"{base}/{folder}/splash.png")
    
    # Landscape splash screens
    landscape_sizes = {
        'drawable-land-mdpi': (480, 320),
        'drawable-land-hdpi': (800, 480),
        'drawable-land-xhdpi': (1280, 720),
        'drawable-land-xxhdpi': (1600, 960),
        'drawable-land-xxxhdpi': (1920, 1280),
    }
    for folder, (w, h) in landscape_sizes.items():
        generate_splash(w, h, f"{base}/{folder}/splash.png")
    
    # Default splash
    generate_splash(480, 800, f"{base}/drawable/splash.png")
    
    # Play Store icon (1024x1024)
    print("\n🎨 Generating Play Store Icon (1024x1024)...")
    generate_icon(1024, "/app/frontend/android/app_icon_1024.png")
    
    # Also generate PWA icons
    print("\n🎨 Generating PWA Icons...")
    generate_icon(192, "/app/frontend/public/pwa-icon-192.png")
    generate_icon(512, "/app/frontend/public/pwa-icon-512.png")
    generate_icon(512, "/app/frontend/public/pwa-icon-maskable.png")
    generate_icon(180, "/app/frontend/public/apple-touch-icon.png")
    
    print("\n✅ All assets generated successfully!")


if __name__ == '__main__':
    main()
