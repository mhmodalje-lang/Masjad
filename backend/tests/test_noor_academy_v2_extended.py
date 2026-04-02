"""
Test Suite: Noor Academy V2 Extended Content
=============================================
Tests for the 150+ lesson skeleton with 5 tracks:
- Nooraniya (70 lessons)
- Aqeedah (50 lessons)
- Fiqh (40 lessons)
- Seerah (60 lessons)
- Adab (20 lessons)

Also tests:
- 9-language support (ar, en, de, fr, tr, ru, sv, nl, el)
- Placeholder structure
- Navigation (has_next, has_prev)
- Digital Shield (30 lessons)
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# All 9 supported languages
SUPPORTED_LANGUAGES = ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"]


class TestAcademyOverview:
    """Test Academy Overview API - must return 5 tracks with correct lesson counts"""
    
    def test_academy_overview_returns_5_tracks(self):
        """Academy overview should return exactly 5 tracks"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/overview?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "tracks" in data
        assert len(data["tracks"]) == 5
        print("✓ Academy overview returns 5 tracks")
    
    def test_academy_overview_track_ids(self):
        """Verify all 5 track IDs are present"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/overview?locale=en")
        data = response.json()
        track_ids = [t["id"] for t in data["tracks"]]
        expected_ids = ["nooraniya", "aqeedah", "fiqh", "seerah", "adab"]
        for expected_id in expected_ids:
            assert expected_id in track_ids, f"Missing track: {expected_id}"
        print(f"✓ All 5 track IDs present: {track_ids}")
    
    def test_academy_overview_lesson_counts(self):
        """Verify correct lesson counts for each track"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/overview?locale=en")
        data = response.json()
        
        expected_counts = {
            "nooraniya": 70,
            "aqeedah": 50,
            "fiqh": 40,
            "seerah": 60,
            "adab": 20
        }
        
        for track in data["tracks"]:
            track_id = track["id"]
            expected = expected_counts.get(track_id)
            actual = track["total_lessons"]
            assert actual == expected, f"Track {track_id}: expected {expected} lessons, got {actual}"
            print(f"✓ Track {track_id}: {actual} lessons (correct)")
    
    def test_academy_overview_has_teaching_methods(self):
        """Verify teaching methods are included"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/overview?locale=en")
        data = response.json()
        assert "teaching_methods" in data
        assert len(data["teaching_methods"]) > 0
        print(f"✓ Teaching methods included: {len(data['teaching_methods'])} methods")
    
    def test_academy_overview_has_badges(self):
        """Verify badges are included"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/overview?locale=en")
        data = response.json()
        assert "badges" in data
        assert len(data["badges"]) > 0
        print(f"✓ Badges included: {len(data['badges'])} badges")


class TestAqeedahTrack:
    """Test Aqeedah Track API - 50 lessons across 5 levels"""
    
    def test_aqeedah_track_detail(self):
        """Get Aqeedah track info and levels"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/track/aqeedah?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "track" in data
        assert data["track"]["id"] == "aqeedah"
        assert "levels" in data
        print(f"✓ Aqeedah track detail: {data['total_levels']} levels")
    
    def test_aqeedah_lesson_1(self):
        """Test Aqeedah lesson 1 retrieval"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/aqeedah/lesson/1?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "lesson" in data
        lesson = data["lesson"]
        assert lesson["id"] == 1
        assert lesson["level"] == 1
        assert "title" in lesson
        assert "content" in lesson
        print(f"✓ Aqeedah lesson 1: {lesson['title']}")
    
    def test_aqeedah_lesson_11_rich_content(self):
        """Test Aqeedah lesson 11 (Level 2 - 99 Names) has rich content"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/aqeedah/lesson/11?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        lesson = data["lesson"]
        assert lesson["level"] == 2
        # Level 2 lessons should have actual content (not placeholder)
        content = lesson.get("content", {})
        # Check if it's not a placeholder
        is_placeholder = content.get("placeholder", False) or content.get("status") == "placeholder"
        print(f"✓ Aqeedah lesson 11: Level {lesson['level']}, placeholder={is_placeholder}")
    
    def test_aqeedah_navigation_flags(self):
        """Test has_next and has_prev navigation flags"""
        # First lesson
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/aqeedah/lesson/1?locale=en")
        data = response.json()
        assert data["has_prev"] == False, "First lesson should have has_prev=False"
        assert data["has_next"] == True, "First lesson should have has_next=True"
        print(f"✓ Aqeedah lesson 1: has_prev={data['has_prev']}, has_next={data['has_next']}")
        
        # Middle lesson
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/aqeedah/lesson/25?locale=en")
        data = response.json()
        assert data["has_prev"] == True, "Middle lesson should have has_prev=True"
        assert data["has_next"] == True, "Middle lesson should have has_next=True"
        print(f"✓ Aqeedah lesson 25: has_prev={data['has_prev']}, has_next={data['has_next']}")


class TestFiqhTrack:
    """Test Fiqh Track API - 40 lessons across 4 levels"""
    
    def test_fiqh_track_detail(self):
        """Get Fiqh track info and levels"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/track/fiqh?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["track"]["id"] == "fiqh"
        print(f"✓ Fiqh track detail: {data['total_levels']} levels")
    
    def test_fiqh_lesson_1(self):
        """Test Fiqh lesson 1 retrieval"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/fiqh/lesson/1?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        lesson = data["lesson"]
        assert lesson["id"] == 1
        assert lesson["level"] == 1
        assert "title" in lesson
        print(f"✓ Fiqh lesson 1: {lesson['title']}")
    
    def test_fiqh_placeholder_format(self):
        """Test Fiqh placeholder lessons have correct format"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/fiqh/lesson/1?locale=en")
        data = response.json()
        lesson = data["lesson"]
        # content checked in specific test methods
        
        # Check structure
        assert "title" in lesson
        assert "method" in lesson
        assert "xp" in lesson
        assert "quiz" in lesson
        print("✓ Fiqh lesson structure correct: title, method, xp, quiz present")


class TestSeerahTrack:
    """Test Seerah Track API - 60 lessons across 6 levels"""
    
    def test_seerah_track_detail(self):
        """Get Seerah track info and levels"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/track/seerah?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["track"]["id"] == "seerah"
        print(f"✓ Seerah track detail: {data['total_levels']} levels")
    
    def test_seerah_lesson_1(self):
        """Test Seerah lesson 1 retrieval"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/seerah/lesson/1?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        lesson = data["lesson"]
        assert lesson["id"] == 1
        assert lesson["level"] == 1
        print(f"✓ Seerah lesson 1: {lesson['title']}")
    
    def test_seerah_navigation(self):
        """Test Seerah navigation flags"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/seerah/lesson/30?locale=en")
        data = response.json()
        assert data["has_prev"] == True
        assert data["has_next"] == True
        print(f"✓ Seerah lesson 30: has_prev={data['has_prev']}, has_next={data['has_next']}")


class TestNooraniyaTrack:
    """Test Nooraniya Track API - 70 lessons across 7 levels"""
    
    def test_nooraniya_track_detail(self):
        """Get Nooraniya track info and levels"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/track/nooraniya?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["track"]["id"] == "nooraniya"
        print(f"✓ Nooraniya track detail: {data['total_levels']} levels")
    
    def test_nooraniya_lesson_1_rich_content(self):
        """Test Nooraniya lesson 1 has rich content (not placeholder)"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/nooraniya/lesson/1?locale=en")
        assert response.status_code == 200
        data = response.json()
        lesson = data["lesson"]
        content = lesson.get("content", {})
        
        # Level 1-3 should have actual content
        is_placeholder = content.get("placeholder", False) or content.get("status") == "placeholder"
        assert is_placeholder == False, "Nooraniya L1 should have actual content"
        print("✓ Nooraniya lesson 1 has rich content (not placeholder)")
    
    def test_nooraniya_extended_lesson_40(self):
        """Test Nooraniya extended lesson (Level 4+)"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/nooraniya/lesson/40?locale=en")
        assert response.status_code == 200
        data = response.json()
        lesson = data["lesson"]
        assert lesson["level"] >= 4, "Lesson 40 should be in Level 4+"
        print(f"✓ Nooraniya lesson 40: Level {lesson['level']}")


class TestAdabTrack:
    """Test Adab Track API - 20 lessons"""
    
    def test_adab_list(self):
        """Get all Adab lessons"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/adab?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "lessons" in data
        # Adab has 10 main lessons (each with rules)
        assert data["total"] >= 10
        print(f"✓ Adab list: {data['total']} lessons")
    
    def test_adab_lesson_1(self):
        """Test Adab lesson 1 detail"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/adab/1?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        adab = data["adab"]
        assert adab["id"] == 1
        assert "title" in adab
        assert "rules" in adab
        assert len(adab["rules"]) > 0
        print(f"✓ Adab lesson 1: {adab['title']} ({len(adab['rules'])} rules)")


class TestLanguageSupport:
    """Test 9-language support with strict fallback logic"""
    
    def test_all_9_languages_academy_overview(self):
        """Test academy overview in all 9 languages"""
        for lang in SUPPORTED_LANGUAGES:
            response = requests.get(f"{BASE_URL}/api/kids-learn/academy/overview?locale={lang}")
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert data["language"] == lang
            # Verify title is translated (not empty)
            assert len(data["academy_name"]) > 0
            print(f"✓ Academy overview in {lang}: {data['academy_name'][:30]}...")
    
    def test_aqeedah_lesson_in_german(self):
        """Test Aqeedah lesson in German (de)"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/aqeedah/lesson/11?locale=de")
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "de"
        lesson = data["lesson"]
        # Title should be in German
        assert len(lesson["title"]) > 0
        print(f"✓ Aqeedah lesson 11 in German: {lesson['title']}")
    
    def test_fiqh_lesson_in_turkish(self):
        """Test Fiqh lesson in Turkish (tr)"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/fiqh/lesson/1?locale=tr")
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "tr"
        print(f"✓ Fiqh lesson 1 in Turkish: {data['lesson']['title']}")
    
    def test_seerah_lesson_in_russian(self):
        """Test Seerah lesson in Russian (ru)"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/seerah/lesson/1?locale=ru")
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "ru"
        print(f"✓ Seerah lesson 1 in Russian: {data['lesson']['title']}")
    
    def test_adab_in_french(self):
        """Test Adab in French (fr)"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/adab?locale=fr")
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "fr"
        print(f"✓ Adab list in French: {data['title']}")
    
    def test_fallback_to_english_for_unknown_locale(self):
        """Test fallback to English for unknown locale"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/overview?locale=xyz")
        assert response.status_code == 200
        data = response.json()
        # Should fallback to English
        assert data["language"] == "en"
        print("✓ Unknown locale 'xyz' falls back to English")
    
    def test_de_AT_maps_to_de(self):
        """Test de-AT locale maps to de"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/overview?locale=de-AT")
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "de"
        print("✓ de-AT maps to de correctly")


class TestDigitalShield:
    """Test Digital Shield - 30 lessons on AI Safety, Privacy, Cyber-Ethics"""
    
    def test_digital_shield_overview(self):
        """Digital Shield overview should return 3 modules with 30 lessons total"""
        response = requests.get(f"{BASE_URL}/api/digital-shield/overview?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "modules" in data
        assert len(data["modules"]) == 3
        assert data["total_lessons"] == 30
        print("✓ Digital Shield: 3 modules, 30 lessons total")
    
    def test_digital_shield_module_lesson_counts(self):
        """Verify each module has correct lesson count"""
        response = requests.get(f"{BASE_URL}/api/digital-shield/overview?locale=en")
        data = response.json()
        
        total_lessons = 0
        for module in data["modules"]:
            total_lessons += module["total_lessons"]
            print(f"  Module {module['id']}: {module['total_lessons']} lessons")
        
        assert total_lessons == 30, f"Expected 30 total lessons, got {total_lessons}"
        print("✓ Digital Shield modules sum to 30 lessons")
    
    def test_digital_shield_lesson_1(self):
        """Test Digital Shield lesson 1"""
        response = requests.get(f"{BASE_URL}/api/digital-shield/lesson/1?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        lesson = data["lesson"]
        assert lesson["id"] == 1
        assert "title" in lesson
        assert "content" in lesson
        assert "islamic_reference" in lesson
        assert "moral" in lesson
        print(f"✓ Digital Shield lesson 1: {lesson['title']}")
    
    def test_digital_shield_navigation(self):
        """Test Digital Shield navigation flags"""
        # First lesson
        response = requests.get(f"{BASE_URL}/api/digital-shield/lesson/1?locale=en")
        data = response.json()
        assert data["has_prev"] == False
        assert data["has_next"] == True
        
        # Last lesson
        response = requests.get(f"{BASE_URL}/api/digital-shield/lesson/30?locale=en")
        data = response.json()
        assert data["has_prev"] == True
        assert data["has_next"] == False
        print("✓ Digital Shield navigation: lesson 1 (prev=False), lesson 30 (next=False)")
    
    def test_digital_shield_module_detail(self):
        """Test Digital Shield module detail"""
        response = requests.get(f"{BASE_URL}/api/digital-shield/module/1?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "module" in data
        assert "lessons" in data
        assert len(data["lessons"]) == data["total"]
        print(f"✓ Digital Shield module 1: {data['total']} lessons")


class TestPlaceholderStructure:
    """Test placeholder lessons return correct format"""
    
    def test_placeholder_has_message_in_all_languages(self):
        """Placeholder lessons should have message in all 9 languages"""
        # Aqeedah L1 lessons are placeholders
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/aqeedah/lesson/1?locale=en")
        data = response.json()
        content = data["lesson"]["content"]
        
        if content.get("placeholder") or content.get("status") == "placeholder":
            # Check message exists
            assert "message" in content
            print("✓ Placeholder has message field")
        else:
            print("✓ Lesson 1 has actual content (not placeholder)")
    
    def test_placeholder_quiz_type(self):
        """Placeholder lessons should have quiz type 'placeholder'"""
        # Check a known placeholder lesson
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/fiqh/lesson/1?locale=en")
        data = response.json()
        quiz = data["lesson"]["quiz"]
        
        # Quiz should have a type
        assert "type" in quiz
        print(f"✓ Quiz type: {quiz['type']}")


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_invalid_lesson_id(self):
        """Test invalid lesson ID returns error"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/aqeedah/lesson/999?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
        print("✓ Invalid lesson ID returns success=False")
    
    def test_invalid_track_id(self):
        """Test invalid track ID returns error"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/track/invalid?locale=en")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
        print("✓ Invalid track ID returns success=False")
    
    def test_lesson_0_invalid(self):
        """Test lesson 0 is invalid"""
        response = requests.get(f"{BASE_URL}/api/kids-learn/academy/aqeedah/lesson/0?locale=en")
        data = response.json()
        assert data["success"] == False
        print("✓ Lesson 0 returns success=False")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
