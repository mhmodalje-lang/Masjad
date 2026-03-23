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
from routers.baraka_market import router as baraka_market_router
from routers.sponsored_content import router as sponsored_content_router
from routers.rewards_store import router as rewards_store_router

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
api_router.include_router(baraka_market_router)
api_router.include_router(sponsored_content_router)
api_router.include_router(rewards_store_router)

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
        await db.baraka_wallets.create_index("user_id", unique=True)
        await db.baraka_transactions.create_index([("user_id", 1), ("created_at", -1)])
        await db.ads_config.create_index("id", unique=True)
        await db.data_deletion_requests.create_index([("created_at", -1)])
    except Exception as e:
        print(f"Index creation note: {e}")
    
    # Seed demo review account for App Store / Play Store review teams
    try:
        from deps import hash_password as _hash_pw
        demo_email = "review@azanhikaya.app"
        existing = await db.users.find_one({"email": demo_email})
        if not existing:
            demo_user = {
                "id": "review-demo-001",
                "email": demo_email,
                "name": "App Reviewer",
                "password_hash": _hash_pw("ReviewDemo2025!"),
                "provider": "email",
                "created_at": datetime.utcnow().isoformat(),
                "avatar": None,
            }
            await db.users.insert_one(demo_user)
            print("Demo review account created: review@azanhikaya.app / ReviewDemo2025!")
        else:
            print("Demo review account already exists")
    except Exception as e:
        print(f"Demo account seed note: {e}")

    # Seed default Islamic content so stories feed is not empty for store reviewers
    try:
        post_count = await db.posts.count_documents({})
        if post_count == 0:
            seed_posts = [
                {
                    "id": f"seed-{i}",
                    "author_id": "review-demo-001",
                    "author_name": "أذان وحكاية",
                    "author_avatar": None,
                    "title": p["title"],
                    "content": p["content"],
                    "category": p["cat"],
                    "media_type": "text",
                    "media_url": None,
                    "is_story": True,
                    "likes_count": 0,
                    "comments_count": 0,
                    "shares_count": 0,
                    "views_count": 0,
                    "created_at": datetime.utcnow().isoformat(),
                    "is_pinned": False,
                    "status": "active",
                }
                for i, p in enumerate([
                    {"title": "فضل الاستغفار", "content": "قال رسول الله ﷺ: «مَن لَزِمَ الاسْتِغْفَارَ جَعَلَ اللَّهُ لَهُ مِنْ كُلِّ ضِيقٍ مَخْرَجًا، وَمِنْ كُلِّ هَمٍّ فَرَجًا، وَرَزَقَهُ مِنْ حَيْثُ لا يَحْتَسِبُ»\n\nالاستغفار مفتاح الفرج وطريق الرزق. أكثروا من الاستغفار في كل حين.", "cat": "istighfar"},
                    {"title": "قصة إسلام عمر بن الخطاب", "content": "كان عمر بن الخطاب رضي الله عنه من أشد أعداء الإسلام، خرج يوماً يريد قتل النبي ﷺ، فلما سمع آيات من سورة طه تحول قلبه وأسلم.\n\nفكان إسلامه فتحاً للمسلمين. قال النبي ﷺ: «اللَّهُمَّ أَعِزَّ الإسلام بأحب العمرين إليك».", "cat": "sahaba"},
                    {"title": "آية الكرسي - أعظم آية", "content": "قال رسول الله ﷺ: «سيد آي القرآن آية الكرسي»\n\n﴿اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ﴾\n\nمن قرأها في ليلة لم يزل عليه من الله حافظ ولا يقربه شيطان حتى يصبح.", "cat": "quran"},
                    {"title": "قصة نبي الله يوسف عليه السلام", "content": "يوسف عليه السلام صبر على الابتلاءات: الجب، والسجن، والغربة. لكن الله نجاه ورفع قدره حتى صار عزيز مصر.\n\n﴿إِنَّهُ مَن يَتَّقِ وَيَصْبِرْ فَإِنَّ اللَّهَ لَا يُضِيعُ أَجْرَ الْمُحْسِنِينَ﴾", "cat": "prophets"},
                    {"title": "دعاء الهم والحزن", "content": "قال رسول الله ﷺ: «ما أصاب عبداً هم ولا حزن فقال:\n\nاللهم إني عبدك ابن عبدك ابن أمتك، ناصيتي بيدك، ماضٍ فيَّ حكمك، عدلٌ فيَّ قضاؤك\n\nإلا أذهب الله همه وأبدل حزنه فرحاً»", "cat": "general"},
                    {"title": "فضل قراءة القرآن", "content": "قال رسول الله ﷺ: «اقرَؤوا القرآن فإنه يأتي يوم القيامة شفيعاً لأصحابه»\n\nوقال ﷺ: «مَن قرأ حرفاً من كتاب الله فله به حسنة، والحسنة بعشر أمثالها»\n\nاجعلوا القرآن رفيقكم اليومي.", "cat": "quran"},
                ])
            ]
            await db.posts.insert_many(seed_posts)
            print(f"Seeded {len(seed_posts)} Islamic content posts")
    except Exception as e:
        print(f"Content seed note: {e}")

    # Pre-fetch Quran translations from official sources (background)
    try:
        import asyncio
        from quran_api_service import prefetch_kids_surahs
        asyncio.create_task(prefetch_kids_surahs())
    except Exception as e:
        print(f"Quran prefetch note: {e}")

@app.on_event("shutdown")
async def shutdown():
    client_db.close()
