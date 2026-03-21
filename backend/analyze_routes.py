"""
Script to extract router sections from server.py into individual files.
Run once for the refactoring.
"""
import re

# Read server.py
with open('/app/backend/server.py', 'r') as f:
    lines = f.readlines()

total = len(lines)
print(f"Total lines: {total}")

# Find all endpoint decorators with their line numbers
endpoints = []
for i, line in enumerate(lines):
    if line.strip().startswith('@api_router.'):
        match = re.search(r'@api_router\.\w+\("(/[^"]+)"', line)
        if match:
            path = match.group(1)
            endpoints.append((i+1, path))  # 1-indexed

print(f"\nTotal endpoints: {len(endpoints)}")

# Categorize by prefix
categories = {}
for line_no, path in endpoints:
    parts = path.strip('/').split('/')
    prefix = parts[0] if parts else 'root'
    # Special handling for multi-segment prefixes
    if prefix == 'admin':
        prefix = 'admin'
    elif prefix == 'sohba':
        prefix = 'social'
    elif prefix in ('kids-zone',):
        prefix = 'kids_zone'
    elif prefix in ('kids-learn',):
        prefix = 'kids_learn'
    elif prefix in ('arabic-academy',):
        prefix = 'arabic_academy'
    elif prefix in ('live-streams',):
        prefix = 'live_streams'
    elif prefix in ('donation-requests',):
        prefix = 'donations'
    elif prefix in ('quran', 'hadith'):
        prefix = 'quran_hadith'
    elif prefix in ('upload', 'uploads'):
        prefix = 'upload'
    elif prefix in ('rewards', 'store', 'membership', 'payments', 'credits', 'gifts'):
        prefix = 'economy'
    elif prefix in ('ads', 'marketplace'):
        prefix = 'marketplace'
    elif prefix in ('push',):
        prefix = 'prayer'
    elif prefix in ('prayer-times', 'mosques', 'hijri-date'):
        prefix = 'prayer'
    elif prefix in ('localization', 'audio', 'asma-al-husna', 'ruqyah', 'ad-config'):
        prefix = 'islamic_tools'
    elif prefix in ('stories', 'translate'):
        prefix = 'stories'
    elif prefix in ('donations',):
        prefix = 'donations'
    elif prefix in ('ai',):
        prefix = 'ai'
    elif prefix in ('user', 'announcements', 'pages', 'embed-content'):
        prefix = 'misc'
    elif prefix in ('analytics', 'contact', 'report', 'status', 'webhook'):
        prefix = 'misc'
    
    if prefix not in categories:
        categories[prefix] = []
    categories[prefix].append((line_no, path))

print("\n=== ROUTE CATEGORIES ===")
for cat, routes in sorted(categories.items()):
    print(f"\n{cat} ({len(routes)} endpoints):")
    for line_no, path in routes:
        print(f"  L{line_no}: {path}")
