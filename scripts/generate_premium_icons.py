"""
Generate PREMIUM أذان وحكاية App Icons & Splash Screens
High-quality Islamic branding with ornamental gold borders
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

# Brand colors
BG_DARK = (4, 54, 40)         # Dark emerald
BG_MID = (6, 78, 59)          # #064e3b
BG_LIGHT = (16, 100, 75)      # Lighter emerald
GOLD = (212, 168, 67)          # #d4a843
GOLD_BRIGHT = (245, 208, 100) # Bright gold
GOLD_DARK = (170, 130, 40)    # Dark gold for depth
WHITE_GOLD = (255, 240, 180)  # Light gold highlight
BLACK = (0, 0, 0)


def draw_gradient_bg(draw, size):
    """Radial gradient emerald background"""
    cx, cy = size // 2, size // 2
    max_r = int(size * 0.75)
    for r in range(max_r, 0, -1):
        t = r / max_r
        color = (
            int(BG_DARK[0] + (BG_LIGHT[0] - BG_DARK[0]) * t * 0.6),
            int(BG_DARK[1] + (BG_LIGHT[1] - BG_DARK[1]) * t * 0.6),
            int(BG_DARK[2] + (BG_LIGHT[2] - BG_DARK[2]) * t * 0.6),
        )
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)


def draw_ornamental_border(draw, size, margin, color, width=2):
    """Draw Islamic geometric ornamental border"""
    m = margin
    s = size - margin
    corner_size = int(size * 0.08)
    
    # Main border rectangle
    for w in range(width):
        draw.rectangle([m+w, m+w, s-w, s-w], outline=color)
    
    # Inner border with gap
    inner_m = margin + int(size * 0.025)
    inner_s = size - margin - int(size * 0.025)
    for w in range(max(1, width - 1)):
        draw.rectangle([inner_m+w, inner_m+w, inner_s-w, inner_s-w], outline=color)
    
    # Corner ornaments (Islamic geometric squares)
    for cx, cy in [(m, m), (s, m), (m, s), (s, s)]:
        cs = corner_size
        # Diamond shape at each corner
        pts = [
            (cx, cy - cs),
            (cx + cs, cy),
            (cx, cy + cs),
            (cx - cs, cy),
        ]
        draw.polygon(pts, fill=color)
        # Smaller inner diamond
        cs2 = int(cs * 0.5)
        pts2 = [
            (cx, cy - cs2),
            (cx + cs2, cy),
            (cx, cy + cs2),
            (cx - cs2, cy),
        ]
        draw.polygon(pts2, fill=BG_MID)
    
    # Side ornaments (small diamonds along edges)
    mid_x = size // 2
    mid_y = size // 2
    diamond_size = int(size * 0.025)
    # Top & bottom center
    for px, py in [(mid_x, m), (mid_x, s), (m, mid_y), (s, mid_y)]:
        ds = diamond_size
        draw.polygon([(px, py-ds), (px+ds, py), (px, py+ds), (px-ds, py)], fill=color)


def draw_crescent_moon(img, cx, cy, outer_r, color_main, color_highlight):
    """Draw a smooth, anti-aliased crescent moon"""
    # Work at 4x resolution for anti-aliasing
    scale = 4
    big_size = int(outer_r * 2 * scale * 1.5)
    big_cx = big_size // 2
    big_cy = big_size // 2
    big_r = outer_r * scale
    
    moon_img = Image.new('RGBA', (big_size, big_size), (0, 0, 0, 0))
    moon_draw = ImageDraw.Draw(moon_img)
    
    # Outer circle (full moon)
    moon_draw.ellipse(
        [big_cx - big_r, big_cy - big_r, big_cx + big_r, big_cy + big_r],
        fill=(*color_main, 255)
    )
    
    # Highlight on the outer edge for 3D effect
    highlight_r = int(big_r * 0.92)
    moon_draw.ellipse(
        [big_cx - highlight_r + int(big_r*0.06), big_cy - highlight_r + int(big_r*0.06),
         big_cx + highlight_r + int(big_r*0.06), big_cy + highlight_r + int(big_r*0.06)],
        fill=(*color_highlight, 200)
    )
    
    # Restore main color
    main_r = int(big_r * 0.88)
    moon_draw.ellipse(
        [big_cx - main_r + int(big_r*0.04), big_cy - main_r + int(big_r*0.04),
         big_cx + main_r + int(big_r*0.04), big_cy + main_r + int(big_r*0.04)],
        fill=(*color_main, 255)
    )
    
    # Cut-out circle (creates the crescent) - shifted right
    cut_r = int(big_r * 0.80)
    cut_offset = int(big_r * 0.42)
    moon_draw.ellipse(
        [big_cx - cut_r + cut_offset, big_cy - cut_r - int(big_r*0.02),
         big_cx + cut_r + cut_offset, big_cy + cut_r - int(big_r*0.02)],
        fill=(0, 0, 0, 0)
    )
    
    # Downscale with anti-aliasing
    target_size = int(outer_r * 2 * 1.5)
    moon_img = moon_img.resize((target_size, target_size), Image.LANCZOS)
    
    # Paste onto main image
    paste_x = cx - target_size // 2
    paste_y = cy - target_size // 2
    img.paste(moon_img, (paste_x, paste_y), moon_img)


def draw_star_8point(img, cx, cy, outer_r, inner_r, color):
    """Draw a smooth 8-pointed star with anti-aliasing"""
    scale = 4
    big_size = int(outer_r * 3 * scale)
    big_cx = big_size // 2
    big_cy = big_size // 2
    big_outer = outer_r * scale
    big_inner = inner_r * scale
    
    star_img = Image.new('RGBA', (big_size, big_size), (0, 0, 0, 0))
    star_draw = ImageDraw.Draw(star_img)
    
    # 8-pointed star: alternate outer and inner points
    points = []
    for i in range(16):
        angle = math.radians(i * 22.5 - 90)  # Start from top
        r = big_outer if i % 2 == 0 else big_inner
        points.append((
            big_cx + r * math.cos(angle),
            big_cy + r * math.sin(angle)
        ))
    
    star_draw.polygon(points, fill=(*color, 255))
    
    # Add a small bright center dot
    dot_r = int(big_inner * 0.35)
    star_draw.ellipse(
        [big_cx - dot_r, big_cy - dot_r, big_cx + dot_r, big_cy + dot_r],
        fill=(*WHITE_GOLD, 255)
    )
    
    # Downscale
    target_size = int(outer_r * 3)
    star_img = star_img.resize((target_size, target_size), Image.LANCZOS)
    
    paste_x = cx - target_size // 2
    paste_y = cy - target_size // 2
    img.paste(star_img, (paste_x, paste_y), star_img)


def generate_premium_icon(size, output_path, with_border=True):
    """Generate premium app icon"""
    img = Image.new('RGBA', (size, size), (*BG_DARK, 255))
    draw = ImageDraw.Draw(img)
    
    # Gradient background
    draw_gradient_bg(draw, size)
    
    # Ornamental border
    if with_border:
        border_margin = int(size * 0.06)
        border_width = max(1, int(size * 0.008))
        draw_ornamental_border(draw, size, border_margin, GOLD, border_width)
    
    # Crescent moon (centered, slightly left)
    moon_r = int(size * 0.28)
    moon_cx = int(size * 0.44)
    moon_cy = int(size * 0.50)
    draw_crescent_moon(img, moon_cx, moon_cy, moon_r, GOLD, GOLD_BRIGHT)
    
    # 8-pointed star (right of crescent, slightly above)
    star_outer = int(size * 0.09)
    star_inner = int(size * 0.045)
    star_cx = int(size * 0.65)
    star_cy = int(size * 0.38)
    draw_star_8point(img, star_cx, star_cy, star_outer, star_inner, GOLD_BRIGHT)
    
    # Convert to RGB
    final = Image.new('RGB', (size, size), BG_DARK)
    final.paste(img, mask=img.split()[3])
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final.save(output_path, 'PNG', quality=95)
    print(f"  ✅ {output_path} ({size}x{size})")


def generate_round_icon(size, output_path):
    """Generate round icon with circular mask"""
    # First generate the normal icon at larger size
    big = size * 2
    img = Image.new('RGBA', (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw circular background
    draw_gradient_bg(draw, big)
    
    # Crescent moon
    moon_r = int(big * 0.26)
    draw_crescent_moon(img, int(big * 0.44), int(big * 0.50), moon_r, GOLD, GOLD_BRIGHT)
    
    # Star
    star_outer = int(big * 0.085)
    star_inner = int(big * 0.042)
    draw_star_8point(img, int(big * 0.65), int(big * 0.38), star_outer, star_inner, GOLD_BRIGHT)
    
    # Add thin gold circle border
    border_w = max(2, int(big * 0.012))
    for w in range(border_w):
        r = big // 2 - w - 2
        draw.ellipse([big//2-r, big//2-r, big//2+r, big//2+r], outline=(*GOLD, 200))
    
    # Apply circular mask
    mask = Image.new('L', (big, big), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([2, 2, big-2, big-2], fill=255)
    img.putalpha(mask)
    
    # Downscale with AA
    img = img.resize((size, size), Image.LANCZOS)
    
    # Save with alpha for round icons
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Also create RGB version with green bg
    final = Image.new('RGB', (size, size), BG_DARK)
    final.paste(img, mask=img.split()[3])
    final.save(output_path, 'PNG', quality=95)
    print(f"  ✅ {output_path} ({size}x{size}) [round]")


def generate_foreground(size, output_path):
    """Generate adaptive icon foreground"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    # Safe zone content (66% of total)
    safe = int(size * 0.66)
    
    # Crescent moon
    moon_r = int(safe * 0.30)
    draw_crescent_moon(img, int(size * 0.44), int(size * 0.50), moon_r, GOLD, GOLD_BRIGHT)
    
    # Star
    star_outer = int(safe * 0.10)
    star_inner = int(safe * 0.05)
    draw_star_8point(img, int(size * 0.64), int(size * 0.38), star_outer, star_inner, GOLD_BRIGHT)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"  ✅ {output_path} ({size}x{size}) [foreground]")


def generate_splash(width, height, output_path):
    """Generate premium splash screen"""
    img = Image.new('RGB', (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Subtle radial gradient
    cx, cy = width // 2, height // 2
    max_r = max(width, height) // 2
    for r in range(max_r, 0, -3):
        t = 1 - (r / max_r)
        c = (
            int(BG_DARK[0] + (BG_LIGHT[0] - BG_DARK[0]) * t * 0.3),
            int(BG_DARK[1] + (BG_LIGHT[1] - BG_DARK[1]) * t * 0.3),
            int(BG_DARK[2] + (BG_LIGHT[2] - BG_DARK[2]) * t * 0.3),
        )
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)
    
    # Convert to RGBA for compositing
    img_rgba = img.convert('RGBA')
    
    # Crescent moon
    icon_r = int(min(width, height) * 0.14)
    draw_crescent_moon(img_rgba, cx - int(icon_r * 0.15), cy - int(icon_r * 0.3), icon_r, GOLD, GOLD_BRIGHT)
    
    # Star
    star_r = int(icon_r * 0.32)
    star_ir = int(icon_r * 0.16)
    draw_star_8point(img_rgba, cx + int(icon_r * 0.55), cy - int(icon_r * 0.65), star_r, star_ir, GOLD_BRIGHT)
    
    # Thin decorative line under the icon
    line_y = cy + int(icon_r * 0.9)
    line_w = int(min(width, height) * 0.3)
    draw_on = ImageDraw.Draw(img_rgba)
    draw_on.line([(cx - line_w//2, line_y), (cx + line_w//2, line_y)], fill=(*GOLD, 80), width=1)
    
    # Convert back to RGB
    final = Image.new('RGB', (width, height), BG_DARK)
    final.paste(img_rgba, mask=img_rgba.split()[3])
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final.save(output_path, 'PNG', quality=90)
    print(f"  ✅ {output_path} ({width}x{height})")


def main():
    base = "/app/frontend/android/app/src/main/res"
    
    print("\n🎨 Generating PREMIUM App Icons...")
    icon_sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192,
    }
    for folder, size in icon_sizes.items():
        generate_premium_icon(size, f"{base}/{folder}/ic_launcher.png")
        generate_round_icon(size, f"{base}/{folder}/ic_launcher_round.png")
    
    print("\n🎨 Generating Adaptive Foregrounds...")
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
    portrait_sizes = {
        'drawable-port-mdpi': (320, 480),
        'drawable-port-hdpi': (480, 800),
        'drawable-port-xhdpi': (720, 1280),
        'drawable-port-xxhdpi': (960, 1600),
        'drawable-port-xxxhdpi': (1280, 1920),
    }
    for folder, (w, h) in portrait_sizes.items():
        generate_splash(w, h, f"{base}/{folder}/splash.png")
    
    landscape_sizes = {
        'drawable-land-mdpi': (480, 320),
        'drawable-land-hdpi': (800, 480),
        'drawable-land-xhdpi': (1280, 720),
        'drawable-land-xxhdpi': (1600, 960),
        'drawable-land-xxxhdpi': (1920, 1280),
    }
    for folder, (w, h) in landscape_sizes.items():
        generate_splash(w, h, f"{base}/{folder}/splash.png")
    
    generate_splash(480, 800, f"{base}/drawable/splash.png")
    
    print("\n🎨 Play Store Icon (1024x1024)...")
    generate_premium_icon(1024, "/app/frontend/android/app_icon_1024.png", with_border=True)
    
    print("\n🎨 PWA Icons...")
    generate_premium_icon(192, "/app/frontend/public/pwa-icon-192.png", with_border=False)
    generate_premium_icon(512, "/app/frontend/public/pwa-icon-512.png", with_border=True)
    generate_premium_icon(512, "/app/frontend/public/pwa-icon-maskable.png", with_border=False)
    generate_round_icon(180, "/app/frontend/public/apple-touch-icon.png")
    
    print("\n✅ All PREMIUM assets generated!")


if __name__ == '__main__':
    main()
