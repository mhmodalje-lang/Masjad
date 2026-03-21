"""
Split server.py into modular routers.
"""
import re

with open('/app/backend/server.py', 'r') as f:
    content = f.read()
    lines = content.split('\n')

total = len(lines)

def extract_lines(start, end):
    """Extract lines (1-indexed inclusive)."""
    return '\n'.join(lines[start-1:end])

def make_router_file(name, tag, code_sections, extra_imports="", extra_top="", has_admin=False):
    """Generate a router file."""
    base_imports = f'''"""
Router: {name}
"""
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from deps import db, get_user, logger, security, verify_jwt, create_jwt, hash_password, check_password, ADMIN_EMAILS, STRIPE_API_KEY, EMERGENT_LLM_KEY, haversine, query_overpass, clean_time, OVERPASS_ENDPOINTS, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_EMAIL, FIREBASE_PROJECT_ID, RESEND_API_KEY, GEMINI_API_KEY
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
import uuid
import random
import math
import re
import httpx
import os
import json as json_module
'''
    if has_admin:
        base_imports += "from deps import get_admin_user\n"
    
    base_imports += extra_imports + "\n"
    
    router_def = f'router = APIRouter(tags=["{tag}"])\n\n'
    
    # Replace @api_router with @router
    combined = '\n\n'.join(code_sections)
    combined = combined.replace('@api_router.', '@router.')
    
    return base_imports + extra_top + router_def + combined + '\n'

# === AUTH ROUTER (lines 201-360) ===
# Models are at lines 129-161, but they're used by auth
auth_models = extract_lines(129, 137)  # UserRegister, UserLogin
auth_profile_model = extract_lines(300, 340)  # UpdateProfileRequest
auth_code = extract_lines(201, 360)

auth_file = make_router_file("auth", "Authentication", [auth_models, auth_profile_model, auth_code],
    extra_imports="from fastapi.security import HTTPAuthorizationCredentials\n")

with open('/app/backend/routers/auth.py', 'w') as f:
    f.write(auth_file)
print("Created auth.py")

# === SOCIAL ROUTER (lines 342-1000) ===
social_models = extract_lines(342, 360)  # CreatePostRequest, CreateCommentRequest, CreatePageRequest
social_code = extract_lines(361, 999)

social_file = make_router_file("social", "Social (Sohba)", [social_models, social_code],
    has_admin=True)

with open('/app/backend/routers/social.py', 'w') as f:
    f.write(social_file)
print("Created social.py")

# === UPLOAD ROUTER (lines 997-1070) ===
upload_code = extract_lines(997, 1070)
upload_file = make_router_file("upload", "Upload", [upload_code],
    extra_imports="from fastapi import UploadFile, File as FastAPIFile\nfrom fastapi.responses import FileResponse\nfrom pathlib import Path\n\nUPLOAD_DIR = Path(__file__).parent.parent / 'uploads'\nUPLOAD_DIR.mkdir(exist_ok=True)\n")

with open('/app/backend/routers/upload.py', 'w') as f:
    f.write(upload_file)
print("Created upload.py")

# === ECONOMY ROUTER (lines 1073-1770) ===
economy_code = extract_lines(1073, 1770)
economy_file = make_router_file("economy", "Economy", [economy_code],
    extra_imports="from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionRequest\nfrom starlette.requests import Request\n")

with open('/app/backend/routers/economy.py', 'w') as f:
    f.write(economy_file)
print("Created economy.py")

# === MARKETPLACE ROUTER (lines 1772-1940) ===
marketplace_code = extract_lines(1772, 1936)
# Also include admin marketplace endpoints
admin_marketplace = extract_lines(1834, 1936)
# And ads active + placement from later
marketplace_file = make_router_file("marketplace", "Marketplace & Ads", [marketplace_code],
    has_admin=True)

with open('/app/backend/routers/marketplace.py', 'w') as f:
    f.write(marketplace_file)
print("Created marketplace.py")

# === AI ROUTER (lines 1937-2020 + 2449-2540 + 4043-4170) ===
ai_code1 = extract_lines(1937, 2020)
ai_code2 = extract_lines(2449, 2541)
ai_code3 = extract_lines(4043, 4170)
ai_file = make_router_file("ai", "AI Assistant", [ai_code1, ai_code2, ai_code3])

with open('/app/backend/routers/ai.py', 'w') as f:
    f.write(ai_file)
print("Created ai.py")

# === PRAYER ROUTER (lines 2165-2450 + 2542-2680) ===
# Include PushSubscription, MosqueTimesRequest, DhikrAIRequest models
prayer_models = extract_lines(138, 161)
prayer_code1 = extract_lines(2165, 2450)
prayer_code2 = extract_lines(2542, 2680)
prayer_file = make_router_file("prayer", "Prayer & Mosques", [prayer_models, prayer_code1, prayer_code2],
    extra_imports="import asyncio\n")

with open('/app/backend/routers/prayer.py', 'w') as f:
    f.write(prayer_file)
print("Created prayer.py")

# === QURAN HADITH ROUTER (lines 2680-2980) ===
quran_code = extract_lines(2680, 2984)
quran_file = make_router_file("quran_hadith", "Quran & Hadith", [quran_code])

with open('/app/backend/routers/quran_hadith.py', 'w') as f:
    f.write(quran_file)
print("Created quran_hadith.py")

# === ADMIN ROUTER (lines 2985-3530) ===
admin_code = extract_lines(2985, 3530)
admin_file = make_router_file("admin", "Admin", [admin_code],
    has_admin=True)

with open('/app/backend/routers/admin.py', 'w') as f:
    f.write(admin_file)
print("Created admin.py")

# === ISLAMIC TOOLS ROUTER (includes localization, audio, ruqyah public, asma-al-husna, ad-config) ===
islamic_code1 = extract_lines(3501, 3653)  # audio, localization
islamic_code2 = extract_lines(3413, 3500)  # ad-config, analytics
islamic_file = make_router_file("islamic_tools", "Islamic Tools", [islamic_code2, islamic_code1])

with open('/app/backend/routers/islamic_tools.py', 'w') as f:
    f.write(islamic_file)
print("Created islamic_tools.py")

# === STORIES ROUTER (lines 3654-3916 + 4172-4248 + 5193-5365) ===
stories_models = extract_lines(3654, 3665)  # CreateStoryRequest area
stories_code1 = extract_lines(3654, 3916)
stories_voice = extract_lines(4172, 4248)
stories_translate = extract_lines(5193, 5364)
stories_file = make_router_file("stories", "Stories", [stories_code1, stories_voice, stories_translate])

with open('/app/backend/routers/stories.py', 'w') as f:
    f.write(stories_file)
print("Created stories.py")

# === MISC ROUTER (status, contact, report, user/*, announcements, pages, embed, analytics, donations, webhook) ===
misc_code1 = extract_lines(1514, 1537)  # webhook/stripe
misc_code2 = extract_lines(2022, 2164)  # user/bank, earnings, admin/bank, announcements, vendors
misc_code3 = extract_lines(2962, 2984)  # user/sync
misc_code4 = extract_lines(3179, 3256)  # public pages
misc_code5 = extract_lines(3910, 3990)  # embed content, status models
misc_code6 = extract_lines(3992, 4042)  # status, contact, report
misc_code7 = extract_lines(4249, 4464)  # admin/stats, admin/contacts, donations, donation-requests, admin/seed-content
misc_code8 = extract_lines(3979, 3990)  # public embed-content
misc_file = make_router_file("misc", "Miscellaneous", 
    [misc_code1, misc_code2, misc_code3, misc_code4, misc_code5, misc_code6, misc_code7],
    extra_imports="from starlette.requests import Request\nfrom emergentintegrations.payments.stripe.checkout import StripeCheckout\n",
    has_admin=True)

with open('/app/backend/routers/misc.py', 'w') as f:
    f.write(misc_file)
print("Created misc.py")

# === ARABIC ACADEMY ROUTER (lines 4663-5045) ===
academy_code = extract_lines(4663, 5045)
academy_file = make_router_file("arabic_academy", "Arabic Academy", [academy_code])

with open('/app/backend/routers/arabic_academy.py', 'w') as f:
    f.write(academy_file)
print("Created arabic_academy.py")

# === LIVE STREAMS ROUTER (lines 5046-5192) ===
streams_code = extract_lines(5046, 5192)
streams_file = make_router_file("live_streams", "Live Streams", [streams_code],
    has_admin=True)

with open('/app/backend/routers/live_streams.py', 'w') as f:
    f.write(streams_file)
print("Created live_streams.py")

# === KIDS ZONE ROUTER (lines 5365-6170) ===
kids_zone_code = extract_lines(5365, 6170)
kids_zone_file = make_router_file("kids_zone", "Kids Zone", [kids_zone_code])

with open('/app/backend/routers/kids_zone.py', 'w') as f:
    f.write(kids_zone_file)
print("Created kids_zone.py")

# === KIDS LEARN ROUTER (lines 6171-6494) ===
kids_learn_code = extract_lines(6171, 6494)
kids_learn_imports = """from kids_learning import (
    build_daily_lesson, get_quran_memorization_plan, get_all_duas,
    get_all_hadiths, get_prophet_stories, get_islamic_pillars,
    get_library_categories, get_library_items,
    QURAN_SURAHS_FOR_KIDS, KIDS_DUAS, KIDS_HADITHS, PROPHET_STORIES, 
    ISLAMIC_PILLARS, KIDS_LIBRARY_CATEGORIES, KIDS_LIBRARY_ITEMS,
)
from kids_learning_extended import (
    ALL_PROPHETS, WUDU_STEPS, SALAH_STEPS, ARABIC_ALPHABET,
    ACHIEVEMENT_BADGES, EXTENDED_LIBRARY, EXTENDED_DUAS, EXTENDED_HADITHS,
    get_wudu_steps, get_salah_steps, get_alphabet, get_vocabulary as ext_get_vocabulary,
    get_achievements, get_all_prophets,
)
from kids_curriculum import (
    get_curriculum_overview, generate_lesson, CURRICULUM_STAGES,
)
"""
kids_learn_file = make_router_file("kids_learn", "Kids Learn", [kids_learn_code],
    extra_imports=kids_learn_imports)

with open('/app/backend/routers/kids_learn.py', 'w') as f:
    f.write(kids_learn_file)
print("Created kids_learn.py")

print("\n=== ALL ROUTERS CREATED ===")
print(f"Original server.py: {total} lines")
