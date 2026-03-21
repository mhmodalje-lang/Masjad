"""
Shared dependencies for all routers.
Database, auth, config, utilities.
"""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
import hashlib
import hmac as hmac_lib
import base64
import json as json_module
import math
import httpx
import re
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Config
JWT_SECRET = os.environ.get('JWT_SECRET', 'almuadhin-global-secret-2026')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID', 'hxhdh-78bec')
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY', '')
VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY', '')
VAPID_EMAIL = os.environ.get('VAPID_EMAIL', 'mailto:mohammadalrejab@gmail.com')
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY', '')
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')

# MongoDB
client_db = AsyncIOMotorClient(MONGO_URL)
db = client_db[DB_NAME]

# Security
security = HTTPBearer(auto_error=False)

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Admin
ADMIN_EMAILS = ['mohammadalrejab@gmail.com']

# JWT
def _b64enc(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def _b64dec(s: str) -> bytes:
    s += '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)

def create_jwt(payload: dict, hours: int = 720) -> str:
    header = _b64enc(json_module.dumps({"alg":"HS256","typ":"JWT"}).encode())
    exp = datetime.utcnow() + timedelta(hours=hours)
    pl = {**payload, "exp": exp.isoformat(), "iat": datetime.utcnow().isoformat()}
    pl_enc = _b64enc(json_module.dumps(pl).encode())
    sig = hmac_lib.new(JWT_SECRET.encode(), f"{header}.{pl_enc}".encode(), hashlib.sha256).digest()
    return f"{header}.{pl_enc}.{_b64enc(sig)}"

def verify_jwt(token: str) -> Optional[dict]:
    try:
        h, p, s = token.split('.')
        expected = hmac_lib.new(JWT_SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
        if not hmac_lib.compare_digest(expected, _b64dec(s)):
            return None
        payload = json_module.loads(_b64dec(p))
        if datetime.utcnow() > datetime.fromisoformat(payload["exp"]):
            return None
        return payload
    except Exception:
        return None

def hash_password(pw: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', pw.encode(), salt, 100000)
    return f"{base64.b64encode(salt).decode()}:{base64.b64encode(dk).decode()}"

def check_password(pw: str, hashed: str) -> bool:
    try:
        s, dk = hashed.split(':')
        return hmac_lib.compare_digest(
            hashlib.pbkdf2_hmac('sha256', pw.encode(), base64.b64decode(s), 100000),
            base64.b64decode(dk)
        )
    except Exception:
        return False

async def get_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> Optional[dict]:
    if not creds:
        return None
    payload = verify_jwt(creds.credentials)
    if not payload:
        return None
    return await db.users.find_one({"id": payload.get("user_id")})

async def get_admin_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="غير مصرح")
    payload = verify_jwt(credentials.credentials)
    if not payload or payload.get("email") not in ADMIN_EMAILS:
        raise HTTPException(status_code=403, detail="غير مصرح - ليس مسؤولاً")
    return payload

# Utilities
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

async def query_overpass(q: str) -> Optional[dict]:
    for ep in OVERPASS_ENDPOINTS:
        try:
            async with httpx.AsyncClient(timeout=20) as c:
                r = await c.post(ep, content=q, headers={"Content-Type":"text/plain"})
                if r.status_code == 200:
                    return r.json()
        except Exception:
            continue
    return None

def clean_time(t: str) -> str:
    return re.sub(r'\s*\(.*?\)', '', t).strip()
