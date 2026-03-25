"""
Noor Academy V2 — Extended Content
====================================
Complete skeleton for 150+ lessons with placeholders
"""

# Import rich content from companion file
from data.noor_academy_aqeedah_fiqh_seerah import AQEEDAH_LESSONS_L2, AQEEDAH_LESSONS_L3

# Placeholder helper
def _create_placeholder_lesson(lesson_id, level, lesson_num, emoji, title_dict, track="general"):
    return {
        "id": lesson_id,
        "level": level,
        "lesson": lesson_num,
        "emoji": emoji,
        "title": title_dict,
        "method": "conceptual",
        "content": {
            "status": "placeholder",
            "message": {
                "ar": "قريباً — المحتوى قيد الإعداد",
                "en": "Coming Soon — Content in preparation",
                "de": "Demnächst",
                "fr": "Prochainement",
                "tr": "Yakında",
                "ru": "Скоро",
                "sv": "Kommer snart",
                "nl": "Binnenkort",
                "el": "Σύντομα"
            }
        },
        "quiz": {"type": "placeholder"},
        "xp": 20
    }

# ═══════════════════════════════════════════════════════════════
# NOORANIYA EXTENDED (Levels 4-7) — 40 lessons
# ═══════════════════════════════════════════════════════════════

NOORANIYA_LESSONS_L4 = [_create_placeholder_lesson(31+i, 4, i+1, "⚡", {"ar": f"التنوين والشدة — درس {i+1}", "en": f"Tanween & Shadda — L{i+1}", "de": f"Tanween & Shadda — L{i+1}", "fr": f"Tanween & Shadda — L{i+1}", "tr": f"Tenvin & Şedde — D{i+1}", "ru": f"Танвин и Шадда — У{i+1}", "sv": f"Tanween & Shadda — L{i+1}", "nl": f"Tanween & Shadda — L{i+1}", "el": f"Τανουίν & Σάντα — Μ{i+1}"}) for i in range(10)]

NOORANIYA_LESSONS_L5 = [_create_placeholder_lesson(41+i, 5, i+1, "📝", {"ar": f"قراءة الكلمات — درس {i+1}", "en": f"Reading Words — L{i+1}", "de": f"Wörter lesen — L{i+1}", "fr": f"Lire mots — L{i+1}", "tr": f"Kelime Okuma — D{i+1}", "ru": f"Чтение слов — У{i+1}", "sv": f"Läsa ord — L{i+1}", "nl": f"Woorden lezen — L{i+1}", "el": f"Ανάγνωση λέξεων — Μ{i+1}"}) for i in range(10)]

NOORANIYA_LESSONS_L6 = [_create_placeholder_lesson(51+i, 6, i+1, "📖", {"ar": f"قراءة الآيات — درس {i+1}", "en": f"Reading Verses — L{i+1}", "de": f"Verse lesen — L{i+1}", "fr": f"Lire versets — L{i+1}", "tr": f"Ayet Okuma — D{i+1}", "ru": f"Чтение аятов — У{i+1}", "sv": f"Läsa verser — L{i+1}", "nl": f"Verzen lezen — L{i+1}", "el": f"Ανάγνωση στίχων — Μ{i+1}"}) for i in range(10)]

NOORANIYA_LESSONS_L7 = [_create_placeholder_lesson(61+i, 7, i+1, "🎓", {"ar": f"التجويد — درس {i+1}", "en": f"Tajweed — L{i+1}", "de": f"Tajweed — L{i+1}", "fr": f"Tajweed — L{i+1}", "tr": f"Tecvid — D{i+1}", "ru": f"Таджвид — У{i+1}", "sv": f"Tajweed — L{i+1}", "nl": f"Tajweed — L{i+1}", "el": f"Τατζουίντ — Μ{i+1}"}) for i in range(10)]

NOORANIYA_ALL_LESSONS_EXTENDED = NOORANIYA_LESSONS_L4 + NOORANIYA_LESSONS_L5 + NOORANIYA_LESSONS_L6 + NOORANIYA_LESSONS_L7

# ═══════════════════════════════════════════════════════════════
# AQEEDAH TRACK (50 lessons, 5 levels)
# ═══════════════════════════════════════════════════════════════

AQEEDAH_LESSONS_L1 = [_create_placeholder_lesson(i+1, 1, i+1, "☝️", {"ar": f"التوحيد — درس {i+1}", "en": f"Tawheed — L{i+1}", "de": f"Tawheed — L{i+1}", "fr": f"Tawheed — L{i+1}", "tr": f"Tevhid — D{i+1}", "ru": f"Таухид — У{i+1}", "sv": f"Tawheed — L{i+1}", "nl": f"Tawheed — L{i+1}", "el": f"Ταουχίντ — Μ{i+1}"}, "aqeedah") for i in range(10)]

AQEEDAH_LESSONS_L4 = [_create_placeholder_lesson(33+i, 4, i+1, "🕋", {"ar": f"أركان الإسلام — درس {i+1}", "en": f"Pillars of Islam — L{i+1}", "de": f"Säulen Islam — L{i+1}", "fr": f"Piliers Islam — L{i+1}", "tr": f"İslam Şartları — D{i+1}", "ru": f"Столпы Ислама — У{i+1}", "sv": f"Islams pelare — L{i+1}", "nl": f"Zuilen Islam — L{i+1}", "el": f"Πυλώνες Ισλάμ — Μ{i+1}"}, "aqeedah") for i in range(10)]

AQEEDAH_LESSONS_L5 = [_create_placeholder_lesson(43+i, 5, i+1, "📚", {"ar": f"مراجعة شاملة — درس {i+1}", "en": f"Review — L{i+1}", "de": f"Wiederholung — L{i+1}", "fr": f"Révision — L{i+1}", "tr": f"Tekrar — D{i+1}", "ru": f"Обзор — У{i+1}", "sv": f"Genomgång — L{i+1}", "nl": f"Herhaling — L{i+1}", "el": f"Επανάληψη — Μ{i+1}"}, "aqeedah") for i in range(8)]

AQEEDAH_ALL_LESSONS = AQEEDAH_LESSONS_L1 + AQEEDAH_LESSONS_L2 + AQEEDAH_LESSONS_L3 + AQEEDAH_LESSONS_L4 + AQEEDAH_LESSONS_L5

# ═══════════════════════════════════════════════════════════════
# FIQH TRACK (40 lessons, 4 levels)
# ═══════════════════════════════════════════════════════════════

FIQH_LESSONS_L1 = [_create_placeholder_lesson(i+1, 1, i+1, "💧", {"ar": f"الطهارة — درس {i+1}", "en": f"Purification — L{i+1}", "de": f"Reinigung — L{i+1}", "fr": f"Purification — L{i+1}", "tr": f"Taharet — D{i+1}", "ru": f"Очищение — У{i+1}", "sv": f"Rening — L{i+1}", "nl": f"Reiniging — L{i+1}", "el": f"Κάθαρση — Μ{i+1}"}, "fiqh") for i in range(10)]

FIQH_LESSONS_L2 = [_create_placeholder_lesson(11+i, 2, i+1, "🕌", {"ar": f"الصلاة — درس {i+1}", "en": f"Prayer — L{i+1}", "de": f"Gebet — L{i+1}", "fr": f"Prière — L{i+1}", "tr": f"Namaz — D{i+1}", "ru": f"Молитва — У{i+1}", "sv": f"Bön — L{i+1}", "nl": f"Gebed — L{i+1}", "el": f"Προσευχή — Μ{i+1}"}, "fiqh") for i in range(12)]

FIQH_LESSONS_L3 = [_create_placeholder_lesson(23+i, 3, i+1, "🌙", {"ar": f"الصيام — درس {i+1}", "en": f"Fasting — L{i+1}", "de": f"Fasten — L{i+1}", "fr": f"Jeûne — L{i+1}", "tr": f"Oruç — D{i+1}", "ru": f"Пост — У{i+1}", "sv": f"Fasta — L{i+1}", "nl": f"Vasten — L{i+1}", "el": f"Νηστεία — Μ{i+1}"}, "fiqh") for i in range(8)]

FIQH_LESSONS_L4 = [_create_placeholder_lesson(31+i, 4, i+1, "💰", {"ar": f"الزكاة والحج — درس {i+1}", "en": f"Zakat & Hajj — L{i+1}", "de": f"Zakat & Hadsch — L{i+1}", "fr": f"Zakat & Hajj — L{i+1}", "tr": f"Zekat & Hac — D{i+1}", "ru": f"Закят и Хадж — У{i+1}", "sv": f"Zakat & Hajj — L{i+1}", "nl": f"Zakat & Hadj — L{i+1}", "el": f"Ζακάτ & Χατζ — Μ{i+1}"}, "fiqh") for i in range(10)]

FIQH_ALL_LESSONS = FIQH_LESSONS_L1 + FIQH_LESSONS_L2 + FIQH_LESSONS_L3 + FIQH_LESSONS_L4

# ═══════════════════════════════════════════════════════════════
# SEERAH TRACK (60 lessons, 6 levels)
# ═══════════════════════════════════════════════════════════════

SEERAH_LESSONS_L1 = [_create_placeholder_lesson(i+1, 1, i+1, "👶", {"ar": f"الميلاد والطفولة — درس {i+1}", "en": f"Birth & Childhood — L{i+1}", "de": f"Geburt & Kindheit — L{i+1}", "fr": f"Naissance & enfance — L{i+1}", "tr": f"Doğum & Çocukluk — D{i+1}", "ru": f"Рождение и детство — У{i+1}", "sv": f"Födelse & barndom — L{i+1}", "nl": f"Geboorte & jeugd — L{i+1}", "el": f"Γέννηση & παιδική ηλικία — Μ{i+1}"}, "seerah") for i in range(10)]

SEERAH_LESSONS_L2 = [_create_placeholder_lesson(11+i, 2, i+1, "📜", {"ar": f"النبوة — درس {i+1}", "en": f"Prophethood — L{i+1}", "de": f"Prophetentum — L{i+1}", "fr": f"Prophétie — L{i+1}", "tr": f"Peygamberlik — D{i+1}", "ru": f"Пророчество — У{i+1}", "sv": f"Profetskap — L{i+1}", "nl": f"Profeetschap — L{i+1}", "el": f"Προφητεία — Μ{i+1}"}, "seerah") for i in range(10)]

SEERAH_LESSONS_L3 = [_create_placeholder_lesson(21+i, 3, i+1, "🐪", {"ar": f"الهجرة — درس {i+1}", "en": f"Hijrah — L{i+1}", "de": f"Hijra — L{i+1}", "fr": f"Hégire — L{i+1}", "tr": f"Hicret — D{i+1}", "ru": f"Хиджра — У{i+1}", "sv": f"Hijrah — L{i+1}", "nl": f"Hijrah — L{i+1}", "el": f"Χίτζρα — Μ{i+1}"}, "seerah") for i in range(10)]

SEERAH_LESSONS_L4 = [_create_placeholder_lesson(31+i, 4, i+1, "⚔️", {"ar": f"الغزوات — درس {i+1}", "en": f"Battles — L{i+1}", "de": f"Schlachten — L{i+1}", "fr": f"Batailles — L{i+1}", "tr": f"Gazalar — D{i+1}", "ru": f"Сражения — У{i+1}", "sv": f"Strider — L{i+1}", "nl": f"Veldslagen — L{i+1}", "el": f"Μάχες — Μ{i+1}"}, "seerah") for i in range(10)]

SEERAH_LESSONS_L5 = [_create_placeholder_lesson(41+i, 5, i+1, "🕋", {"ar": f"فتح مكة — درس {i+1}", "en": f"Conquest — L{i+1}", "de": f"Eroberung — L{i+1}", "fr": f"Conquête — L{i+1}", "tr": f"Fetih — D{i+1}", "ru": f"Завоевание — У{i+1}", "sv": f"Erövring — L{i+1}", "nl": f"Verovering — L{i+1}", "el": f"Κατάκτηση — Μ{i+1}"}, "seerah") for i in range(10)]

SEERAH_LESSONS_L6 = [_create_placeholder_lesson(51+i, 6, i+1, "💝", {"ar": f"أخلاق النبي ﷺ — درس {i+1}", "en": f"Prophet's Character — L{i+1}", "de": f"Charakter — L{i+1}", "fr": f"Caractère — L{i+1}", "tr": f"Ahlak — D{i+1}", "ru": f"Характер — У{i+1}", "sv": f"Karaktär — L{i+1}", "nl": f"Karakter — L{i+1}", "el": f"Χαρακτήρας — Μ{i+1}"}, "seerah") for i in range(10)]

SEERAH_ALL_LESSONS = SEERAH_LESSONS_L1 + SEERAH_LESSONS_L2 + SEERAH_LESSONS_L3 + SEERAH_LESSONS_L4 + SEERAH_LESSONS_L5 + SEERAH_LESSONS_L6
