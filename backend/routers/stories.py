"""
Router: stories
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

router = APIRouter(tags=["Stories"])

STORY_CATEGORIES = [
    {"key": "general", "label": "عام", "labelKey": "storyCatGeneral", "emoji": "🌟", "icon": "star", "color": "#64748b"},
    {"key": "istighfar", "label": "قصص الاستغفار", "labelKey": "storyCatIstighfar", "emoji": "🤲", "icon": "sparkles", "color": "#10b981"},
    {"key": "sahaba", "label": "قصص الصحابة", "labelKey": "storyCatSahaba", "emoji": "⚔️", "icon": "sword", "color": "#f59e0b"},
    {"key": "quran", "label": "قصص القرآن", "labelKey": "storyCatQuran", "emoji": "📖", "icon": "book-open", "color": "#059669"},
    {"key": "prophets", "label": "قصص الأنبياء", "labelKey": "storyCatProphets", "emoji": "🕌", "icon": "building", "color": "#8b5cf6"},
    {"key": "ruqyah", "label": "قصص الرقية", "labelKey": "storyCatRuqyah", "emoji": "🛡️", "icon": "shield", "color": "#3b82f6"},
    {"key": "rizq", "label": "قصص الرزق", "labelKey": "storyCatRizq", "emoji": "💎", "icon": "gem", "color": "#eab308"},
    {"key": "tawba", "label": "قصص التوبة", "labelKey": "storyCatTawba", "emoji": "💧", "icon": "droplet", "color": "#22c55e"},
    {"key": "miracles", "label": "معجزات وعبر", "labelKey": "storyCatMiracles", "emoji": "✨", "icon": "sparkles", "color": "#6366f1"},
    {"key": "embed", "label": "فيديوهات", "labelKey": "storyCatEmbed", "emoji": "🎬", "icon": "film", "color": "#ef4444"},
]

@router.get("/stories/categories")
async def get_story_categories():
    return {"categories": STORY_CATEGORIES}

class CreateStoryRequest(BaseModel):
    title: Optional[str] = None
    content: str = Field(default="", max_length=10000)
    category: str = "istighfar"
    media_type: str = "text"  # text, image, video, embed
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    embed_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

@router.post("/stories/create")
async def create_story(data: CreateStoryRequest, user: dict = Depends(get_user)):
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول للنشر")
    if not data.content.strip() and not data.image_url and not data.video_url and not data.embed_url:
        raise HTTPException(400, "يجب إضافة محتوى أو وسائط")
    post_id = str(uuid.uuid4())
    story = {
        "id": post_id,
        "author_id": user["id"],
        "author_name": user.get("name", "مستخدم"),
        "author_avatar": user.get("avatar"),
        "title": data.title or "",
        "content": data.content or data.title or "",
        "category": data.category,
        "media_type": data.media_type,
        "image_url": data.image_url,
        "video_url": data.video_url,
        "embed_url": data.embed_url,
        "thumbnail_url": data.thumbnail_url,
        "is_embed": data.media_type == "embed",
        "views_count": 0,
        "created_at": datetime.utcnow().isoformat(),
        "shares_count": 0,
        "is_story": True,
    }
    await db.posts.insert_one(story)
    story.pop("_id", None)
    story["liked"] = False
    story["saved"] = False
    story["likes_count"] = 0
    story["comments_count"] = 0
    return {"story": story}

@router.get("/stories/list")
async def list_stories(category: str = "all", page: int = 1, limit: int = 20, user: dict = Depends(get_user)):
    query = {"is_story": True}
    if category != "all":
        query["category"] = category
    skip = (page - 1) * limit
    cursor = db.posts.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    stories = await cursor.to_list(length=limit)
    total = await db.posts.count_documents(query)
    # Enrich
    post_ids = [s["id"] for s in stories]
    user_id = user["id"] if user else None
    likes_set, saves_set = set(), set()
    if user_id and post_ids:
        ul = await db.likes.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        likes_set = {d["post_id"] for d in ul}
        us = await db.saves.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        saves_set = {d["post_id"] for d in us}
    likes_counts, comments_counts = {}, {}
    if post_ids:
        async for doc in db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            likes_counts[doc["_id"]] = doc["c"]
        async for doc in db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            comments_counts[doc["_id"]] = doc["c"]
    for s in stories:
        pid = s["id"]
        s["liked"] = pid in likes_set
        s["saved"] = pid in saves_set
        s["likes_count"] = likes_counts.get(pid, 0)
        s["comments_count"] = comments_counts.get(pid, 0)
        # Ensure thumbnail_url field is always present for API consistency
        if "thumbnail_url" not in s:
            s["thumbnail_url"] = None
    return {"stories": stories, "total": total, "page": page, "has_more": skip + limit < total}

@router.get("/stories/my-saved")
async def get_my_saved_stories(limit: int = 50, user: dict = Depends(get_user)):
    """Get stories saved by current user"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    saved_docs = await db.saves.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    post_ids = [s["post_id"] for s in saved_docs]
    if not post_ids:
        return {"stories": []}
    stories = []
    for pid in post_ids:
        story = await db.posts.find_one({"id": pid, "is_story": True}, {"_id": 0})
        if story:
            story["liked"] = bool(await db.likes.find_one({"post_id": pid, "user_id": user["id"]}))
            story["saved"] = True
            story["likes_count"] = await db.likes.count_documents({"post_id": pid})
            story["comments_count"] = await db.comments.count_documents({"post_id": pid})
            stories.append(story)
    return {"stories": stories}

@router.get("/stories/my-liked")
async def get_my_liked_stories(limit: int = 50, user: dict = Depends(get_user)):
    """Get stories liked by current user"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    liked_docs = await db.likes.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    post_ids = [doc["post_id"] for doc in liked_docs]
    if not post_ids:
        return {"stories": []}
    stories = []
    for pid in post_ids:
        story = await db.posts.find_one({"id": pid, "is_story": True}, {"_id": 0})
        if story:
            story["liked"] = True
            story["saved"] = bool(await db.saves.find_one({"post_id": pid, "user_id": user["id"]}))
            story["likes_count"] = await db.likes.count_documents({"post_id": pid})
            story["comments_count"] = await db.comments.count_documents({"post_id": pid})
            stories.append(story)
    return {"stories": stories}

@router.post("/stories/auto-categorize")
async def auto_categorize_story(data: dict, user: dict = Depends(get_user)):
    """AI auto-categorize a story based on title and content"""
    if not user:
        raise HTTPException(401, "يجب تسجيل الدخول")
    title = data.get("title", "")
    content = data.get("content", "")
    if not title and not content:
        return {"category": "general"}
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY
        ).with_model("gemini", "gemini-2.0-flash")
        categories_str = ", ".join([f"{c['key']}({c['label']})" for c in STORY_CATEGORIES if c['key'] != 'embed'])
        prompt = f"""صنف هذا المحتوى الإسلامي في واحدة من هذه الفئات فقط:
{categories_str}

العنوان: {title}
المحتوى: {content[:500]}

أجب بكلمة واحدة فقط هي مفتاح الفئة (مثل: istighfar, sahaba, quran, prophets, ruqyah, rizq, tawba, miracles, general)"""
        response = await chat.chat([UserMessage(content=prompt)])
        cat_key = response.content.strip().lower().replace('"', '').replace("'", "")
        valid_keys = [c["key"] for c in STORY_CATEGORIES if c["key"] != "embed"]
        if cat_key not in valid_keys:
            cat_key = "general"
        return {"category": cat_key}
    except Exception as e:
        logging.error(f"AI categorize error: {e}")
        return {"category": "general"}

@router.get("/stories/list-translated")
async def list_stories_translated(
    category: str = "all",
    page: int = 1,
    limit: int = 20,
    language: str = Query("ar"),
    user: dict = Depends(get_user)
):
    """List stories with translated content for the requested language."""
    query = {"is_story": True}
    if category != "all":
        query["category"] = category
    skip = (page - 1) * limit
    cursor = db.posts.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    stories = await cursor.to_list(length=limit)
    total = await db.posts.count_documents(query)
    
    # Enrich with likes/saves/comments
    post_ids = [s["id"] for s in stories]
    user_id = user["id"] if user else None
    likes_set, saves_set = set(), set()
    if user_id and post_ids:
        ul = await db.likes.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        likes_set = {d["post_id"] for d in ul}
        us = await db.saves.find({"post_id": {"$in": post_ids}, "user_id": user_id}, {"_id": 0, "post_id": 1}).to_list(None)
        saves_set = {d["post_id"] for d in us}
    likes_counts, comments_counts = {}, {}
    if post_ids:
        async for doc in db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            likes_counts[doc["_id"]] = doc["c"]
        async for doc in db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            comments_counts[doc["_id"]] = doc["c"]
    
    for s in stories:
        pid = s["id"]
        s["liked"] = pid in likes_set
        s["saved"] = pid in saves_set
        s["likes_count"] = likes_counts.get(pid, 0)
        s["comments_count"] = comments_counts.get(pid, 0)
        # Ensure thumbnail_url field is always present for API consistency
        if "thumbnail_url" not in s:
            s["thumbnail_url"] = None
        # Apply translation if available and language is not source
        if language != "ar" and language in s.get("translations", {}):
            trans = s["translations"][language]
            s["title"] = trans.get("title", s.get("title", ""))
            s["content"] = trans.get("content", s.get("content", ""))
        s.pop("translations", None)  # Don't send all translations to client
    
    return {"stories": stories, "total": total, "page": page, "has_more": skip + limit < total}

@router.get("/stories/{story_id}")
async def get_story(story_id: str, user: dict = Depends(get_user)):
    story = await db.posts.find_one({"id": story_id}, {"_id": 0})
    if not story:
        raise HTTPException(404, "القصة غير موجودة")
    # Increment view
    await db.posts.update_one({"id": story_id}, {"$inc": {"views_count": 1}})
    story["views_count"] = story.get("views_count", 0) + 1
    # Enrich
    user_id = user["id"] if user else None
    story["liked"] = bool(await db.likes.find_one({"post_id": story_id, "user_id": user_id})) if user_id else False
    story["saved"] = bool(await db.saves.find_one({"post_id": story_id, "user_id": user_id})) if user_id else False
    story["likes_count"] = await db.likes.count_documents({"post_id": story_id})
    story["comments_count"] = await db.comments.count_documents({"post_id": story_id})
    return {"story": story}

@router.post("/stories/{story_id}/view")
async def track_story_view(story_id: str):
    await db.posts.update_one({"id": story_id}, {"$inc": {"views_count": 1}})
    return {"success": True}

@router.get("/ads/placement/{position}")
async def get_ads_by_placement(position: str):
    """Get active ads for a specific placement position"""
    query = {"enabled": True, "$or": [{"placement": position}, {"placement": "all"}]}
    ads = await db.ad_placements.find(query, {"_id": 0}).sort("priority", -1).to_list(5)
    return {"ads": ads}

@router.get("/stories/feed/most-viewed")
async def most_viewed_stories(limit: int = 20, user: dict = Depends(get_user)):
    pipeline = [
        {"$match": {"is_story": True}},
        {"$lookup": {"from": "likes", "localField": "id", "foreignField": "post_id", "as": "likes_data"}},
        {"$lookup": {"from": "comments", "localField": "id", "foreignField": "post_id", "as": "comments_data"}},
        {"$addFields": {
            "likes_count": {"$size": "$likes_data"},
            "comments_count": {"$size": "$comments_data"},
        }},
        {"$project": {"_id": 0, "likes_data": 0, "comments_data": 0}},
        {"$sort": {"views_count": -1, "created_at": -1}},
        {"$limit": limit}
    ]
    stories = []
    async for doc in db.posts.aggregate(pipeline):
        doc["liked"] = False
        doc["saved"] = False
        stories.append(doc)
    # Enrich user-specific
    if user:
        pids = [s["id"] for s in stories]
        if pids:
            ul = await db.likes.find({"post_id": {"$in": pids}, "user_id": user["id"]}, {"_id": 0, "post_id": 1}).to_list(None)
            ls = {d["post_id"] for d in ul}
            for s in stories:
                s["liked"] = s["id"] in ls
    return {"stories": stories}

@router.get("/stories/feed/most-interacted")
async def most_interacted_stories(limit: int = 20, user: dict = Depends(get_user)):
    pipeline = [
        {"$match": {"is_story": True}},
        {"$lookup": {"from": "likes", "localField": "id", "foreignField": "post_id", "as": "likes_data"}},
        {"$lookup": {"from": "comments", "localField": "id", "foreignField": "post_id", "as": "comments_data"}},
        {"$addFields": {
            "likes_count": {"$size": "$likes_data"},
            "comments_count": {"$size": "$comments_data"},
            "engagement": {"$add": [{"$multiply": [{"$size": "$likes_data"}, 2]}, {"$multiply": [{"$size": "$comments_data"}, 3]}, {"$ifNull": ["$views_count", 0]}]}
        }},
        {"$project": {"_id": 0, "likes_data": 0, "comments_data": 0}},
        {"$sort": {"engagement": -1, "created_at": -1}},
        {"$limit": limit}
    ]
    stories = []
    async for doc in db.posts.aggregate(pipeline):
        doc["liked"] = False
        doc["saved"] = False
        stories.append(doc)
    if user:
        pids = [s["id"] for s in stories]
        if pids:
            ul = await db.likes.find({"post_id": {"$in": pids}, "user_id": user["id"]}, {"_id": 0, "post_id": 1}).to_list(None)
            ls = {d["post_id"] for d in ul}
            for s in stories:
                s["liked"] = s["id"] in ls
    return {"stories": stories}

@router.get("/stories/feed/search")
async def search_stories(q: str = Query("", min_length=1), limit: int = 30, user: dict = Depends(get_user)):
    if not q.strip():
        return {"stories": []}
    search_regex = {"$regex": q.strip(), "$options": "i"}
    query = {"is_story": True, "$or": [{"title": search_regex}, {"content": search_regex}, {"author_name": search_regex}, {"category": search_regex}]}
    cursor = db.posts.find(query, {"_id": 0}).sort("created_at", -1).limit(limit)
    stories = await cursor.to_list(length=limit)
    post_ids = [s["id"] for s in stories]
    likes_counts, comments_counts = {}, {}
    if post_ids:
        async for doc in db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            likes_counts[doc["_id"]] = doc["c"]
        async for doc in db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            comments_counts[doc["_id"]] = doc["c"]
    for s in stories:
        s["likes_count"] = likes_counts.get(s["id"], 0)
        s["comments_count"] = comments_counts.get(s["id"], 0)
        s["liked"] = False
        s["saved"] = False
    return {"stories": stories}

# ==================== ADMIN EMBED CONTENT (محتوى مضمن) ====================

class EmbedContentRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = ""
    embed_url: str = Field(..., min_length=5)
    platform: str = "youtube"  # youtube, dailymotion, vimeo, etc.
    category: str = "general"
    thumbnail_url: Optional[str] = None

@router.post("/stories/voice-search")
async def voice_search_stories(data: dict, user: dict = Depends(get_user)):
    """AI-powered voice search - analyzes query and finds matching stories"""
    query_text = data.get("query", "").strip()
    if not query_text:
        return {"stories": [], "ai_response": ""}
    
    # Use Gemini to understand the query and extract search terms
    ai_response = ""
    search_terms = [query_text]
    
    try:
        gemini_key = os.environ.get("GEMINI_API_KEY", "")
        if gemini_key:
            import httpx
            prompt = f"""أنت مساعد بحث في تطبيق إسلامي. المستخدم يبحث عن: "{query_text}"

استخرج كلمات البحث الرئيسية من هذا الطلب وأعطني:
1. قائمة بـ 3-5 كلمات مفتاحية للبحث (مفصولة بفاصلة)
2. رد قصير ومفيد للمستخدم

أجب بصيغة JSON فقط:
{{"keywords": ["كلمة1", "كلمة2"], "response": "رد قصير"}}"""
            
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}",
                    json={"contents": [{"parts": [{"text": prompt}]}]}
                )
                if resp.status_code == 200:
                    text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                    import re as re_module
                    json_match = re_module.search(r'\{.*\}', text, re_module.DOTALL)
                    if json_match:
                        import json as json_module
                        parsed = json_module.loads(json_match.group())
                        search_terms = parsed.get("keywords", [query_text])
                        ai_response = parsed.get("response", "")
    except Exception as e:
        logging.error(f"Voice search AI error: {e}")
    
    # Search stories using extracted keywords
    or_conditions = []
    for term in search_terms:
        term = term.strip()
        if term:
            regex = {"$regex": term, "$options": "i"}
            or_conditions.extend([{"title": regex}, {"content": regex}, {"author_name": regex}, {"category": regex}])
    
    if not or_conditions:
        or_conditions = [{"title": {"$regex": query_text, "$options": "i"}}, {"content": {"$regex": query_text, "$options": "i"}}]
    
    query_filter = {"is_story": True, "$or": or_conditions}
    cursor = db.posts.find(query_filter, {"_id": 0}).sort("views_count", -1).limit(30)
    stories = await cursor.to_list(length=30)
    
    # Add likes/comments counts
    post_ids = [s["id"] for s in stories]
    if post_ids:
        likes_counts = {}
        async for doc in db.likes.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            likes_counts[doc["_id"]] = doc["c"]
        comments_counts = {}
        async for doc in db.comments.aggregate([{"$match": {"post_id": {"$in": post_ids}}}, {"$group": {"_id": "$post_id", "c": {"$sum": 1}}}]):
            comments_counts[doc["_id"]] = doc["c"]
        for s in stories:
            s["likes_count"] = likes_counts.get(s["id"], 0)
            s["comments_count"] = comments_counts.get(s["id"], 0)
            s["liked"] = False
            s["saved"] = False
    
    return {"stories": stories, "ai_response": ai_response, "keywords": search_terms}

# ==================== ADMIN MANAGEMENT (إدارة التطبيق) ====================

ADMIN_EMAILS = ['mohammadalrejab@gmail.com']

# Supported languages for translation
SUPPORTED_LANGUAGES = ["ar", "en", "de", "ru", "fr", "tr", "sv", "nl", "el"]

# Language names mapping
LANGUAGE_NAMES = {
    "ar": "Arabic",
    "en": "English", 
    "de": "German",
    "ru": "Russian",
    "fr": "French",
    "tr": "Turkish",
    "sv": "Swedish",
    "nl": "Dutch",
    "el": "Greek"
}

async def translate_text_ai(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text using OpenAI GPT with Islamic context."""
    if not EMERGENT_LLM_KEY or source_lang == target_lang:
        return text
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"translate-{uuid.uuid4().hex[:8]}",
            system_message=f"You are an expert Islamic text translator. Translate the given text from {LANGUAGE_NAMES.get(source_lang, source_lang)} to {LANGUAGE_NAMES.get(target_lang, target_lang)}. Preserve Islamic terminology and spiritual meaning. Return ONLY the translated text, nothing else."
        )
        response = await chat.send_message(UserMessage(text=text))
        return response.strip()
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text

@router.post("/translate/story")
async def translate_story_content(
    story_id: str = Query(...),
    target_lang: str = Query(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    user: dict = Depends(get_user)
):
    """Translate a story's title and content to the target language and store it."""
    if target_lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(400, f"Unsupported language: {target_lang}")
    
    story = await db.posts.find_one({"id": story_id, "is_story": True}, {"_id": 0})
    if not story:
        raise HTTPException(404, "Story not found")
    
    # Check if translation already exists
    existing = story.get("translations", {}).get(target_lang)
    if existing:
        return {"translated": True, "title": existing.get("title", ""), "content": existing.get("content", "")}
    
    # Detect source language (assume Arabic if contains Arabic chars)
    source_lang = "ar" if re.search(r'[\u0600-\u06FF]', story.get("content", "")) else "en"
    
    title = await translate_text_ai(story.get("title", ""), source_lang, target_lang) if story.get("title") else ""
    content = await translate_text_ai(story.get("content", ""), source_lang, target_lang)
    
    # Store translation in DB
    await db.posts.update_one(
        {"id": story_id},
        {"$set": {f"translations.{target_lang}": {"title": title, "content": content}}}
    )
    
    return {"translated": True, "title": title, "content": content}



@router.post("/stories/batch-translate")
async def batch_translate_stories(
    target_lang: str = Query(...),
    user: dict = Depends(get_user)
):
    """Batch translate all stories to a target language. Admin/background task."""
    if target_lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(400, f"Unsupported language: {target_lang}")
    
    # Find stories without this language translation
    stories = await db.posts.find(
        {"is_story": True, f"translations.{target_lang}": {"$exists": False}},
        {"_id": 0, "id": 1, "title": 1, "content": 1}
    ).to_list(100)
    
    if not stories:
        return {"message": f"All stories already translated to {target_lang}", "count": 0}
    
    translated_count = 0
    for story in stories:
        try:
            source_lang = "ar" if re.search(r'[\u0600-\u06FF]', story.get("content", "")) else "en"
            title = await translate_text_ai(story.get("title", ""), source_lang, target_lang) if story.get("title") else ""
            content = await translate_text_ai(story.get("content", ""), source_lang, target_lang)
            await db.posts.update_one(
                {"id": story["id"]},
                {"$set": {f"translations.{target_lang}": {"title": title, "content": content}}}
            )
            translated_count += 1
        except Exception as e:
            logger.error(f"Failed to translate story {story['id']}: {e}")
    
    return {"message": f"Translated {translated_count} stories to {target_lang}", "count": translated_count}



# ==================== KIDS ZONE - INFINITE GAME ENGINE (PCG) ====================

# Confusable phoneme pairs for adaptive difficulty
CONFUSABLE_PHONEMES = [
    (6, 7, "ح", "خ"),   # Ha vs Kha
    (12, 13, "س", "ش"), # Sin vs Shin
    (14, 15, "ص", "ض"), # Sad vs Dad
    (16, 17, "ط", "ظ"), # Tah vs Zah
    (8, 9, "د", "ذ"),   # Dal vs Dhal
    (4, 5, "ث", "ج"),   # Tha vs Jim
    (18, 19, "ع", "غ"), # Ain vs Ghain
    (26, 27, "ه", "و"), # Ha2 vs Waw
    (3, 16, "ت", "ط"),  # Ta vs emphatic Tah
    (8, 15, "د", "ض"),  # Dal vs emphatic Dad
]

# Difficulty tiers with thresholds
DIFFICULTY_TIERS = [
    {"name": "seedling", "min_xp": 0, "choices": 2, "time_bonus": 30, "brick_reward": 1},
    {"name": "sprout", "min_xp": 100, "choices": 3, "time_bonus": 25, "brick_reward": 2},
    {"name": "sapling", "min_xp": 300, "choices": 4, "time_bonus": 20, "brick_reward": 3},
    {"name": "tree", "min_xp": 600, "choices": 4, "time_bonus": 15, "brick_reward": 4},
    {"name": "forest", "min_xp": 1000, "choices": 5, "time_bonus": 12, "brick_reward": 5},
]

# Virtual Mosque building stages
MOSQUE_STAGES = [
    {"stage": 1, "name": "foundation", "bricks_needed": 10, "emoji": "🧱"},
    {"stage": 2, "name": "walls", "bricks_needed": 25, "emoji": "🏗️"},
    {"stage": 3, "name": "dome", "bricks_needed": 50, "emoji": "🕌"},
    {"stage": 4, "name": "minaret", "bricks_needed": 80, "emoji": "🗼"},
    {"stage": 5, "name": "garden", "bricks_needed": 120, "emoji": "🌳"},
    {"stage": 6, "name": "golden_dome", "bricks_needed": 200, "emoji": "✨"},
]



# ═══════════════════════════════════════════════════════════════
# DIGITAL SHIELD (درع الوعي) — AI Safety, Privacy, Cyber-Ethics
# ═══════════════════════════════════════════════════════════════

from data.digital_shield_content import DIGITAL_SHIELD_MODULES, DIGITAL_SHIELD_LESSONS

@router.get("/digital-shield/overview")
async def digital_shield_overview(locale: str = "ar"):
    """Get Digital Shield overview — 3 modules, 30 lessons."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    if locale == "de-AT":
        lang = "de"

    modules = []
    for m in DIGITAL_SHIELD_MODULES:
        start, end = m["lessons_range"]
        modules.append({
            "id": m["id"],
            "emoji": m["emoji"],
            "color": m["color"],
            "title": m["title"].get(lang, m["title"]["en"]),
            "description": m["desc"].get(lang, m["desc"]["en"]),
            "lesson_start": start,
            "lesson_end": end,
            "total_lessons": end - start + 1,
        })

    return {
        "success": True,
        "title": {
            "ar": "درع الوعي",
            "en": "Digital Shield",
            "de": "Digitaler Schutzschild",
            "fr": "Bouclier Numérique",
            "tr": "Dijital Kalkan",
            "ru": "Цифровой Щит",
            "sv": "Digital Sköld",
            "nl": "Digitaal Schild",
            "el": "Ψηφιακή Ασπίδα",
        }.get(lang, "Digital Shield"),
        "subtitle": {
            "ar": "٣٠ درساً في سلامة الذكاء الاصطناعي والخصوصية والأخلاق الرقمية",
            "en": "30 Lessons on AI Safety, Privacy & Cyber-Ethics",
            "de": "30 Lektionen über KI-Sicherheit, Privatsphäre & Cyber-Ethik",
            "fr": "30 leçons sur la sécurité IA, la vie privée et la cyber-éthique",
            "tr": "Yapay Zekâ Güvenliği, Gizlilik ve Siber Ahlak Üzerine 30 Ders",
            "ru": "30 уроков по безопасности ИИ, приватности и кибер-этике",
            "sv": "30 lektioner om AI-säkerhet, integritet och cyberetik",
            "nl": "30 lessen over AI-veiligheid, privacy en cyber-ethiek",
            "el": "30 μαθήματα για ασφάλεια ΤΝ, απόρρητο και κυβερνο-ηθική",
        }.get(lang, "30 Lessons on AI Safety, Privacy & Cyber-Ethics"),
        "modules": modules,
        "total_lessons": 30,
        "language": lang,
    }


@router.get("/digital-shield/lesson/{lesson_id}")
async def digital_shield_lesson(lesson_id: int, locale: str = "ar"):
    """Get a specific Digital Shield lesson (1-30)."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    if locale == "de-AT":
        lang = "de"

    lesson = next((l for l in DIGITAL_SHIELD_LESSONS if l["id"] == lesson_id), None)
    if not lesson:
        return {"success": False, "error": "Lesson not found", "lesson_id": lesson_id}

    # Find the module
    module = next((m for m in DIGITAL_SHIELD_MODULES if m["lessons_range"][0] <= lesson_id <= m["lessons_range"][1]), None)

    return {
        "success": True,
        "lesson": {
            "id": lesson["id"],
            "module": lesson["module"],
            "module_title": module["title"].get(lang, module["title"]["en"]) if module else "",
            "module_emoji": module["emoji"] if module else "",
            "module_color": module["color"] if module else "",
            "emoji": lesson["emoji"],
            "title": lesson["title"].get(lang, lesson["title"]["en"]),
            "content": lesson["content"].get(lang, lesson["content"]["en"]),
            "islamic_reference": lesson["islamic_ref"].get(lang, lesson["islamic_ref"]["en"]),
            "moral": lesson["moral"].get(lang, lesson["moral"]["en"]),
        },
        "language": lang,
        "total_lessons": 30,
        "has_next": lesson_id < 30,
        "has_prev": lesson_id > 1,
    }


@router.get("/digital-shield/module/{module_id}")
async def digital_shield_module_lessons(module_id: int, locale: str = "ar"):
    """Get all lessons in a specific Digital Shield module (1-3)."""
    lang = locale if locale in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] else "en"
    if locale == "de-AT":
        lang = "de"

    if module_id < 1 or module_id > 3:
        return {"success": False, "error": "Module not found. Valid: 1, 2, 3"}

    module = DIGITAL_SHIELD_MODULES[module_id - 1]
    start, end = module["lessons_range"]

    lessons = []
    for l in DIGITAL_SHIELD_LESSONS:
        if start <= l["id"] <= end:
            lessons.append({
                "id": l["id"],
                "emoji": l["emoji"],
                "title": l["title"].get(lang, l["title"]["en"]),
                "content_preview": l["content"].get(lang, l["content"]["en"])[:150] + "...",
            })

    return {
        "success": True,
        "module": {
            "id": module_id,
            "emoji": module["emoji"],
            "color": module["color"],
            "title": module["title"].get(lang, module["title"]["en"]),
            "description": module["desc"].get(lang, module["desc"]["en"]),
        },
        "lessons": lessons,
        "total": len(lessons),
        "language": lang,
    }
