"""
أذان وحكاية - Backend API
Modular Architecture - All routes split into domain routers.
"""
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime

from deps import db, client_db, logger

# Import all routers
from routers.auth import router as auth_router
from routers.social import router as social_router
from routers.upload import router as upload_router
from routers.economy import router as economy_router
from routers.marketplace import router as marketplace_router
from routers.ai import router as ai_router
from routers.prayer import router as prayer_router
from routers.quran_hadith import router as quran_hadith_router
from routers.admin import router as admin_router
from routers.islamic_tools import router as islamic_tools_router
from routers.stories import router as stories_router
from routers.misc import router as misc_router
from routers.arabic_academy import router as arabic_academy_router
from routers.live_streams import router as live_streams_router
from routers.kids_zone import router as kids_zone_router
from routers.kids_learn import router as kids_learn_router
from routers.kids_ai import router as kids_ai_router
from routers.gamification import router as gamification_router

# App
app = FastAPI(title="أذان وحكاية API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Main API router
api_router = APIRouter(prefix="/api")

@api_router.get("/")
async def root():
    return {"message": "أذان وحكاية API", "version": "3.0", "status": "running", "architecture": "modular"}

@api_router.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat(), "app": "أذان وحكاية"}

# Include all domain routers
api_router.include_router(auth_router)
api_router.include_router(social_router)
api_router.include_router(upload_router)
api_router.include_router(economy_router)
api_router.include_router(marketplace_router)
api_router.include_router(ai_router)
api_router.include_router(prayer_router)
api_router.include_router(quran_hadith_router)
api_router.include_router(admin_router)
api_router.include_router(islamic_tools_router)
api_router.include_router(stories_router)
api_router.include_router(misc_router)
api_router.include_router(arabic_academy_router)
api_router.include_router(live_streams_router)
api_router.include_router(kids_zone_router)
api_router.include_router(kids_learn_router)
api_router.include_router(kids_ai_router)
api_router.include_router(gamification_router)

app.include_router(api_router)

@app.on_event("startup")
async def create_indexes():
    """Create MongoDB indexes for performance"""
    try:
        await db.posts.create_index([("created_at", -1)])
        await db.posts.create_index([("category", 1), ("created_at", -1)])
        await db.posts.create_index("author_id")
        await db.likes.create_index([("post_id", 1), ("user_id", 1)], unique=True)
        await db.saves.create_index([("post_id", 1), ("user_id", 1)], unique=True)
        await db.comments.create_index([("post_id", 1), ("created_at", 1)])
        await db.follows.create_index([("follower_id", 1), ("following_id", 1)], unique=True)
        await db.users.create_index("email", unique=True)
        await db.users.create_index("id", unique=True)
        await db.wallets.create_index("user_id", unique=True)
        await db.gold_transactions.create_index([("user_id", 1), ("created_at", -1)])
        await db.store_items.create_index("category")
        await db.purchases.create_index([("user_id", 1), ("created_at", -1)])
        await db.memberships.create_index("user_id", unique=True)
    except Exception as e:
        print(f"Index creation note: {e}")

@app.on_event("shutdown")
async def shutdown():
    client_db.close()
