"""
Router: live_streams
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
from deps import get_admin_user

router = APIRouter(tags=["Live Streams"])

# Default live streams to seed when DB is empty
DEFAULT_STREAMS = [
    {
        "id": "makkah-live",
        "name": "بث مباشر من المسجد الحرام - مكة المكرمة",
        "embed_type": "channel",
        "embed_value": "UCbsPpCigjUXLes8oZEPpnnQ",
        "thumbnail": "https://i.ytimg.com/vi/ZKVM8ERdBHQ/maxresdefault_live.jpg",
        "city": "Makkah",
        "country": "Saudi Arabia",
        "category": "haramain",
        "is_247": True,
        "is_active": True,
        "sort_order": 1,
    },
    {
        "id": "madinah-live",
        "name": "بث مباشر من المسجد النبوي - المدينة المنورة",
        "embed_type": "video",
        "embed_value": "Kp4ZqcS2EBo",
        "thumbnail": "https://i.ytimg.com/vi/Kp4ZqcS2EBo/maxresdefault_live.jpg",
        "city": "Madinah",
        "country": "Saudi Arabia",
        "category": "haramain",
        "is_247": True,
        "is_active": True,
        "sort_order": 2,
    },
    {
        "id": "aqsa-live",
        "name": "بث مباشر من المسجد الأقصى - القدس",
        "embed_type": "video",
        "embed_value": "j1L8bEmWYCE",
        "thumbnail": "https://i.ytimg.com/vi/j1L8bEmWYCE/maxresdefault_live.jpg",
        "city": "Jerusalem",
        "country": "Palestine",
        "category": "holy",
        "is_247": True,
        "is_active": True,
        "sort_order": 3,
    },
]

@router.get("/live-streams")
async def get_live_streams(category: str = "all"):
    """Get available live streams from DB"""
    query = {"is_active": True}
    if category != "all":
        query["category"] = category
    streams_cursor = db.live_streams.find(query).sort("sort_order", 1)
    streams = []
    async for s in streams_cursor:
        s.pop("_id", None)
        # Build embed URL
        if s.get("embed_type") == "channel":
            s["embed_url"] = f"https://www.youtube.com/embed/live_stream?channel={s['embed_value']}"
        else:
            s["embed_url"] = f"https://www.youtube.com/embed/{s['embed_value']}"
        streams.append(s)
    # If no streams in DB, seed defaults
    if not streams and category == "all":
        for ds in DEFAULT_STREAMS:
            await db.live_streams.insert_one({**ds})
        return await get_live_streams(category)
    return {"success": True, "streams": streams, "total": len(streams)}

@router.get("/live-streams/{stream_id}")
async def get_live_stream(stream_id: str):
    """Get a specific live stream"""
    stream = await db.live_streams.find_one({"id": stream_id})
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    stream.pop("_id", None)
    if stream.get("embed_type") == "channel":
        stream["embed_url"] = f"https://www.youtube.com/embed/live_stream?channel={stream['embed_value']}"
    else:
        stream["embed_url"] = f"https://www.youtube.com/embed/{stream['embed_value']}"
    return {"success": True, "stream": stream}

# Admin CRUD for Live Streams
@router.post("/admin/live-streams")
async def admin_create_stream(data: dict, user: dict = Depends(get_user)):
    """Admin: Add a new live stream"""
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    # Parse embed URL/ID from user input
    embed_input = data.get("embed_url", "").strip()
    embed_type = "video"
    embed_value = embed_input
    
    # Detect embed type from URL
    if "youtube.com/embed/live_stream?channel=" in embed_input:
        embed_type = "channel"
        embed_value = embed_input.split("channel=")[-1].split("&")[0]
    elif "youtube.com/embed/" in embed_input:
        embed_value = embed_input.split("/embed/")[-1].split("?")[0]
    elif "youtube.com/watch?v=" in embed_input:
        embed_value = embed_input.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in embed_input:
        embed_value = embed_input.split("youtu.be/")[-1].split("?")[0]
    elif "youtube.com/channel/" in embed_input:
        embed_type = "channel"
        embed_value = embed_input.split("/channel/")[-1].split("/")[0]
    
    stream = {
        "id": str(uuid.uuid4())[:8],
        "name": data.get("name", "Live Stream"),
        "embed_type": embed_type,
        "embed_value": embed_value,
        "thumbnail": data.get("thumbnail", ""),
        "city": data.get("city", ""),
        "country": data.get("country", ""),
        "category": data.get("category", "other"),
        "is_247": data.get("is_247", False),
        "is_active": True,
        "sort_order": data.get("sort_order", 99),
        "created_at": datetime.utcnow().isoformat(),
        "created_by": user["id"]
    }
    await db.live_streams.insert_one(stream)
    stream.pop("_id", None)
    return {"success": True, "stream": stream}

@router.put("/admin/live-streams/{stream_id}")
async def admin_update_stream(stream_id: str, data: dict, user: dict = Depends(get_user)):
    """Admin: Update a live stream"""
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    update = {}
    for field in ["name", "embed_type", "embed_value", "thumbnail", "city", "country", "category", "is_247", "is_active", "sort_order"]:
        if field in data:
            update[field] = data[field]
    
    # Handle embed_url input
    if "embed_url" in data:
        embed_input = data["embed_url"].strip()
        if "youtube.com/embed/live_stream?channel=" in embed_input:
            update["embed_type"] = "channel"
            update["embed_value"] = embed_input.split("channel=")[-1].split("&")[0]
        elif "youtube.com/embed/" in embed_input:
            update["embed_type"] = "video"
            update["embed_value"] = embed_input.split("/embed/")[-1].split("?")[0]
        elif "youtube.com/watch?v=" in embed_input:
            update["embed_type"] = "video"
            update["embed_value"] = embed_input.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in embed_input:
            update["embed_type"] = "video"
            update["embed_value"] = embed_input.split("youtu.be/")[-1].split("?")[0]
    
    if update:
        await db.live_streams.update_one({"id": stream_id}, {"$set": update})
    
    stream = await db.live_streams.find_one({"id": stream_id})
    if stream:
        stream.pop("_id", None)
    return {"success": True, "stream": stream}

@router.delete("/admin/live-streams/{stream_id}")
async def admin_delete_stream(stream_id: str, user: dict = Depends(get_user)):
    """Admin: Delete a live stream"""
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    await db.live_streams.delete_one({"id": stream_id})
    return {"success": True, "message": "Stream deleted"}

@router.get("/admin/live-streams")
async def admin_list_streams(user: dict = Depends(get_user)):
    """Admin: List all streams (including inactive)"""
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    streams = []
    async for s in db.live_streams.find().sort("sort_order", 1):
        s.pop("_id", None)
        if s.get("embed_type") == "channel":
            s["embed_url"] = f"https://www.youtube.com/embed/live_stream?channel={s['embed_value']}"
        else:
            s["embed_url"] = f"https://www.youtube.com/embed/{s['embed_value']}"
        streams.append(s)
    return {"success": True, "streams": streams, "total": len(streams)}


# ==================== TRANSLATION SERVICE ====================
SUPPORTED_LANGUAGES = ['ar', 'en', 'sv', 'nl', 'el', 'de', 'ru', 'fr', 'tr']
LANGUAGE_NAMES = {
    'ar': 'Arabic', 'en': 'English', 'sv': 'Swedish', 'nl': 'Dutch',
    'el': 'Greek', 'de': 'German', 'ru': 'Russian', 'fr': 'French', 'tr': 'Turkish'
}

