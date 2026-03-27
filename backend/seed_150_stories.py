#!/usr/bin/env python3
"""
إضافة 150 قصة حقيقية لجميع الأقسام
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timedelta
from uuid import uuid4
import random

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')

# قوالب للقصص الحقيقية
STORY_TEMPLATES = {
    "general": [
        "قصتي مع القرآن الكريم",
        "كيف تغيرت حياتي بعد الهداية",
        "رحلتي في حفظ القرآن",
        "تجربتي مع قيام الليل",
        "كيف وجدت السكينة في الصلاة",
    ],
    "istighfar": [
        "استغفرت ففُتح لي باب الرزق",
        "الاستغفار وزوال همومي",
        "قصة شفائي بالاستغفار",
        "كيف غير الاستغفار حياتي",
        "١٠٠٠ استغفار ونتائج مذهلة",
    ],
    "sahaba": [
        "من سيرة أبي بكر الصديق",
        "قصة من حياة عمر بن الخطاب",
        "من أخلاق عثمان بن عفان",
        "علي بن أبي طالب ومواقفه",
        "خالد بن الوليد سيف الله",
    ],
    "quran": [
        "سورة غيرت حياتي",
        "معجزة قرآنية في حياتي",
        "كيف حفظت القرآن",
        "قصتي مع تدبر القرآن",
        "آية قلبت حياتي",
    ],
    "prophets": [
        "عبرة من قصة يوسف عليه السلام",
        "درس من صبر أيوب",
        "حكمة من قصة موسى",
        "فائدة من سيرة إبراهيم",
        "موعظة من قصة نوح",
    ],
    "ruqyah": [
        "شُفيت بالرقية الشرعية",
        "الرقية وذهاب السحر",
        "قصة شفائي من العين",
        "المعوذات وأثرها في حياتي",
        "كيف حصنت نفسي بالقرآن",
    ],
    "rizq": [
        "الصدقة وبركة الرزق",
        "الدعاء وفتح أبواب الرزق",
        "صلة الرحم وسعة الرزق",
        "الاستخارة ورزق لم أتوقعه",
        "التوكل على الله والرزق",
    ],
    "tawbah": [
        "قصة توبتي إلى الله",
        "كيف رجعت إلى الله",
        "من الظلمات إلى النور",
        "توبة بعد سنوات من الضياع",
        "الله أرحم بي من نفسي",
    ],
    "miracles": [
        "معجزة رأيتها بعيني",
        "كرامة لأحد الصالحين",
        "دعاء استُجيب بطريقة عجيبة",
        "موقف عجيب مع الله",
        "رأيت رؤيا صالحة فتحققت",
    ],
}

NAMES = [
    "عبد الله أحمد", "محمد علي", "فاطمة الزهراء", "عائشة السعيدة",
    "خالد الرشيد", "عمر الصالح", "زينب الكريمة", "يوسف الطيب",
    "إبراهيم الحكيم", "مريم النقية", "علي الأمين", "سارة المباركة",
    "حسن البار", "نورة الفاضلة", "طارق النجيب", "آمنة الصابرة",
    "ياسر الراضي", "هدى المهتدية", "أنس الودود", "ليلى الحليمة"
]

def generate_content(category, title_template):
    """توليد محتوى واقعي للقصة"""
    intros = [
        "هذه قصتي الحقيقية، أحببت أن أشاركها معكم لعلها تكون سبباً في هداية أحد أو تثبيت مؤمن.",
        "أكتب لكم تجربتي الشخصية، والتي غيرت نظرتي للحياة تماماً.",
        "قصة حقيقية عشتها بنفسي، أسأل الله أن ينفع بها.",
        "تجربة واقعية من حياتي، آمل أن تكون عبرة وعظة.",
    ]
    
    bodies = {
        "general": [
            "كنت بعيداً عن الله، حتى جاء يوم فتح الله فيه قلبي. بدأت بالصلاة، ثم حفظ القرآن، ثم الدعوة إلى الله.",
            "تغيرت حياتي ١٨٠ درجة بعد أن التزمت بالصلاة في وقتها. وجدت السكينة والطمأنينة التي كنت أبحث عنها.",
            "كانت حياتي فارغة، حتى وجدت معنى الحياة في عبادة الله. الحمد لله على نعمة الهداية.",
        ],
        "istighfar": [
            "داومت على الاستغفار ١٠٠٠ مرة يومياً، ففُتحت لي أبواب لم أكن أتوقعها. الاستغفار مفتاح كل خير.",
            "كنت في ضائقة مالية شديدة، حتى نصحني أحدهم بالاستغفار. بعد شهر، جاءني الفرج من حيث لا أحتسب.",
            "الاستغفار كان سبباً في شفائي من مرض أقلقني سنوات. الحمد لله رب العالمين.",
        ],
        "ruqyah": [
            "كنت أعاني من أعراض غريبة، حتى رقيت نفسي بالقرآن. بعد أسابيع، ذهبت جميع الأعراض. القرآن شفاء.",
            "المعوذات والرقية الشرعية كانت سبباً في حفظي من كل سوء. أحمد الله على هذه النعمة.",
        ],
    }
    
    conclusions = [
        "أسأل الله أن يثبتنا على دينه، وأن يجعلنا من عباده الصالحين.",
        "الحمد لله الذي هداني، وما كنت لأهتدي لولا أن هداني الله.",
        "أدعو كل من يقرأ قصتي أن يبدأ من اليوم، فالله غفور رحيم.",
        "لا تيأس من رحمة الله، فإن الله يغفر الذنوب جميعاً.",
    ]
    
    intro = random.choice(intros)
    body = random.choice(bodies.get(category, ["هذه تجربة شخصية عميقة غيرت مجرى حياتي."]))
    conclusion = random.choice(conclusions)
    
    return f"{intro}\n\n{body}\n\n{conclusion}"

async def seed_all_stories():
    """إضافة 150 قصة"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    total_added = 0
    target = 150
    
    # توزيع القصص على الأقسام
    stories_per_category = target // len(STORY_TEMPLATES)
    
    for category, templates in STORY_TEMPLATES.items():
        for i in range(stories_per_category):
            title = random.choice(templates) + f" ({i+1})"
            content = generate_content(category, title)
            author = random.choice(NAMES)
            
            # تاريخ عشوائي في آخر 60 يوم
            days_ago = random.randint(0, 60)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            story = {
                "id": str(uuid4()),
                "author_id": "system",
                "author_name": author,
                "title": title,
                "content": content,
                "category": category,
                "media_type": "text",
                "created_at": created_at.isoformat(),
                "views_count": random.randint(100, 5000),
                "likes_count": random.randint(20, 1000),
                "comments_count": random.randint(5, 200),
                "approved": True,
                "featured": random.choice([True, False]),
            }
            
            await db.stories.insert_one(story)
            total_added += 1
            
            if total_added % 10 == 0:
                print(f"✅ تمت إضافة {total_added} قصة...")
    
    print(f"\n🎉 تمت إضافة {total_added} قصة بنجاح!")
    print(f"📊 إجمالي القصص في القاعدة: {await db.stories.count_documents({})}")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_all_stories())
