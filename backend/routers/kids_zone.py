"""
Router: kids_zone
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

router = APIRouter(tags=["Kids Zone"])

# ═══ Constants ═══
MOSQUE_STAGES = [
    {"stage": "foundation", "bricks_needed": 0, "emoji": "🧱", "name_key": "mosque_foundation"},
    {"stage": "walls", "bricks_needed": 50, "emoji": "🏗️", "name_key": "mosque_walls"},
    {"stage": "pillars", "bricks_needed": 120, "emoji": "🏛️", "name_key": "mosque_pillars"},
    {"stage": "dome_base", "bricks_needed": 200, "emoji": "⛪", "name_key": "mosque_dome_base"},
    {"stage": "dome", "bricks_needed": 300, "emoji": "🕌", "name_key": "mosque_dome"},
    {"stage": "minaret", "bricks_needed": 450, "emoji": "🗼", "name_key": "mosque_minaret"},
    {"stage": "garden", "bricks_needed": 600, "emoji": "🌳", "name_key": "mosque_garden"},
    {"stage": "golden_dome", "bricks_needed": 800, "emoji": "✨", "name_key": "mosque_golden_dome"},
    {"stage": "complete", "bricks_needed": 1000, "emoji": "🕋", "name_key": "mosque_complete"},
]

DIFFICULTY_TIERS = [
    {"name": "beginner", "min_xp": 0, "emoji": "🌱"},
    {"name": "intermediate", "min_xp": 100, "emoji": "📖"},
    {"name": "advanced", "min_xp": 300, "emoji": "⭐"},
    {"name": "expert", "min_xp": 600, "emoji": "🌟"},
    {"name": "master", "min_xp": 1000, "emoji": "💎"},
]

def get_difficulty_tier(total_xp: int) -> dict:
    tier = DIFFICULTY_TIERS[0]
    for t in DIFFICULTY_TIERS:
        if total_xp >= t["min_xp"]:
            tier = t
    return tier

def get_mosque_progress(total_bricks: int) -> dict:
    current_stage = MOSQUE_STAGES[0]
    next_stage = MOSQUE_STAGES[1] if len(MOSQUE_STAGES) > 1 else None
    for i, stage in enumerate(MOSQUE_STAGES):
        if total_bricks >= stage["bricks_needed"]:
            current_stage = stage
            next_stage = MOSQUE_STAGES[i + 1] if i + 1 < len(MOSQUE_STAGES) else None
    return {
        "current_stage": current_stage,
        "next_stage": next_stage,
        "total_bricks": total_bricks,
        "bricks_to_next": (next_stage["bricks_needed"] - total_bricks) if next_stage else 0,
        "progress_pct": min(100, int((total_bricks / (next_stage["bricks_needed"] if next_stage else current_stage["bricks_needed"])) * 100)),
        "stages": MOSQUE_STAGES,
    }


@router.get("/kids-zone/generate-game")
async def generate_game(user_id: str = "", game_type: str = "auto", locale: str = "ar"):
    """Procedural Content Generator: generates a game based on user skill gaps."""
    import random
    
    # Get or create user skill profile
    skill = await db.kids_skills.find_one({"user_id": user_id}) if user_id else None
    if not skill:
        skill = {
            "user_id": user_id or "guest",
            "phoneme_accuracy": {},
            "total_xp": 0,
            "golden_bricks": 0,
            "games_played": 0,
            "weak_phonemes": [],
        }
    
    tier = get_difficulty_tier(skill.get("total_xp", 0))
    phoneme_acc = skill.get("phoneme_accuracy", {})
    
    # Identify weak phonemes (accuracy < 70%)
    weak_letters = []
    for pair in CONFUSABLE_PHONEMES:
        id_a, id_b = str(pair[0]), str(pair[1])
        acc_a = phoneme_acc.get(id_a, {}).get("accuracy", 50)
        acc_b = phoneme_acc.get(id_b, {}).get("accuracy", 50)
        if acc_a < 70:
            weak_letters.append(pair[0])
        if acc_b < 70:
            weak_letters.append(pair[1])
    
    # Auto-select game type based on weak areas
    game_types = ["letter_maze", "word_match", "tajweed_puzzle", "pronunciation"]
    if game_type == "auto":
        if weak_letters:
            # Prioritize pronunciation and letter games for weak phonemes
            game_type = random.choice(["letter_maze", "pronunciation", "tajweed_puzzle"])
        else:
            game_type = random.choice(game_types)
    
    # Procedurally generate game content
    if game_type == "letter_maze":
        game_data = _gen_letter_maze(tier, weak_letters)
    elif game_type == "word_match":
        game_data = _gen_word_match(tier)
    elif game_type == "tajweed_puzzle":
        game_data = _gen_tajweed_puzzle(tier, weak_letters)
    elif game_type == "pronunciation":
        game_data = _gen_pronunciation(tier, weak_letters)
    else:
        game_data = _gen_word_match(tier)
    
    game_id = str(uuid.uuid4())
    game_data["game_id"] = game_id
    game_data["game_type"] = game_type
    game_data["difficulty"] = tier["name"]
    game_data["time_limit"] = tier["time_bonus"]
    game_data["brick_reward"] = tier["brick_reward"]
    game_data["xp_reward"] = 10 + (DIFFICULTY_TIERS.index(tier) * 5)
    
    return {"success": True, "game": game_data}


def _gen_letter_maze(tier: dict, weak_letters: list) -> dict:
    """Generate a letter identification maze game."""
    import random
    # Pick target letters - prefer weak ones
    all_letters = list(ARABIC_LETTERS)
    if weak_letters:
        targets = [lt for lt in all_letters if lt["id"] in weak_letters]
        if len(targets) < 2:
            targets = random.sample(all_letters, 2)
    else:
        targets = random.sample(all_letters, min(3, tier["choices"]))
    
    target = random.choice(targets)
    # Generate grid with distractors
    grid_size = 3 if tier["choices"] <= 3 else 4
    grid = []
    distractors = [lt for lt in all_letters if lt["id"] != target["id"]]
    
    for row in range(grid_size):
        grid_row = []
        for col in range(grid_size):
            if row == 0 and col == 0:
                grid_row.append({"letter": target["letter"], "id": target["id"], "is_target": True})
            else:
                d = random.choice(distractors)
                grid_row.append({"letter": d["letter"], "id": d["id"], "is_target": False})
        grid.append(grid_row)
    
    # Shuffle target position
    target_row = random.randint(0, grid_size - 1)
    target_col = random.randint(0, grid_size - 1)
    grid[0][0], grid[target_row][target_col] = grid[target_row][target_col], grid[0][0]
    
    # Add confusable pair if exists
    confusable = None
    for pair in CONFUSABLE_PHONEMES:
        if target["id"] == pair[0]:
            confusable = {"id": pair[1], "letter": pair[3]}
            break
        if target["id"] == pair[1]:
            confusable = {"id": pair[0], "letter": pair[2]}
            break
    
    return {
        "target_letter": {
            "id": target["id"],
            "letter": target["letter"],
            "name_ar": target["name_ar"],
            "name_en": target["name_en"],
            "transliteration": target["transliteration"],
            "audio_hint": target["audio_hint"],
            "example_word": target["example_word"],
            "example_meaning": target["example_meaning"],
        },
        "grid": grid,
        "grid_size": grid_size,
        "confusable": confusable,
        "find_count": 1,
    }


def _gen_word_match(tier: dict) -> dict:
    """Generate a Quranic word matching game."""
    import random
    pool = list(QURAN_VOCAB)
    count = min(tier["choices"], len(pool))
    selected = random.sample(pool, count)
    
    words = [{"id": w["id"], "word": w["word"], "transliteration": w["transliteration"]} for w in selected]
    meanings = [{"id": w["id"], "meaning": w["meaning"], "surah": w["surah"]} for w in selected]
    random.shuffle(meanings)
    
    return {
        "words": words,
        "meanings": meanings,
        "pair_count": count,
    }


def _gen_tajweed_puzzle(tier: dict, weak_letters: list) -> dict:
    """Generate a Tajweed pronunciation rule puzzle."""
    import random
    
    tajweed_rules = [
        {"id": "idgham", "name_ar": "إدغام", "name_en": "Idgham (Merging)", "description": "When Noon Sakinah or Tanween is followed by ي ن م و ل ر", "example": "مَن يَعْمَلُ", "correct_rule": "merge"},
        {"id": "ikhfa", "name_ar": "إخفاء", "name_en": "Ikhfa (Hiding)", "description": "When Noon Sakinah or Tanween is followed by 15 specific letters", "example": "مِنْ قَبْلِ", "correct_rule": "hide"},
        {"id": "iqlab", "name_ar": "إقلاب", "name_en": "Iqlab (Conversion)", "description": "When Noon Sakinah or Tanween is followed by ب", "example": "أَنْبِئْهُمْ", "correct_rule": "convert"},
        {"id": "izhar", "name_ar": "إظهار", "name_en": "Izhar (Clear)", "description": "When Noon Sakinah or Tanween is followed by throat letters", "example": "مَنْ آمَنَ", "correct_rule": "clear"},
        {"id": "madd_tabii", "name_ar": "مدّ طبيعي", "name_en": "Madd Tabii (Natural)", "description": "Alif after Fathah, Ya after Kasrah, or Waw after Dammah (2 counts)", "example": "قَالَ", "correct_rule": "natural_stretch"},
        {"id": "qalqalah", "name_ar": "قلقلة", "name_en": "Qalqalah (Echoing)", "description": "Bouncing sound on Sukoon of letters ق ط ب ج د", "example": "أَحَدْ", "correct_rule": "echo"},
    ]
    
    selected = random.sample(tajweed_rules, min(3, len(tajweed_rules)))
    target_rule = random.choice(selected)
    
    # Generate choices - one correct + distractors
    all_rules = [r["correct_rule"] for r in tajweed_rules]
    choices = [target_rule["correct_rule"]]
    distractors = [r for r in all_rules if r != target_rule["correct_rule"]]
    choices.extend(random.sample(distractors, min(tier["choices"] - 1, len(distractors))))
    random.shuffle(choices)
    
    return {
        "question_rule": {
            "id": target_rule["id"],
            "name_ar": target_rule["name_ar"],
            "name_en": target_rule["name_en"],
            "example": target_rule["example"],
        },
        "description": target_rule["description"],
        "choices": choices,
        "correct_answer": target_rule["correct_rule"],
        "all_rules": [{"id": r["id"], "name_ar": r["name_ar"], "name_en": r["name_en"], "correct_rule": r["correct_rule"]} for r in tajweed_rules],
    }


def _gen_pronunciation(tier: dict, weak_letters: list) -> dict:
    """Generate a pronunciation challenge targeting weak phonemes."""
    import random
    
    # Pick words from Quran vocab + letter examples
    candidates = []
    if weak_letters:
        for lt in ARABIC_LETTERS:
            if lt["id"] in weak_letters:
                candidates.append({
                    "word": lt["example_word"],
                    "transliteration": lt["transliteration"],
                    "meaning": lt["example_meaning"],
                    "letter_id": lt["id"],
                    "letter": lt["letter"],
                    "source": "letter",
                })
    
    # Add Quranic words
    for qw in QURAN_VOCAB:
        candidates.append({
            "word": qw["word"],
            "transliteration": qw["transliteration"],
            "meaning": qw["meaning"],
            "letter_id": None,
            "letter": None,
            "source": "quran",
        })
    
    if not candidates:
        candidates = [{"word": lt["example_word"], "transliteration": lt["transliteration"], "meaning": lt["example_meaning"], "letter_id": lt["id"], "letter": lt["letter"], "source": "letter"} for lt in ARABIC_LETTERS]
    
    target = random.choice(candidates)
    accuracy_threshold = max(60, 85 - (DIFFICULTY_TIERS.index(tier) * 5))
    
    return {
        "target_word": target["word"],
        "transliteration": target["transliteration"],
        "meaning": target["meaning"],
        "letter_id": target["letter_id"],
        "letter": target["letter"],
        "source": target["source"],
        "accuracy_threshold": accuracy_threshold,
    }


@router.post("/kids-zone/submit-result")
async def submit_game_result(payload: dict):
    """Submit game result and update skill profile."""
    user_id = payload.get("user_id", "guest")
    game_type = payload.get("game_type", "")
    correct = payload.get("correct", False)
    score = payload.get("score", 0)
    phonemes_tested = payload.get("phonemes_tested", [])
    pronunciation_accuracy = payload.get("pronunciation_accuracy", 0)
    
    # Get or create skill profile
    skill = await db.kids_skills.find_one({"user_id": user_id})
    if not skill:
        skill = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "phoneme_accuracy": {},
            "total_xp": 0,
            "golden_bricks": 0,
            "games_played": 0,
            "weak_phonemes": [],
            "created_at": datetime.utcnow().isoformat(),
        }
        await db.kids_skills.insert_one(skill)
    
    # Calculate rewards
    xp_earned = score if correct else max(2, score // 3)
    tier = get_difficulty_tier(skill.get("total_xp", 0))
    bricks_earned = tier["brick_reward"] if correct else 0
    
    # Update phoneme accuracy for tested phonemes
    phoneme_acc = skill.get("phoneme_accuracy", {})
    for pid in phonemes_tested:
        pid_str = str(pid)
        if pid_str not in phoneme_acc:
            phoneme_acc[pid_str] = {"attempts": 0, "correct": 0, "accuracy": 50}
        phoneme_acc[pid_str]["attempts"] += 1
        if correct:
            phoneme_acc[pid_str]["correct"] += 1
        total = phoneme_acc[pid_str]["attempts"]
        corr = phoneme_acc[pid_str]["correct"]
        phoneme_acc[pid_str]["accuracy"] = int((corr / total) * 100) if total > 0 else 50
    
    # For pronunciation games, also update based on accuracy
    if game_type == "pronunciation" and pronunciation_accuracy > 0:
        for pid in phonemes_tested:
            pid_str = str(pid)
            if pid_str in phoneme_acc:
                # Blend speech accuracy with game accuracy
                old_acc = phoneme_acc[pid_str]["accuracy"]
                phoneme_acc[pid_str]["accuracy"] = int((old_acc * 0.7) + (pronunciation_accuracy * 0.3))
    
    # Identify new weak phonemes
    weak = []
    for pair in CONFUSABLE_PHONEMES:
        for pid in [pair[0], pair[1]]:
            pid_str = str(pid)
            if pid_str in phoneme_acc and phoneme_acc[pid_str]["accuracy"] < 70:
                weak.append(pid)
    
    # Update skill profile
    update = {
        "$set": {
            "phoneme_accuracy": phoneme_acc,
            "weak_phonemes": weak,
            "updated_at": datetime.utcnow().isoformat(),
        },
        "$inc": {
            "total_xp": xp_earned,
            "golden_bricks": bricks_earned,
            "games_played": 1,
        },
    }
    await db.kids_skills.update_one({"user_id": user_id}, update)
    
    new_xp = skill.get("total_xp", 0) + xp_earned
    new_bricks = skill.get("golden_bricks", 0) + bricks_earned
    new_tier = get_difficulty_tier(new_xp)
    mosque = get_mosque_progress(new_bricks)
    
    return {
        "success": True,
        "xp_earned": xp_earned,
        "bricks_earned": bricks_earned,
        "total_xp": new_xp,
        "total_bricks": new_bricks,
        "difficulty": new_tier["name"],
        "mosque_progress": mosque,
        "weak_phonemes": weak,
        "level_up": new_tier["name"] != tier["name"],
    }


@router.get("/kids-zone/progress")
async def get_kids_progress(user_id: str = ""):
    """Get user's skill map and progression data."""
    skill = await db.kids_skills.find_one({"user_id": user_id}, {"_id": 0}) if user_id else None
    if not skill:
        skill = {
            "user_id": user_id or "guest",
            "phoneme_accuracy": {},
            "total_xp": 0,
            "golden_bricks": 0,
            "games_played": 0,
            "weak_phonemes": [],
        }
    
    tier = get_difficulty_tier(skill.get("total_xp", 0))
    mosque = get_mosque_progress(skill.get("golden_bricks", 0))
    
    # Build per-letter skill map
    letter_skills = []
    for lt in ARABIC_LETTERS:
        pid = str(lt["id"])
        acc_data = skill.get("phoneme_accuracy", {}).get(pid, {"accuracy": 50, "attempts": 0, "correct": 0})
        letter_skills.append({
            "id": lt["id"],
            "letter": lt["letter"],
            "name_ar": lt["name_ar"],
            "accuracy": acc_data.get("accuracy", 50),
            "attempts": acc_data.get("attempts", 0),
            "is_weak": lt["id"] in skill.get("weak_phonemes", []),
        })
    
    return {
        "success": True,
        "profile": {
            "total_xp": skill.get("total_xp", 0),
            "golden_bricks": skill.get("golden_bricks", 0),
            "games_played": skill.get("games_played", 0),
            "difficulty": tier["name"],
            "tier": tier,
            "weak_phonemes": skill.get("weak_phonemes", []),
        },
        "letter_skills": letter_skills,
        "mosque": mosque,
        "confusable_pairs": [{"a": p[2], "b": p[3], "id_a": p[0], "id_b": p[1]} for p in CONFUSABLE_PHONEMES],
    }


@router.get("/kids-zone/mosque")
async def get_mosque_status(user_id: str = ""):
    """Get the virtual mosque building progress."""
    skill = await db.kids_skills.find_one({"user_id": user_id}, {"_id": 0}) if user_id else None
    bricks = skill.get("golden_bricks", 0) if skill else 0
    return {"success": True, "mosque": get_mosque_progress(bricks)}



# ==================== KIDS JOURNEY - CONNECTED LEARNING PATH ====================

# IRS Method: Introduce → Recognize → Say
# 5 Worlds, each with multiple stages, each stage has 3 activities

JOURNEY_WORLDS = [
    {
        "id": "w1", "title_ar": "الحروف", "title_en": "Letters",
        "emoji": "🔤", "color": "#3B82F6",
        "description_ar": "تعلم الحروف العربية", "description_en": "Learn Arabic Letters",
        "stages": [
            {"id": "w1s1", "title_ar": "أ ب ت ث", "title_en": "Alif Ba Ta Tha", "letters": [1, 2, 3, 4], "type": "letters"},
            {"id": "w1s2", "title_ar": "ج ح خ", "title_en": "Jim Ha Kha", "letters": [5, 6, 7], "type": "letters"},
            {"id": "w1s3", "title_ar": "د ذ ر ز", "title_en": "Dal Dhal Ra Za", "letters": [8, 9, 10, 11], "type": "letters"},
            {"id": "w1s4", "title_ar": "س ش ص ض", "title_en": "Sin Shin Sad Dad", "letters": [12, 13, 14, 15], "type": "letters"},
            {"id": "w1s5", "title_ar": "ط ظ ع غ", "title_en": "Tah Zah Ain Ghain", "letters": [16, 17, 18, 19], "type": "letters"},
            {"id": "w1s6", "title_ar": "ف ق ك ل", "title_en": "Fa Qaf Kaf Lam", "letters": [20, 21, 22, 23], "type": "letters"},
            {"id": "w1s7", "title_ar": "م ن ه و ي", "title_en": "Mim Nun Ha Waw Ya", "letters": [24, 25, 26, 27, 28], "type": "letters"},
            {"id": "w1boss", "title_ar": "تحدي الحروف", "title_en": "Letter Boss", "letters": list(range(1, 29)), "type": "boss"},
        ],
    },
    {
        "id": "w2", "title_ar": "الحركات", "title_en": "Vowels",
        "emoji": "📝", "color": "#10B981",
        "description_ar": "تعلم الحركات والتشكيل", "description_en": "Learn Harakat & Diacritics",
        "stages": [
            {"id": "w2s1", "title_ar": "الفَتحة", "title_en": "Fathah (a)", "haraka": "fathah", "type": "harakat",
             "examples": [{"letter": "بَ", "sound": "ba"}, {"letter": "تَ", "sound": "ta"}, {"letter": "سَ", "sound": "sa"}, {"letter": "نَ", "sound": "na"}]},
            {"id": "w2s2", "title_ar": "الكَسرة", "title_en": "Kasrah (i)", "haraka": "kasrah", "type": "harakat",
             "examples": [{"letter": "بِ", "sound": "bi"}, {"letter": "تِ", "sound": "ti"}, {"letter": "سِ", "sound": "si"}, {"letter": "نِ", "sound": "ni"}]},
            {"id": "w2s3", "title_ar": "الضَّمة", "title_en": "Dammah (u)", "haraka": "dammah", "type": "harakat",
             "examples": [{"letter": "بُ", "sound": "bu"}, {"letter": "تُ", "sound": "tu"}, {"letter": "سُ", "sound": "su"}, {"letter": "نُ", "sound": "nu"}]},
            {"id": "w2s4", "title_ar": "السُّكون", "title_en": "Sukoon", "haraka": "sukoon", "type": "harakat",
             "examples": [{"letter": "بْ", "sound": "b"}, {"letter": "تْ", "sound": "t"}, {"letter": "سْ", "sound": "s"}, {"letter": "نْ", "sound": "n"}]},
            {"id": "w2s5", "title_ar": "التنوين", "title_en": "Tanween", "haraka": "tanween", "type": "harakat",
             "examples": [{"letter": "بًا", "sound": "ban"}, {"letter": "بٍ", "sound": "bin"}, {"letter": "بٌ", "sound": "bun"}]},
            {"id": "w2boss", "title_ar": "تحدي الحركات", "title_en": "Harakat Boss", "haraka": "all", "type": "boss"},
        ],
    },
    {
        "id": "w3", "title_ar": "القراءة", "title_en": "Reading",
        "emoji": "📖", "color": "#8B5CF6",
        "description_ar": "تعلم قراءة الكلمات", "description_en": "Learn to Read Words",
        "stages": [
            {"id": "w3s1", "title_ar": "كلمات بسيطة", "title_en": "Simple Words", "type": "reading",
             "words": [{"ar": "كَتَبَ", "en": "wrote", "trans": "kataba"}, {"ar": "ذَهَبَ", "en": "went", "trans": "dhahaba"}, {"ar": "قَرَأَ", "en": "read", "trans": "qara'a"}]},
            {"id": "w3s2", "title_ar": "كلمات القرآن", "title_en": "Quran Words", "type": "reading",
             "words": [{"ar": "بِسْمِ", "en": "In the name", "trans": "bismi"}, {"ar": "اللَّهِ", "en": "Allah", "trans": "Allahi"}, {"ar": "الرَّحْمَنِ", "en": "Most Gracious", "trans": "Ar-Rahmani"}]},
            {"id": "w3s3", "title_ar": "جمل قصيرة", "title_en": "Short Phrases", "type": "reading",
             "words": [{"ar": "الحَمْدُ لِلَّهِ", "en": "Praise be to Allah", "trans": "Alhamdulillah"}, {"ar": "سُبْحَانَ اللَّهِ", "en": "Glory to Allah", "trans": "SubhanAllah"}]},
            {"id": "w3boss", "title_ar": "تحدي القراءة", "title_en": "Reading Boss", "type": "boss"},
        ],
    },
    {
        "id": "w4", "title_ar": "القرآن", "title_en": "Quran",
        "emoji": "🕌", "color": "#F59E0B",
        "description_ar": "اقرأ سور قصيرة", "description_en": "Read Short Surahs",
        "stages": [
            {"id": "w4s1", "title_ar": "الفاتحة", "title_en": "Al-Fatiha", "type": "surah",
             "ayahs": ["بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "الرَّحْمَنِ الرَّحِيمِ", "مَالِكِ يَوْمِ الدِّينِ", "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ", "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ"],
             "meanings": ["In the name of Allah, Most Gracious, Most Merciful", "Praise be to Allah, Lord of all worlds", "The Most Gracious, Most Merciful", "Master of the Day of Judgment", "You alone we worship, You alone we ask for help", "Guide us to the straight path", "The path of those You have blessed, not of those who earned anger, nor of those who went astray"]},
            {"id": "w4s2", "title_ar": "الإخلاص", "title_en": "Al-Ikhlas", "type": "surah",
             "ayahs": ["بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "قُلْ هُوَ اللَّهُ أَحَدٌ", "اللَّهُ الصَّمَدُ", "لَمْ يَلِدْ وَلَمْ يُولَدْ", "وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ"],
             "meanings": ["In the name of Allah, Most Gracious, Most Merciful", "Say: He is Allah, the One", "Allah, the Eternal Refuge", "He neither begets nor was He begotten", "Nor is there to Him any equal"]},
            {"id": "w4s3", "title_ar": "الناس", "title_en": "An-Nas", "type": "surah",
             "ayahs": ["بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "قُلْ أَعُوذُ بِرَبِّ النَّاسِ", "مَلِكِ النَّاسِ", "إِلَهِ النَّاسِ", "مِنْ شَرِّ الْوَسْوَاسِ الْخَنَّاسِ", "الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ", "مِنَ الْجِنَّةِ وَالنَّاسِ"],
             "meanings": ["In the name of Allah, Most Gracious, Most Merciful", "Say: I seek refuge in the Lord of mankind", "The King of mankind", "The God of mankind", "From the evil of the whisperer who withdraws", "Who whispers in the chests of mankind", "From among the jinn and mankind"]},
            {"id": "w4s4", "title_ar": "الفلق", "title_en": "Al-Falaq", "type": "surah",
             "ayahs": ["بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ", "مِنْ شَرِّ مَا خَلَقَ", "وَمِنْ شَرِّ غَاسِقٍ إِذَا وَقَبَ", "وَمِنْ شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ", "وَمِنْ شَرِّ حَاسِدٍ إِذَا حَسَدَ"],
             "meanings": ["In the name of Allah, Most Gracious, Most Merciful", "Say: I seek refuge in the Lord of daybreak", "From the evil of that which He created", "From the evil of darkness when it settles", "From the evil of the blowers in knots", "From the evil of an envier when they envy"]},
            {"id": "w4boss", "title_ar": "تحدي القرآن", "title_en": "Quran Boss", "type": "boss"},
        ],
    },
    {
        "id": "w5", "title_ar": "التجويد", "title_en": "Tajweed",
        "emoji": "🎯", "color": "#EF4444",
        "description_ar": "أحكام التجويد", "description_en": "Tajweed Rules",
        "stages": [
            {"id": "w5s1", "title_ar": "إظهار و إدغام", "title_en": "Izhar & Idgham", "type": "tajweed",
             "rules": [
                 {"id": "izhar", "name_ar": "إظهار", "name_en": "Clear", "desc": "Noon Sakinah before throat letters", "example": "مَنْ آمَنَ"},
                 {"id": "idgham", "name_ar": "إدغام", "name_en": "Merge", "desc": "Noon Sakinah before ي ن م و ل ر", "example": "مَن يَعْمَلُ"},
             ]},
            {"id": "w5s2", "title_ar": "إخفاء و إقلاب", "title_en": "Ikhfa & Iqlab", "type": "tajweed",
             "rules": [
                 {"id": "ikhfa", "name_ar": "إخفاء", "name_en": "Hide", "desc": "Noon Sakinah before 15 letters", "example": "مِنْ قَبْلِ"},
                 {"id": "iqlab", "name_ar": "إقلاب", "name_en": "Convert", "desc": "Noon Sakinah before ب", "example": "أَنْبِئْهُمْ"},
             ]},
            {"id": "w5s3", "title_ar": "المدود", "title_en": "Madd (Stretching)", "type": "tajweed",
             "rules": [
                 {"id": "madd_tabii", "name_ar": "مد طبيعي", "name_en": "Natural (2 counts)", "desc": "Alif after Fathah, Ya after Kasrah, Waw after Dammah", "example": "قَالَ"},
             ]},
            {"id": "w5s4", "title_ar": "القلقلة", "title_en": "Qalqalah", "type": "tajweed",
             "rules": [
                 {"id": "qalqalah", "name_ar": "قلقلة", "name_en": "Echo", "desc": "Bouncing sound on ق ط ب ج د with Sukoon", "example": "أَحَدْ"},
             ]},
            {"id": "w5boss", "title_ar": "تحدي التجويد", "title_en": "Tajweed Boss", "type": "boss"},
        ],
    },
]

def build_flat_stages():
    """Build a flat list of all stages with world info."""
    stages = []
    for w in JOURNEY_WORLDS:
        for s in w["stages"]:
            stages.append({**s, "world_id": w["id"], "world_title_ar": w["title_ar"], "world_emoji": w["emoji"], "world_color": w["color"]})
    return stages

ALL_STAGES = build_flat_stages()
STAGE_INDEX = {s["id"]: i for i, s in enumerate(ALL_STAGES)}


@router.get("/kids-zone/journey")
async def get_journey(user_id: str = ""):
    """Get the full learning journey map with user progress."""
    # Get user progress
    prog = await db.kids_journey.find_one({"user_id": user_id}, {"_id": 0}) if user_id else None
    if not prog:
        prog = {"user_id": user_id or "guest", "completed": {}, "stars": {}, "current_stage": "w1s1"}

    completed = prog.get("completed", {})
    stars_map = prog.get("stars", {})
    current = prog.get("current_stage", "w1s1")

    # Build worlds with unlock status
    worlds = []
    prev_unlocked = True
    for w in JOURNEY_WORLDS:
        stages = []
        world_completed = 0
        for s in w["stages"]:
            sid = s["id"]
            is_complete = completed.get(sid, False)
            st = stars_map.get(sid, 0)
            is_current = sid == current
            is_unlocked = prev_unlocked
            if is_complete:
                world_completed += 1
                prev_unlocked = True
            elif is_current:
                is_unlocked = True
                prev_unlocked = False
            else:
                prev_unlocked = False

            stages.append({
                "id": sid,
                "title_ar": s["title_ar"],
                "title_en": s.get("title_en", ""),
                "type": s["type"],
                "unlocked": is_unlocked,
                "completed": is_complete,
                "stars": st,
                "is_current": is_current,
                "is_boss": s["type"] == "boss",
            })
        worlds.append({
            "id": w["id"],
            "title_ar": w["title_ar"],
            "title_en": w["title_en"],
            "emoji": w["emoji"],
            "color": w["color"],
            "description_ar": w["description_ar"],
            "description_en": w["description_en"],
            "stages": stages,
            "progress": world_completed,
            "total": len(stages),
        })
    
    # Get mosque/XP data
    skill = await db.kids_skills.find_one({"user_id": user_id}, {"_id": 0}) if user_id else None
    xp = skill.get("total_xp", 0) if skill else 0
    bricks_val = skill.get("golden_bricks", 0) if skill else 0

    return {
        "success": True,
        "worlds": worlds,
        "current_stage": current,
        "total_xp": xp,
        "golden_bricks": bricks_val,
        "mosque": get_mosque_progress(bricks_val),
    }


@router.get("/kids-zone/stage/{stage_id}")
async def get_stage_content(stage_id: str, user_id: str = ""):
    """Get the IRS content for a specific stage."""
    import random
    if stage_id not in STAGE_INDEX:
        raise HTTPException(status_code=404, detail="Stage not found")

    idx = STAGE_INDEX[stage_id]
    stage = ALL_STAGES[idx]
    stype = stage["type"]

    # Build IRS (Introduce-Recognize-Say) activities
    activities = []

    if stype == "letters":
        letter_ids = stage.get("letters", [])
        letters = [lt for lt in ARABIC_LETTERS if lt["id"] in letter_ids]
        # INTRODUCE: Show letters with names and sounds
        activities.append({
            "phase": "introduce",
            "phase_ar": "تعرّف",
            "phase_emoji": "👁️",
            "content": [{
                "id": lt["id"], "letter": lt["letter"], "name_ar": lt["name_ar"],
                "name_en": lt["name_en"], "transliteration": lt["transliteration"],
                "audio_hint": lt["audio_hint"], "example_word": lt["example_word"],
                "example_meaning": lt["example_meaning"],
            } for lt in letters],
        })
        # RECOGNIZE: Find letters in grid
        target = random.choice(letters)
        distractors = [lt for lt in ARABIC_LETTERS if lt["id"] not in letter_ids]
        grid_size = 3
        grid = []
        for r in range(grid_size):
            row = []
            for c in range(grid_size):
                if r == 0 and c == 0:
                    row.append({"letter": target["letter"], "id": target["id"], "correct": True})
                else:
                    d = random.choice(distractors)
                    row.append({"letter": d["letter"], "id": d["id"], "correct": False})
            grid.append(row)
        tr = random.randint(0, grid_size - 1)
        tc = random.randint(0, grid_size - 1)
        grid[0][0], grid[tr][tc] = grid[tr][tc], grid[0][0]
        activities.append({
            "phase": "recognize",
            "phase_ar": "اكتشف",
            "phase_emoji": "🔍",
            "game_type": "find_letter",
            "target": {"id": target["id"], "letter": target["letter"], "name_ar": target["name_ar"], "audio_hint": target["audio_hint"]},
            "grid": grid, "grid_size": grid_size,
        })
        # SAY: Pronounce each letter
        activities.append({
            "phase": "say",
            "phase_ar": "انطق",
            "phase_emoji": "🎤",
            "targets": [{"id": lt["id"], "letter": lt["letter"], "word": lt["example_word"], "transliteration": lt["transliteration"]} for lt in letters],
        })

    elif stype == "harakat":
        examples = stage.get("examples", [])
        activities.append({
            "phase": "introduce", "phase_ar": "تعرّف", "phase_emoji": "👁️",
            "haraka": stage.get("haraka"), "title_ar": stage["title_ar"],
            "content": examples,
        })
        # RECOGNIZE: Match letter+haraka to sound
        random.shuffle(examples)
        activities.append({
            "phase": "recognize", "phase_ar": "اكتشف", "phase_emoji": "🔍",
            "game_type": "match_sound",
            "pairs": [{"display": ex["letter"], "answer": ex["sound"]} for ex in examples],
        })
        activities.append({
            "phase": "say", "phase_ar": "انطق", "phase_emoji": "🎤",
            "targets": [{"letter": ex["letter"], "word": ex["letter"], "transliteration": ex["sound"]} for ex in examples],
        })

    elif stype == "reading":
        words = stage.get("words", [])
        activities.append({
            "phase": "introduce", "phase_ar": "تعرّف", "phase_emoji": "👁️",
            "content": words,
        })
        shuffled_meanings = list(words)
        random.shuffle(shuffled_meanings)
        activities.append({
            "phase": "recognize", "phase_ar": "اكتشف", "phase_emoji": "🔍",
            "game_type": "match_meaning",
            "words": [{"ar": w["ar"], "trans": w["trans"]} for w in words],
            "meanings": [{"ar": w["ar"], "en": w["en"]} for w in shuffled_meanings],
        })
        activities.append({
            "phase": "say", "phase_ar": "انطق", "phase_emoji": "🎤",
            "targets": [{"letter": w["ar"], "word": w["ar"], "transliteration": w["trans"]} for w in words],
        })

    elif stype == "surah":
        ayahs = stage.get("ayahs", [])
        meanings = stage.get("meanings", [])
        activities.append({
            "phase": "introduce", "phase_ar": "تعرّف", "phase_emoji": "👁️",
            "surah_name": stage["title_ar"],
            "ayahs": [{"text": a, "meaning": meanings[i] if i < len(meanings) else ""} for i, a in enumerate(ayahs)],
        })
        # RECOGNIZE: Put ayahs in correct order
        indices = list(range(len(ayahs)))
        shuffled = list(indices)
        random.shuffle(shuffled)
        activities.append({
            "phase": "recognize", "phase_ar": "اكتشف", "phase_emoji": "🔍",
            "game_type": "order_ayahs",
            "shuffled_ayahs": [{"text": ayahs[i], "correct_index": i} for i in shuffled],
        })
        activities.append({
            "phase": "say", "phase_ar": "انطق", "phase_emoji": "🎤",
            "targets": [{"letter": a, "word": a, "transliteration": ""} for a in ayahs[:3]],
        })

    elif stype == "tajweed":
        rules = stage.get("rules", [])
        activities.append({
            "phase": "introduce", "phase_ar": "تعرّف", "phase_emoji": "👁️",
            "content": rules,
        })
        target_rule = random.choice(rules)
        all_rule_ids = ["izhar", "idgham", "ikhfa", "iqlab", "madd_tabii", "qalqalah"]
        choices = [target_rule["id"]]
        others = [r for r in all_rule_ids if r != target_rule["id"]]
        choices.extend(random.sample(others, min(2, len(others))))
        random.shuffle(choices)
        activities.append({
            "phase": "recognize", "phase_ar": "اكتشف", "phase_emoji": "🔍",
            "game_type": "identify_rule",
            "example": target_rule["example"],
            "rule_name_ar": target_rule["name_ar"],
            "correct": target_rule["id"],
            "choices": choices,
        })
        activities.append({
            "phase": "say", "phase_ar": "انطق", "phase_emoji": "🎤",
            "targets": [{"letter": r["example"], "word": r["example"], "transliteration": r["name_en"]} for r in rules],
        })

    elif stype == "boss":
        activities.append({
            "phase": "boss", "phase_ar": "تحدي", "phase_emoji": "🏆",
            "world_id": stage["world_id"],
        })

    return {
        "success": True,
        "stage": {
            "id": stage_id,
            "title_ar": stage["title_ar"],
            "title_en": stage.get("title_en", ""),
            "type": stype,
            "world_id": stage["world_id"],
            "world_emoji": stage["world_emoji"],
            "world_color": stage["world_color"],
        },
        "activities": activities,
    }


@router.post("/kids-zone/complete-stage")
async def complete_stage(payload: dict):
    """Mark a stage as complete and unlock next."""
    user_id = payload.get("user_id", "guest")
    stage_id = payload.get("stage_id", "")
    stars_earned = min(3, max(1, payload.get("stars", 1)))

    if stage_id not in STAGE_INDEX:
        raise HTTPException(status_code=404, detail="Stage not found")

    idx = STAGE_INDEX[stage_id]
    next_id = ALL_STAGES[idx + 1]["id"] if idx + 1 < len(ALL_STAGES) else None

    # Update journey progress
    prog = await db.kids_journey.find_one({"user_id": user_id})
    if not prog:
        prog = {"id": str(uuid.uuid4()), "user_id": user_id, "completed": {}, "stars": {}, "current_stage": "w1s1"}
        await db.kids_journey.insert_one(prog)

    update = {
        "$set": {
            f"completed.{stage_id}": True,
            f"stars.{stage_id}": max(stars_earned, prog.get("stars", {}).get(stage_id, 0)),
        }
    }
    if next_id:
        update["$set"]["current_stage"] = next_id

    await db.kids_journey.update_one({"user_id": user_id}, update)

    # Also award XP and bricks
    xp_reward = 15 if "boss" in stage_id else 10
    brick_reward = 3 if "boss" in stage_id else 1
    await db.kids_skills.update_one(
        {"user_id": user_id},
        {"$inc": {"total_xp": xp_reward, "golden_bricks": brick_reward, "games_played": 1}},
        upsert=True,
    )

    skill = await db.kids_skills.find_one({"user_id": user_id}, {"_id": 0})
    bricks_val = skill.get("golden_bricks", 0) if skill else brick_reward

    return {
        "success": True,
        "stars": stars_earned,
        "xp_earned": xp_reward,
        "bricks_earned": brick_reward,
        "next_stage": next_id,
        "mosque": get_mosque_progress(bricks_val),
    }



# ==================== KIDS LEARNING MODULE API ====================

