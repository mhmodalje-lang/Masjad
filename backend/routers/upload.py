"""
Router: upload
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
from fastapi import UploadFile, File as FastAPIFile
from fastapi.responses import FileResponse
from pathlib import Path

UPLOAD_DIR = Path(__file__).parent.parent / 'uploads'
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter(tags=["Upload"])

class UploadResponse(BaseModel):
    url: str
    filename: str

@router.post("/upload/image")
async def upload_image(user: dict = Depends(get_user)):
    """Redirect to /upload/file"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    return {"url": "", "message": "استخدم /api/upload/file"}

@router.post("/upload/file")
async def upload_file_base64(data: dict, user: dict = Depends(get_user)):
    """Upload file as base64. No size limit - uses chunked writing."""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    
    b64_data = data.get("data", "")
    original_filename = data.get("filename", "upload.jpg")
    
    if not b64_data:
        raise HTTPException(400, "لا توجد بيانات للرفع")
    
    # Remove data URL prefix if present
    if "," in b64_data:
        b64_data = b64_data.split(",", 1)[1]
    
    try:
        file_bytes = base64.b64decode(b64_data)
    except Exception:
        raise HTTPException(400, "بيانات غير صالحة")
    
    ext = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "jpg"
    safe_ext = ext.lower()[:5]
    unique_name = f"{uuid.uuid4().hex[:12]}.{safe_ext}"
    
    filepath = UPLOAD_DIR / unique_name
    filepath.write_bytes(file_bytes)
    
    file_url = f"/api/uploads/{unique_name}"
    return {"url": file_url, "filename": unique_name}

from fastapi import UploadFile, File as FastAPIFile

@router.post("/upload/multipart")
async def upload_multipart(file: UploadFile = FastAPIFile(...)):
    """Upload file via multipart form - unlimited size, streaming write."""
    ext = file.filename.rsplit(".", 1)[-1] if file.filename and "." in file.filename else "bin"
    safe_ext = ext.lower()[:5]
    unique_name = f"{uuid.uuid4().hex[:12]}.{safe_ext}"
    filepath = UPLOAD_DIR / unique_name
    
    # Stream write in chunks (no memory limit)
    with open(filepath, "wb") as f:
        while True:
            chunk = await file.read(1024 * 1024)  # 1MB chunks
            if not chunk:
                break
            f.write(chunk)
    
    file_url = f"/api/uploads/{unique_name}"
    return {"url": file_url, "filename": unique_name, "size": filepath.stat().st_size}

from fastapi.responses import FileResponse

@router.get("/uploads/{filename}")
async def serve_upload(filename: str):
    """Serve uploaded files"""
    filepath = UPLOAD_DIR / filename
    if not filepath.exists():
        raise HTTPException(404, "الملف غير موجود")
    content_types = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "gif": "image/gif", "webp": "image/webp", "mp4": "video/mp4", "webm": "video/webm"}
    ext = filename.rsplit(".", 1)[-1].lower()
    return FileResponse(str(filepath), media_type=content_types.get(ext, "application/octet-stream"))
