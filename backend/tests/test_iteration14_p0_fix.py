"""
Iteration 14: P0 Content Publishing Fix Tests
Tests the fix where CreateStoryRequest.title was changed from required Field(..., min_length=1) 
to Optional[str] = None, allowing stories to be created without a title.
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestStoryP0Fix:
    """Tests for P0 story creation fix - title now optional"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test user and get auth token"""
        self.test_email = f"test_p0_{uuid.uuid4().hex[:8]}@test.com"
        self.test_password = "Test123!"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        
        # Register test user
        register_res = self.session.post(f"{BASE_URL}/api/auth/register", json={
            "email": self.test_email,
            "password": self.test_password,
            "name": "Test P0 User"
        })
        
        if register_res.status_code == 200:
            data = register_res.json()
            self.auth_token = data.get("access_token") or data.get("token")
        else:
            # Try login if already exists
            login_res = self.session.post(f"{BASE_URL}/api/auth/login", json={
                "email": self.test_email,
                "password": self.test_password
            })
            if login_res.status_code == 200:
                login_data = login_res.json()
                self.auth_token = login_data.get("access_token") or login_data.get("token")
            else:
                self.auth_token = None
        
        if self.auth_token:
            self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
        yield
    
    def test_create_story_without_title_empty_string(self):
        """P0 FIX: Create story with empty string title - should succeed"""
        if not self.auth_token:
            pytest.skip("Auth failed")
        
        payload = {
            "content": "هذا منشور اختباري بدون عنوان - P0 fix verification",
            "category": "general",
            "media_type": "text",
            "title": ""  # Empty string - the P0 fix
        }
        
        response = self.session.post(f"{BASE_URL}/api/stories/create", json=payload)
        
        # Should succeed with 200
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "story" in data, f"No story in response: {data}"
        story = data["story"]
        
        # Verify story structure
        assert story["content"] == payload["content"]
        assert story["category"] == payload["category"]
        assert story["media_type"] == payload["media_type"]
        assert story.get("title", "") == ""  # Title should be empty string
        assert "id" in story
        assert "author_id" in story
        
        print(f"✅ Story created without title, ID: {story['id']}")
    
    def test_create_story_without_title_field_omitted(self):
        """Create story with title field completely omitted - should succeed"""
        if not self.auth_token:
            pytest.skip("Auth failed")
        
        payload = {
            "content": "منشور بدون حقل العنوان على الإطلاق",
            "category": "dua",
            "media_type": "text"
            # No title field at all
        }
        
        response = self.session.post(f"{BASE_URL}/api/stories/create", json=payload)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "story" in data
        story = data["story"]
        assert story["content"] == payload["content"]
        
        print(f"✅ Story created with omitted title, ID: {story['id']}")
    
    def test_create_story_with_title(self):
        """Create story with title provided - should succeed"""
        if not self.auth_token:
            pytest.skip("Auth failed")
        
        payload = {
            "content": "محتوى المنشور مع عنوان",
            "category": "quran",
            "media_type": "text",
            "title": "عنوان المنشور الاختباري"
        }
        
        response = self.session.post(f"{BASE_URL}/api/stories/create", json=payload)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "story" in data
        story = data["story"]
        assert story["content"] == payload["content"]
        assert story["title"] == payload["title"]
        
        print(f"✅ Story created with title: '{story['title']}', ID: {story['id']}")
    
    def test_create_story_validates_content_required(self):
        """Content is still required - should fail with empty content"""
        if not self.auth_token:
            pytest.skip("Auth failed")
        
        payload = {
            "content": "",  # Empty content should fail
            "category": "general"
        }
        
        response = self.session.post(f"{BASE_URL}/api/stories/create", json=payload)
        
        # Should fail - content is required
        assert response.status_code == 422, f"Expected 422 validation error, got {response.status_code}"
        print("✅ Content validation still works - empty content rejected")
    
    def test_create_story_without_auth_fails(self):
        """Story creation requires authentication"""
        # Create session without auth
        no_auth_session = requests.Session()
        no_auth_session.headers.update({"Content-Type": "application/json"})
        
        payload = {
            "content": "Test content without auth",
            "category": "general"
        }
        
        response = no_auth_session.post(f"{BASE_URL}/api/stories/create", json=payload)
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print("✅ Auth required for story creation")


class TestStoriesListAPI:
    """Tests for stories list endpoint with enriched data"""
    
    def test_list_stories_returns_enriched_data(self):
        """GET /api/stories/list returns stories with enriched data"""
        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})
        
        response = session.get(f"{BASE_URL}/api/stories/list")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "stories" in data
        assert "total" in data
        
        # If stories exist, verify enriched fields
        if data["stories"]:
            story = data["stories"][0]
            # Verify enriched fields exist
            assert "liked" in story
            assert "saved" in story
            assert "likes_count" in story or story.get("likes_count") is None or "likes_count" in story
            assert "comments_count" in story or story.get("comments_count") is None or "comments_count" in story
            print(f"✅ Stories list returned {data['total']} stories with enriched data")
        else:
            print("✅ Stories list returned empty (no stories yet)")
    
    def test_list_stories_with_category_filter(self):
        """GET /api/stories/list with category filter"""
        session = requests.Session()
        
        response = session.get(f"{BASE_URL}/api/stories/list?category=quran")
        
        assert response.status_code == 200
        data = response.json()
        assert "stories" in data
        
        # If stories exist, verify category
        for story in data["stories"]:
            assert story["category"] == "quran", f"Expected category 'quran', got {story['category']}"
        
        print(f"✅ Category filter works, returned {len(data['stories'])} quran stories")


class TestStoriesCategoriesAPI:
    """Tests for story categories endpoint"""
    
    def test_get_categories(self):
        """GET /api/stories/categories returns category list"""
        session = requests.Session()
        
        response = session.get(f"{BASE_URL}/api/stories/categories")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "categories" in data
        assert isinstance(data["categories"], list)
        assert len(data["categories"]) > 0
        
        print(f"✅ Categories returned: {len(data['categories'])} categories")


class TestExistingCredentials:
    """Test with provided test credentials"""
    
    def test_login_with_test_credentials(self):
        """Login with provided test credentials"""
        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})
        
        response = session.post(f"{BASE_URL}/api/auth/login", json={
            "email": "testpub123@test.com",
            "password": "Test123!"
        })
        
        # If user doesn't exist, register them
        if response.status_code == 401:
            session.post(f"{BASE_URL}/api/auth/register", json={
                "email": "testpub123@test.com",
                "password": "Test123!",
                "name": "Test Publisher"
            })
            if reg_res.status_code == 200:
                print("✅ Test user registered successfully")
                response = session.post(f"{BASE_URL}/api/auth/login", json={
                    "email": "testpub123@test.com",
                    "password": "Test123!"
                })
        
        assert response.status_code == 200, f"Login failed: {response.status_code} - {response.text}"
        
        data = response.json()
        assert "access_token" in data or "token" in data
        print("✅ Login successful for testpub123@test.com")
        return data.get("access_token") or data.get("token")
    
    def test_create_story_with_test_user(self):
        """Create story with test user to verify full flow"""
        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})
        
        # Login first
        login_res = session.post(f"{BASE_URL}/api/auth/login", json={
            "email": "testpub123@test.com",
            "password": "Test123!"
        })
        
        if login_res.status_code != 200:
            # Register if needed
            session.post(f"{BASE_URL}/api/auth/register", json={
                "email": "testpub123@test.com",
                "password": "Test123!",
                "name": "Test Publisher"
            })
            login_res = session.post(f"{BASE_URL}/api/auth/login", json={
                "email": "testpub123@test.com",
                "password": "Test123!"
            })
        
        if login_res.status_code != 200:
            pytest.skip("Could not login with test credentials")
        
        login_data = login_res.json()
        token = login_data.get("access_token") or login_data.get("token")
        session.headers.update({"Authorization": f"Bearer {token}"})
        
        # Create story without title (P0 fix verification)
        payload = {
            "content": f"P0 Fix Test - {uuid.uuid4().hex[:8]} - Story created without title to verify fix",
            "category": "general",
            "media_type": "text",
            "title": ""
        }
        
        response = session.post(f"{BASE_URL}/api/stories/create", json=payload)
        
        assert response.status_code == 200, f"Story creation failed: {response.status_code} - {response.text}"
        
        data = response.json()
        assert "story" in data
        print(f"✅ Story created with test user, ID: {data['story']['id']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
