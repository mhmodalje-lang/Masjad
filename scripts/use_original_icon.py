"""
Use the EXACT user-provided icon image for all app icons.
Resize to all required Android + PWA sizes.
"""
from PIL import Image, ImageDraw
import os

SOURCE = "/tmp/original_icon.jpg"
img_src = Image.open(SOURCE).convert('RGBA')

# Make it perfectly square (crop center if needed)
w, h = img_src.size
s = min(w, h)
left = (w - s) // 2
top = (h - s) // 2
img_src = img_src.crop((left, top, left + s, top + s))

print(f"Source icon: {img_src.size}")

def save_icon(size, path):
    """Resize and save as PNG"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    resized = img_src.resize((size, size), Image.LANCZOS)
    # Convert to RGB for standard PNG
    rgb = Image.new('RGB', (size, size), (6, 78, 59))
    rgb.paste(resized, mask=resized.split()[3] if resized.mode == 'RGBA' else None)
    rgb.save(path, 'PNG', quality=95)
    print(f"  ✅ {path} ({size}x{size})")

def save_round_icon(size, path):
    """Resize with circular mask"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    resized = img_src.resize((size, size), Image.LANCZOS)
    # Create circular mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, size, size], fill=255)
    # Apply mask
    rgb = Image.new('RGB', (size, size), (6, 78, 59))
    rgb.paste(resized, mask=resized.split()[3] if resized.mode == 'RGBA' else None)
    # Create final with circle
    final = Image.new('RGB', (size, size), (6, 78, 59))
    final.paste(rgb, mask=mask)
    final.save(path, 'PNG', quality=95)
    print(f"  ✅ {path} ({size}x{size}) [round]")

def save_foreground(size, path):
    """Adaptive icon foreground - centered in safe zone (66%)"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    # Content occupies 66% of the canvas
    content_size = int(size * 0.72)
    content = img_src.resize((content_size, content_size), Image.LANCZOS)
    offset = (size - content_size) // 2
    canvas.paste(content, (offset, offset), content.split()[3] if content.mode == 'RGBA' else None)
    canvas.save(path, 'PNG')
    print(f"  ✅ {path} ({size}x{size}) [foreground]")

def save_splash(width, height, path):
    """Splash screen - icon centered on dark emerald background"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bg = Image.new('RGB', (width, height), (4, 54, 40))
    # Draw subtle radial gradient
    draw = ImageDraw.Draw(bg)
    cx, cy = width // 2, height // 2
    max_r = max(width, height) // 2
    for r in range(max_r, 0, -4):
        t = 1 - (r / max_r)
        c = (
            int(4 + 12 * t * 0.3),
            int(54 + 24 * t * 0.3),
            int(40 + 19 * t * 0.3),
        )
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)
    # Place icon in center
    icon_size = int(min(width, height) * 0.35)
    icon = img_src.resize((icon_size, icon_size), Image.LANCZOS)
    ix = (width - icon_size) // 2
    iy = (height - icon_size) // 2
    bg.paste(icon, (ix, iy), icon.split()[3] if icon.mode == 'RGBA' else None)
    bg.save(path, 'PNG', quality=90)
    print(f"  ✅ {path} ({width}x{height})")

# ═══════ GENERATE ALL ═══════
base = "/app/frontend/android/app/src/main/res"

print("\n🎨 Android App Icons (ic_launcher)...")
for folder, size in [('mipmap-mdpi', 48), ('mipmap-hdpi', 72), ('mipmap-xhdpi', 96), ('mipmap-xxhdpi', 144), ('mipmap-xxxhdpi', 192)]:
    save_icon(size, f"{base}/{folder}/ic_launcher.png")

print("\n🎨 Android Round Icons (ic_launcher_round)...")
for folder, size in [('mipmap-mdpi', 48), ('mipmap-hdpi', 72), ('mipmap-xhdpi', 96), ('mipmap-xxhdpi', 144), ('mipmap-xxxhdpi', 192)]:
    save_round_icon(size, f"{base}/{folder}/ic_launcher_round.png")

print("\n🎨 Adaptive Icon Foregrounds...")
for folder, size in [('mipmap-mdpi', 108), ('mipmap-hdpi', 162), ('mipmap-xhdpi', 216), ('mipmap-xxhdpi', 324), ('mipmap-xxxhdpi', 432)]:
    save_foreground(size, f"{base}/{folder}/ic_launcher_foreground.png")

print("\n🎨 Splash Screens (Portrait)...")
for folder, dims in [('drawable-port-mdpi', (320,480)), ('drawable-port-hdpi', (480,800)), ('drawable-port-xhdpi', (720,1280)), ('drawable-port-xxhdpi', (960,1600)), ('drawable-port-xxxhdpi', (1280,1920))]:
    save_splash(dims[0], dims[1], f"{base}/{folder}/splash.png")

print("\n🎨 Splash Screens (Landscape)...")
for folder, dims in [('drawable-land-mdpi', (480,320)), ('drawable-land-hdpi', (800,480)), ('drawable-land-xhdpi', (1280,720)), ('drawable-land-xxhdpi', (1600,960)), ('drawable-land-xxxhdpi', (1920,1280))]:
    save_splash(dims[0], dims[1], f"{base}/{folder}/splash.png")

save_splash(480, 800, f"{base}/drawable/splash.png")

print("\n🎨 Play Store Icon (1024x1024)...")
save_icon(1024, "/app/frontend/android/app_icon_1024.png")

print("\n🎨 PWA Icons...")
save_icon(192, "/app/frontend/public/pwa-icon-192.png")
save_icon(512, "/app/frontend/public/pwa-icon-512.png")
save_icon(512, "/app/frontend/public/pwa-icon-maskable.png")
save_round_icon(180, "/app/frontend/public/apple-touch-icon.png")

# Also save favicon
print("\n🎨 Favicon...")
favicon = img_src.resize((64, 64), Image.LANCZOS)
favicon_rgb = Image.new('RGB', (64, 64), (6, 78, 59))
favicon_rgb.paste(favicon, mask=favicon.split()[3] if favicon.mode == 'RGBA' else None)
favicon_rgb.save("/app/frontend/public/favicon.ico", quality=95)
print("  ✅ favicon.ico (64x64)")

print("\n✅ ALL ICONS GENERATED FROM YOUR ORIGINAL IMAGE!")
