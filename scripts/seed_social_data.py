"""
Seed social data: users, posts (text/image/video), likes, comments, follows
to test reels, trending, and video feeds.
"""
import asyncio
import os
import sys
import uuid
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')

# Sample data
SAMPLE_USERS = [
    {"name": "أحمد محمد", "email": "ahmed@test.com", "avatar": None},
    {"name": "فاطمة علي", "email": "fatima@test.com", "avatar": None},
    {"name": "عمر خالد", "email": "omar@test.com", "avatar": None},
    {"name": "خديجة حسن", "email": "khadija@test.com", "avatar": None},
    {"name": "يوسف سعيد", "email": "yusuf@test.com", "avatar": None},
    {"name": "مريم أحمد", "email": "maryam@test.com", "avatar": None},
    {"name": "إبراهيم عبدالله", "email": "ibrahim@test.com", "avatar": None},
    {"name": "نور الدين", "email": "nour@test.com", "avatar": None},
]

ARABIC_TEXTS = [
    "اتفق وبشدة مع المقولة: عاشروا من تحبون سرا فالعلن لا خير فيه",
    "قال رسول الله ﷺ: إنما الأعمال بالنيات وإنما لكل امرئ ما نوى",
    "اللهم إني أسألك العفو والعافية في الدنيا والآخرة",
    "سبحان الله وبحمده سبحان الله العظيم",
    "ربِّ اشرح لي صدري ويسّر لي أمري",
    "الحمد لله على كل حال، نعمة الإيمان أعظم نعمة",
    "من قال لا إله إلا الله وحده لا شريك له، له الملك وله الحمد",
    "اللهم صلِّ وسلّم على نبينا محمد ﷺ",
    "كن مع الله يكن معك، توكل على الله وكفى بالله وكيلا",
    "قال الله تعالى: وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ",
    "لا تحزن إن الله معنا، الصبر مفتاح الفرج",
    "اذكروا الله يذكركم، واشكروا له ولا تكفرون",
    "رب اغفر لي ولوالدي ولجميع المسلمين والمسلمات",
    "الدنيا مزرعة الآخرة، ازرع خيراً تحصد خيراً",
    "يا رب أسألك راحة البال وصلاح الحال",
]

STORY_TITLES = [
    "قصة توبة صادقة",
    "من أجمل قصص الصحابة",
    "عجائب الاستغفار",
    "دعاء مستجاب",
    "حكمة اليوم",
    "تأملات قرآنية",
    "درس مؤثر",
    "قصة ملهمة",
]

CATEGORIES = ["general", "istighfar", "sahaba", "quran", "prophets", "ruqyah", "rizq", "tawba", "miracles"]

COMMENTS = [
    "ما شاء الله 🤲",
    "جزاك الله خيراً",
    "سبحان الله",
    "بارك الله فيك",
    "اللهم آمين",
    "كلام جميل جداً ❤️",
    "نفع الله بك",
    "رائع! شكراً للمشاركة",
    "اللهم صلّ على محمد ﷺ",
    "حقيقي كلام معبر",
    "الله يجزاك خير",
    "تبارك الرحمن",
]

# Sample YouTube embed URLs for video content
SAMPLE_EMBED_URLS = [
    "https://www.youtube.com/watch?v=gAzq1ch5RnY",
    "https://www.youtube.com/watch?v=VO359jOBfCk",
    "https://www.youtube.com/watch?v=jBYrnVptmCo",
    "https://www.youtube.com/watch?v=wQMmHBBl3cA",
    "https://www.youtube.com/watch?v=o4N9vYUFHzA",
]


async def seed():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    # Check if already seeded
    existing = await db.posts.count_documents({})
    if existing > 0:
        print(f"Database already has {existing} posts. Skipping seed.")
        return

    print("Seeding social data...")

    # 1. Create users
    users = []
    for u_data in SAMPLE_USERS:
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "name": u_data["name"],
            "email": u_data["email"],
            "avatar": u_data.get("avatar"),
            "password_hash": "dummy_hash:dummy_dk",  # Not real, just for testing
            "created_at": (datetime.utcnow() - timedelta(days=random.randint(10, 90))).isoformat(),
            "points": random.randint(50, 500),
        }
        await db.users.insert_one(user)
        users.append(user)
        print(f"  Created user: {user['name']} ({user_id})")

    # 2. Create posts (mix of text, image stories, video, embeds)
    posts = []
    now = datetime.utcnow()

    # Text-only stories
    for i in range(8):
        author = random.choice(users)
        post_id = str(uuid.uuid4())
        post = {
            "id": post_id,
            "author_id": author["id"],
            "author_name": author["name"],
            "author_avatar": author.get("avatar"),
            "title": random.choice(STORY_TITLES),
            "content": random.choice(ARABIC_TEXTS),
            "category": random.choice(CATEGORIES),
            "media_type": "text",
            "content_type": "text",
            "image_url": None,
            "video_url": None,
            "embed_url": None,
            "thumbnail_url": None,
            "is_embed": False,
            "is_story": True,
            "views_count": random.randint(10, 500),
            "shares_count": random.randint(0, 50),
            "created_at": (now - timedelta(hours=random.randint(1, 72))).isoformat(),
        }
        await db.posts.insert_one(post)
        posts.append(post)

    # Image stories (using placeholder images)
    image_urls = [
        "https://images.unsplash.com/photo-1564769625905-50e93615e769?w=600",
        "https://images.unsplash.com/photo-1542816417-0983c9c9ad53?w=600",
        "https://images.unsplash.com/photo-1519817650390-64a93db51149?w=600",
        "https://images.unsplash.com/photo-1519818187420-8e49de7adeef?w=600",
    ]
    for i in range(4):
        author = random.choice(users)
        post_id = str(uuid.uuid4())
        post = {
            "id": post_id,
            "author_id": author["id"],
            "author_name": author["name"],
            "author_avatar": author.get("avatar"),
            "title": random.choice(STORY_TITLES),
            "content": random.choice(ARABIC_TEXTS),
            "category": random.choice(CATEGORIES),
            "media_type": "image",
            "content_type": "image",
            "image_url": image_urls[i % len(image_urls)],
            "video_url": None,
            "embed_url": None,
            "thumbnail_url": None,
            "is_embed": False,
            "is_story": True,
            "views_count": random.randint(50, 1000),
            "shares_count": random.randint(5, 100),
            "created_at": (now - timedelta(hours=random.randint(1, 48))).isoformat(),
        }
        await db.posts.insert_one(post)
        posts.append(post)

    # Video embeds (YouTube)
    for i, url in enumerate(SAMPLE_EMBED_URLS):
        author = random.choice(users)
        post_id = str(uuid.uuid4())
        # Extract YouTube ID for thumbnail
        yt_id = url.split("v=")[-1] if "v=" in url else ""
        post = {
            "id": post_id,
            "author_id": author["id"],
            "author_name": author["name"],
            "author_avatar": author.get("avatar"),
            "title": random.choice(STORY_TITLES),
            "content": random.choice(ARABIC_TEXTS),
            "category": "embed",
            "media_type": "embed",
            "content_type": "video_short",
            "image_url": None,
            "video_url": None,
            "embed_url": url,
            "thumbnail_url": f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg" if yt_id else None,
            "is_embed": True,
            "is_story": True,
            "views_count": random.randint(100, 5000),
            "shares_count": random.randint(10, 200),
            "created_at": (now - timedelta(hours=random.randint(1, 96))).isoformat(),
        }
        await db.posts.insert_one(post)
        posts.append(post)

    # Social posts (non-story, for sohba feed)
    for i in range(6):
        author = random.choice(users)
        post_id = str(uuid.uuid4())
        post = {
            "id": post_id,
            "author_id": author["id"],
            "author_name": author["name"],
            "author_avatar": author.get("avatar"),
            "content": random.choice(ARABIC_TEXTS),
            "category": random.choice(["general", "istighfar", "quran"]),
            "content_type": "text",
            "image_url": None,
            "video_url": None,
            "thumbnail_url": None,
            "shares_count": random.randint(0, 30),
            "created_at": (now - timedelta(hours=random.randint(1, 48))).isoformat(),
        }
        await db.posts.insert_one(post)
        posts.append(post)

    print(f"  Created {len(posts)} posts")

    # 3. Create likes (random likes for engagement/trending)
    likes_count = 0
    for post in posts:
        # Random number of likes per post
        num_likes = random.randint(2, len(users))
        likers = random.sample(users, min(num_likes, len(users)))
        for liker in likers:
            if liker["id"] != post["author_id"]:  # Don't self-like
                like = {
                    "id": str(uuid.uuid4()),
                    "post_id": post["id"],
                    "user_id": liker["id"],
                    "created_at": datetime.utcnow().isoformat(),
                }
                await db.likes.insert_one(like)
                likes_count += 1

    print(f"  Created {likes_count} likes")

    # 4. Create comments
    comments_count = 0
    for post in posts:
        num_comments = random.randint(0, 5)
        commenters = random.sample(users, min(num_comments + 1, len(users)))
        for commenter in commenters[:num_comments]:
            comment = {
                "id": str(uuid.uuid4()),
                "post_id": post["id"],
                "author_id": commenter["id"],
                "author_name": commenter["name"],
                "author_avatar": commenter.get("avatar"),
                "content": random.choice(COMMENTS),
                "created_at": (datetime.utcnow() - timedelta(minutes=random.randint(5, 300))).isoformat(),
            }
            await db.comments.insert_one(comment)
            comments_count += 1

    print(f"  Created {comments_count} comments")

    # 5. Create follows (random follows between users)
    follows_count = 0
    for user in users:
        # Each user follows 2-5 other users
        num_follows = random.randint(2, 5)
        targets = [u for u in users if u["id"] != user["id"]]
        for target in random.sample(targets, min(num_follows, len(targets))):
            follow = {
                "id": str(uuid.uuid4()),
                "follower_id": user["id"],
                "following_id": target["id"],
                "created_at": datetime.utcnow().isoformat(),
            }
            await db.follows.insert_one(follow)
            follows_count += 1

    print(f"  Created {follows_count} follows")
    print("\n✅ Seed complete!")
    print(f"  Users: {len(users)}")
    print(f"  Posts: {len(posts)}")
    print(f"  Likes: {likes_count}")
    print(f"  Comments: {comments_count}")
    print(f"  Follows: {follows_count}")


if __name__ == "__main__":
    asyncio.run(seed())
