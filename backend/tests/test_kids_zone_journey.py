"""
Kids Zone Journey API Tests - Iteration 15
Tests the new journey-based APIs for the Kids Zone feature:
- GET /api/kids-zone/journey - Get learning journey map with worlds and stages
- GET /api/kids-zone/stage/{stage_id} - Get IRS activities for a stage
- POST /api/kids-zone/complete-stage - Complete a stage and unlock next
"""
import pytest
import requests
import os
import time

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://fast-reload-app.preview.emergentagent.com')

# Test user IDs
TEST_USER_ID = f"kid_test_pytest_{int(time.time())}"


class TestKidsZoneJourney:
    """Tests for /api/kids-zone/journey endpoint"""
    
    def test_journey_returns_success(self):
        """Test that journey endpoint returns success"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/journey?user_id={TEST_USER_ID}")
        assert response.status_code == 200
        data = response.json()
        assert data.get("success") == True
        print(f"✓ Journey endpoint returns success")
    
    def test_journey_has_worlds_array(self):
        """Test that journey returns worlds array"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/journey?user_id={TEST_USER_ID}")
        data = response.json()
        assert "worlds" in data
        assert isinstance(data["worlds"], list)
        assert len(data["worlds"]) >= 5, "Should have at least 5 worlds"
        print(f"✓ Journey has {len(data['worlds'])} worlds")
    
    def test_journey_has_5_worlds_with_correct_structure(self):
        """Test that all 5 worlds exist with correct structure"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/journey?user_id={TEST_USER_ID}")
        data = response.json()
        worlds = data["worlds"]
        
        expected_world_ids = ["w1", "w2", "w3", "w4", "w5"]
        actual_world_ids = [w["id"] for w in worlds]
        
        for wid in expected_world_ids:
            assert wid in actual_world_ids, f"World {wid} should exist"
        
        # Check world structure
        for world in worlds:
            assert "id" in world
            assert "title_ar" in world
            assert "title_en" in world
            assert "emoji" in world
            assert "color" in world
            assert "description_ar" in world
            assert "description_en" in world
            assert "stages" in world
            assert "progress" in world
            assert "total" in world
            assert isinstance(world["stages"], list)
            assert len(world["stages"]) > 0, f"World {world['id']} should have stages"
        
        print(f"✓ All 5 worlds exist with correct structure")
    
    def test_journey_stages_have_correct_structure(self):
        """Test that stages have correct structure"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/journey?user_id={TEST_USER_ID}")
        data = response.json()
        
        for world in data["worlds"]:
            for stage in world["stages"]:
                assert "id" in stage
                assert "title_ar" in stage
                assert "title_en" in stage
                assert "type" in stage
                assert "unlocked" in stage
                assert "completed" in stage
                assert "stars" in stage
                assert "is_current" in stage
                assert "is_boss" in stage
        
        print(f"✓ All stages have correct structure")
    
    def test_journey_first_stage_unlocked(self):
        """Test that first stage (w1s1) is unlocked for new user"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/journey?user_id={TEST_USER_ID}")
        data = response.json()
        
        first_world = data["worlds"][0]
        first_stage = first_world["stages"][0]
        
        assert first_stage["id"] == "w1s1"
        assert first_stage["unlocked"] == True
        assert first_stage["is_current"] == True
        print(f"✓ First stage w1s1 is unlocked and current")
    
    def test_journey_has_current_stage(self):
        """Test that journey returns current_stage"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/journey?user_id={TEST_USER_ID}")
        data = response.json()
        
        assert "current_stage" in data
        assert data["current_stage"] == "w1s1", "New user should start at w1s1"
        print(f"✓ Current stage is {data['current_stage']}")
    
    def test_journey_has_xp_and_bricks(self):
        """Test that journey returns XP and golden bricks"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/journey?user_id={TEST_USER_ID}")
        data = response.json()
        
        assert "total_xp" in data
        assert "golden_bricks" in data
        assert isinstance(data["total_xp"], int)
        assert isinstance(data["golden_bricks"], int)
        print(f"✓ XP: {data['total_xp']}, Bricks: {data['golden_bricks']}")
    
    def test_journey_has_mosque_progress(self):
        """Test that journey returns mosque progress"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/journey?user_id={TEST_USER_ID}")
        data = response.json()
        
        assert "mosque" in data
        assert data["mosque"] is not None
        print(f"✓ Mosque progress included")


class TestKidsZoneStage:
    """Tests for /api/kids-zone/stage/{stage_id} endpoint"""
    
    def test_stage_w1s1_returns_success(self):
        """Test that stage w1s1 returns success"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w1s1?user_id={TEST_USER_ID}")
        assert response.status_code == 200
        data = response.json()
        assert data.get("success") == True
        print(f"✓ Stage w1s1 returns success")
    
    def test_stage_has_activities_array(self):
        """Test that stage returns activities array"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w1s1?user_id={TEST_USER_ID}")
        data = response.json()
        
        assert "activities" in data
        assert isinstance(data["activities"], list)
        assert len(data["activities"]) >= 3, "Should have at least 3 activities (introduce, recognize, say)"
        print(f"✓ Stage has {len(data['activities'])} activities")
    
    def test_stage_has_irs_phases(self):
        """Test that stage has Introduce, Recognize, Say phases"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w1s1?user_id={TEST_USER_ID}")
        data = response.json()
        
        phases = [a["phase"] for a in data["activities"]]
        assert "introduce" in phases, "Should have introduce phase"
        assert "recognize" in phases, "Should have recognize phase"
        assert "say" in phases, "Should have say phase"
        print(f"✓ Stage has IRS phases: {phases}")
    
    def test_stage_introduce_has_content(self):
        """Test that introduce phase has content with letters"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w1s1?user_id={TEST_USER_ID}")
        data = response.json()
        
        introduce = next((a for a in data["activities"] if a["phase"] == "introduce"), None)
        assert introduce is not None
        assert "content" in introduce
        assert len(introduce["content"]) > 0
        
        # Check letter content structure
        letter = introduce["content"][0]
        assert "letter" in letter
        assert "name_ar" in letter
        print(f"✓ Introduce phase has {len(introduce['content'])} letters")
    
    def test_stage_recognize_has_grid(self):
        """Test that recognize phase has grid for find_letter game"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w1s1?user_id={TEST_USER_ID}")
        data = response.json()
        
        recognize = next((a for a in data["activities"] if a["phase"] == "recognize"), None)
        assert recognize is not None
        assert recognize.get("game_type") == "find_letter"
        assert "target" in recognize
        assert "grid" in recognize
        assert "grid_size" in recognize
        print(f"✓ Recognize phase has grid with target letter")
    
    def test_stage_say_has_targets(self):
        """Test that say phase has targets for pronunciation"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w1s1?user_id={TEST_USER_ID}")
        data = response.json()
        
        say = next((a for a in data["activities"] if a["phase"] == "say"), None)
        assert say is not None
        assert "targets" in say
        assert len(say["targets"]) > 0
        
        target = say["targets"][0]
        assert "letter" in target or "word" in target
        print(f"✓ Say phase has {len(say['targets'])} targets")
    
    def test_stage_info_structure(self):
        """Test that stage info has correct structure"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w1s1?user_id={TEST_USER_ID}")
        data = response.json()
        
        assert "stage" in data
        stage = data["stage"]
        assert stage["id"] == "w1s1"
        assert "title_ar" in stage
        assert "title_en" in stage
        assert "type" in stage
        assert "world_id" in stage
        assert "world_emoji" in stage
        print(f"✓ Stage info: {stage['title_ar']} ({stage['title_en']})")
    
    def test_stage_not_found(self):
        """Test that invalid stage returns 404"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/invalid_stage?user_id={TEST_USER_ID}")
        assert response.status_code == 404
        print(f"✓ Invalid stage returns 404")


class TestKidsZoneCompleteStage:
    """Tests for /api/kids-zone/complete-stage endpoint"""
    
    def test_complete_stage_returns_success(self):
        """Test that complete-stage returns success"""
        response = requests.post(
            f"{BASE_URL}/api/kids-zone/complete-stage",
            json={"user_id": TEST_USER_ID, "stage_id": "w1s1", "stars": 3}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("success") == True
        print(f"✓ Complete stage returns success")
    
    def test_complete_stage_returns_rewards(self):
        """Test that complete-stage returns XP and bricks earned"""
        response = requests.post(
            f"{BASE_URL}/api/kids-zone/complete-stage",
            json={"user_id": TEST_USER_ID, "stage_id": "w1s1", "stars": 3}
        )
        data = response.json()
        
        assert "xp_earned" in data
        assert "bricks_earned" in data
        assert "stars" in data
        assert data["xp_earned"] > 0
        assert data["bricks_earned"] > 0
        print(f"✓ Rewards: {data['xp_earned']} XP, {data['bricks_earned']} bricks, {data['stars']} stars")
    
    def test_complete_stage_returns_next_stage(self):
        """Test that complete-stage returns next_stage"""
        response = requests.post(
            f"{BASE_URL}/api/kids-zone/complete-stage",
            json={"user_id": TEST_USER_ID, "stage_id": "w1s1", "stars": 3}
        )
        data = response.json()
        
        assert "next_stage" in data
        assert data["next_stage"] == "w1s2", "Next stage after w1s1 should be w1s2"
        print(f"✓ Next stage: {data['next_stage']}")
    
    def test_complete_stage_returns_mosque(self):
        """Test that complete-stage returns mosque progress"""
        response = requests.post(
            f"{BASE_URL}/api/kids-zone/complete-stage",
            json={"user_id": TEST_USER_ID, "stage_id": "w1s1", "stars": 3}
        )
        data = response.json()
        
        assert "mosque" in data
        print(f"✓ Mosque progress included in response")
    
    def test_complete_stage_invalid_stage(self):
        """Test that invalid stage returns 404"""
        response = requests.post(
            f"{BASE_URL}/api/kids-zone/complete-stage",
            json={"user_id": TEST_USER_ID, "stage_id": "invalid_stage", "stars": 3}
        )
        assert response.status_code == 404
        print(f"✓ Invalid stage returns 404")


class TestKidsZoneProgression:
    """Tests for stage progression logic"""
    
    def test_progression_after_completion(self):
        """Test that after completing w1s1, current_stage becomes w1s2 and w1s2 is unlocked"""
        # Use a unique user for this test
        progression_user = f"kid_test_progression_{int(time.time())}"
        
        # First, check initial state
        response = requests.get(f"{BASE_URL}/api/kids-zone/journey?user_id={progression_user}")
        data = response.json()
        assert data["current_stage"] == "w1s1"
        
        # Complete w1s1
        response = requests.post(
            f"{BASE_URL}/api/kids-zone/complete-stage",
            json={"user_id": progression_user, "stage_id": "w1s1", "stars": 3}
        )
        assert response.status_code == 200
        
        # Check progression
        response = requests.get(f"{BASE_URL}/api/kids-zone/journey?user_id={progression_user}")
        data = response.json()
        
        assert data["current_stage"] == "w1s2", "Current stage should be w1s2 after completing w1s1"
        
        # Check w1s1 is completed
        w1 = next((w for w in data["worlds"] if w["id"] == "w1"), None)
        w1s1 = next((s for s in w1["stages"] if s["id"] == "w1s1"), None)
        w1s2 = next((s for s in w1["stages"] if s["id"] == "w1s2"), None)
        
        assert w1s1["completed"] == True, "w1s1 should be completed"
        assert w1s1["stars"] == 3, "w1s1 should have 3 stars"
        assert w1s2["unlocked"] == True, "w1s2 should be unlocked"
        assert w1s2["is_current"] == True, "w1s2 should be current"
        
        print(f"✓ Progression works: w1s1 completed, w1s2 unlocked and current")


class TestKidsZoneWorldTypes:
    """Tests for different world/stage types"""
    
    def test_letters_stage_type(self):
        """Test letters stage type (w1s1)"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w1s1?user_id={TEST_USER_ID}")
        data = response.json()
        assert data["stage"]["type"] == "letters"
        print(f"✓ Letters stage type works")
    
    def test_harakat_stage_type(self):
        """Test harakat stage type (w2s1)"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w2s1?user_id={TEST_USER_ID}")
        data = response.json()
        assert data["stage"]["type"] == "harakat"
        
        # Check harakat-specific content
        introduce = next((a for a in data["activities"] if a["phase"] == "introduce"), None)
        assert "haraka" in introduce or "examples" in introduce or "content" in introduce
        print(f"✓ Harakat stage type works")
    
    def test_reading_stage_type(self):
        """Test reading stage type (w3s1)"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w3s1?user_id={TEST_USER_ID}")
        data = response.json()
        assert data["stage"]["type"] == "reading"
        print(f"✓ Reading stage type works")
    
    def test_surah_stage_type(self):
        """Test surah stage type (w4s1)"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w4s1?user_id={TEST_USER_ID}")
        data = response.json()
        assert data["stage"]["type"] == "surah"
        
        # Check surah-specific content
        introduce = next((a for a in data["activities"] if a["phase"] == "introduce"), None)
        assert "ayahs" in introduce or "surah_name" in introduce
        print(f"✓ Surah stage type works")
    
    def test_tajweed_stage_type(self):
        """Test tajweed stage type (w5s1)"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w5s1?user_id={TEST_USER_ID}")
        data = response.json()
        assert data["stage"]["type"] == "tajweed"
        print(f"✓ Tajweed stage type works")
    
    def test_boss_stage_type(self):
        """Test boss stage type (w1boss)"""
        response = requests.get(f"{BASE_URL}/api/kids-zone/stage/w1boss?user_id={TEST_USER_ID}")
        data = response.json()
        assert data["stage"]["type"] == "boss"
        
        # Check boss-specific content
        boss_activity = next((a for a in data["activities"] if a["phase"] == "boss"), None)
        assert boss_activity is not None
        print(f"✓ Boss stage type works")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
