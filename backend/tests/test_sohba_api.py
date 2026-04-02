"""
Social Platform (Sohba) API Tests
Tests for posts CRUD, likes, comments, saves, follows, categories
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test credentials
ADMIN_EMAIL = os.getenv('TEST_ADMIN_EMAIL', 'mhmd321324t@gmail.com')
ADMIN_PASSWORD = os.getenv('TEST_ADMIN_PASSWORD', 'admin123')

@pytest.fixture(scope="module")
def api_client():
    """Shared requests session"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session

@pytest.fixture(scope="module")
def auth_token(api_client):
    """Get authentication token for admin user"""
    response = api_client.post(f"{BASE_URL}/api/auth/login", json={
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })
    if response.status_code == 200:
        return response.json().get("access_token")
    pytest.skip("Authentication failed - skipping authenticated tests")

@pytest.fixture(scope="module")
def authenticated_client(api_client, auth_token):
    """Session with auth header"""
    api_client.headers.update({"Authorization": f"Bearer {auth_token}"})
    return api_client


class TestHealth:
    """Health check endpoint tests"""
    
    def test_health_endpoint(self, api_client):
        """GET /api/health returns healthy status"""
        response = api_client.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health endpoint working")


class TestAuth:
    """Authentication endpoint tests"""
    
    def test_login_success(self, api_client):
        """POST /api/auth/login with valid credentials returns token"""
        response = api_client.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == ADMIN_EMAIL
        print(f"✅ Login successful for {ADMIN_EMAIL}")
    
    def test_login_invalid_credentials(self, api_client):
        """POST /api/auth/login with invalid credentials returns 401"""
        response = api_client.post(f"{BASE_URL}/api/auth/login", json={
            "email": "wrong@example.com",
            "password": "wrongpass"
        })
        assert response.status_code == 401
        print("✅ Invalid login properly rejected with 401")
    
    def test_get_me_authenticated(self, authenticated_client):
        """GET /api/auth/me returns user info when authenticated"""
        response = authenticated_client.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert data["email"] == ADMIN_EMAIL
        print(f"✅ /api/auth/me returns user: {data['email']}")


class TestSohbaCategories:
    """Sohba categories endpoint tests"""
    
    def test_get_categories(self, api_client):
        """GET /api/sohba/categories returns 10 categories"""
        response = api_client.get(f"{BASE_URL}/api/sohba/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert len(data["categories"]) == 10
        
        # Verify expected categories
        category_keys = [c["key"] for c in data["categories"]]
        expected = ["general", "quran", "hadith", "ramadan", "dua", "stories", "hajj", "halal", "family", "youth"]
        for key in expected:
            assert key in category_keys, f"Missing category: {key}"
        print(f"✅ Categories endpoint returns 10 categories: {category_keys}")


class TestSohbaPosts:
    """Sohba posts CRUD tests"""
    
    def test_get_posts_public(self, api_client):
        """GET /api/sohba/posts returns posts list (no auth required)"""
        response = api_client.get(f"{BASE_URL}/api/sohba/posts")
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
        assert "total" in data
        assert isinstance(data["posts"], list)
        print(f"✅ GET posts returns {len(data['posts'])} posts, total: {data['total']}")
    
    def test_get_posts_by_category(self, api_client):
        """GET /api/sohba/posts?category=quran filters by category"""
        response = api_client.get(f"{BASE_URL}/api/sohba/posts?category=quran")
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
        for post in data["posts"]:
            assert post["category"] == "quran", f"Post category mismatch: {post['category']}"
        print(f"✅ Category filter works - {len(data['posts'])} quran posts")
    
    def test_create_post_requires_auth(self, api_client):
        """POST /api/sohba/posts without auth returns 401"""
        # Remove auth header for this test
        clean_client = requests.Session()
        clean_client.headers.update({"Content-Type": "application/json"})
        response = clean_client.post(f"{BASE_URL}/api/sohba/posts", json={
            "content": "Test post without auth",
            "category": "general"
        })
        assert response.status_code == 401
        print("✅ Create post without auth properly rejected with 401")
    
    def test_create_post_authenticated(self, authenticated_client):
        """POST /api/sohba/posts creates a new post (requires auth)"""
        unique_content = f"TEST_post_{uuid.uuid4().hex[:8]} - تجربة منشور جديد"
        response = authenticated_client.post(f"{BASE_URL}/api/sohba/posts", json={
            "content": unique_content,
            "category": "general"
        })
        assert response.status_code == 200
        data = response.json()
        assert "post" in data
        assert data["post"]["content"] == unique_content
        assert data["post"]["category"] == "general"
        assert "id" in data["post"]
        
        post_id = data["post"]["id"]
        print(f"✅ Created post with ID: {post_id}")
        
        # Verify post exists in GET
        get_response = authenticated_client.get(f"{BASE_URL}/api/sohba/posts")
        posts = get_response.json()["posts"]
        post_ids = [p["id"] for p in posts]
        assert post_id in post_ids, "Created post not found in posts list"
        print(f"✅ Verified post {post_id} exists in posts list")


class TestSohbaInteractions:
    """Tests for like, save, comment, follow"""
    
    @pytest.fixture
    def test_post_id(self, api_client):
        """Get an existing post ID for testing interactions"""
        response = api_client.get(f"{BASE_URL}/api/sohba/posts")
        posts = response.json().get("posts", [])
        if not posts:
            pytest.skip("No posts available for interaction tests")
        return posts[0]["id"]
    
    def test_toggle_like_requires_auth(self, api_client, test_post_id):
        """POST /api/sohba/posts/{id}/like without auth returns 401"""
        clean_client = requests.Session()
        clean_client.headers.update({"Content-Type": "application/json"})
        response = clean_client.post(f"{BASE_URL}/api/sohba/posts/{test_post_id}/like")
        assert response.status_code == 401
        print("✅ Like without auth properly rejected with 401")
    
    def test_toggle_like_authenticated(self, authenticated_client, test_post_id):
        """POST /api/sohba/posts/{id}/like toggles like status"""
        # First like
        response = authenticated_client.post(f"{BASE_URL}/api/sohba/posts/{test_post_id}/like")
        assert response.status_code == 200
        data = response.json()
        assert "liked" in data
        first_state = data["liked"]
        print(f"✅ Toggle like - state: {first_state}")
        
        # Toggle again
        response2 = authenticated_client.post(f"{BASE_URL}/api/sohba/posts/{test_post_id}/like")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["liked"] != first_state, "Like state should toggle"
        print(f"✅ Toggle like again - state: {data2['liked']} (toggled correctly)")
    
    def test_toggle_save_requires_auth(self, api_client, test_post_id):
        """POST /api/sohba/posts/{id}/save without auth returns 401"""
        clean_client = requests.Session()
        clean_client.headers.update({"Content-Type": "application/json"})
        response = clean_client.post(f"{BASE_URL}/api/sohba/posts/{test_post_id}/save")
        assert response.status_code == 401
        print("✅ Save without auth properly rejected with 401")
    
    def test_toggle_save_authenticated(self, authenticated_client, test_post_id):
        """POST /api/sohba/posts/{id}/save toggles save status"""
        response = authenticated_client.post(f"{BASE_URL}/api/sohba/posts/{test_post_id}/save")
        assert response.status_code == 200
        data = response.json()
        assert "saved" in data
        print(f"✅ Toggle save - state: {data['saved']}")
    
    def test_get_comments(self, api_client, test_post_id):
        """GET /api/sohba/posts/{id}/comments returns comments list"""
        response = api_client.get(f"{BASE_URL}/api/sohba/posts/{test_post_id}/comments")
        assert response.status_code == 200
        data = response.json()
        assert "comments" in data
        assert isinstance(data["comments"], list)
        print(f"✅ GET comments returns {len(data['comments'])} comments")
    
    def test_create_comment_requires_auth(self, api_client, test_post_id):
        """POST /api/sohba/posts/{id}/comments without auth returns 401"""
        clean_client = requests.Session()
        clean_client.headers.update({"Content-Type": "application/json"})
        response = clean_client.post(f"{BASE_URL}/api/sohba/posts/{test_post_id}/comments", json={
            "content": "Test comment without auth"
        })
        assert response.status_code == 401
        print("✅ Create comment without auth properly rejected with 401")
    
    def test_create_comment_authenticated(self, authenticated_client, test_post_id):
        """POST /api/sohba/posts/{id}/comments creates a comment"""
        comment_text = f"TEST_comment_{uuid.uuid4().hex[:8]} - تعليق تجريبي"
        response = authenticated_client.post(f"{BASE_URL}/api/sohba/posts/{test_post_id}/comments", json={
            "content": comment_text
        })
        assert response.status_code == 200
        data = response.json()
        assert "comment" in data
        assert data["comment"]["content"] == comment_text
        assert "id" in data["comment"]
        print(f"✅ Created comment: {data['comment']['id']}")
        
        # Verify comment exists in GET
        get_response = authenticated_client.get(f"{BASE_URL}/api/sohba/posts/{test_post_id}/comments")
        comments = get_response.json()["comments"]
        comment_ids = [c["id"] for c in comments]
        assert data["comment"]["id"] in comment_ids
        print(f"✅ Verified comment exists in comments list")


class TestSohbaMyStats:
    """Tests for my-stats endpoint"""
    
    def test_my_stats_requires_auth(self, api_client):
        """GET /api/sohba/my-stats without auth returns 401"""
        clean_client = requests.Session()
        clean_client.headers.update({"Content-Type": "application/json"})
        response = clean_client.get(f"{BASE_URL}/api/sohba/my-stats")
        assert response.status_code == 401
        print("✅ my-stats without auth properly rejected with 401")
    
    def test_my_stats_authenticated(self, authenticated_client):
        """GET /api/sohba/my-stats returns user stats"""
        response = authenticated_client.get(f"{BASE_URL}/api/sohba/my-stats")
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
        assert "followers" in data
        assert "following" in data
        print(f"✅ my-stats: posts={data['posts']}, followers={data['followers']}, following={data['following']}")


class TestSohbaFollow:
    """Tests for follow system"""
    
    @pytest.fixture
    def other_user_id(self):
        """Get or create another user for follow tests"""
        # Use a placeholder UUID since we can't easily create another user
        return "00000000-0000-0000-0000-000000000001"
    
    def test_follow_requires_auth(self, api_client, other_user_id):
        """POST /api/sohba/follow/{id} without auth returns 401"""
        clean_client = requests.Session()
        clean_client.headers.update({"Content-Type": "application/json"})
        response = clean_client.post(f"{BASE_URL}/api/sohba/follow/{other_user_id}")
        assert response.status_code == 401
        print("✅ Follow without auth properly rejected with 401")
    
    def test_cannot_follow_self(self, authenticated_client):
        """POST /api/sohba/follow/{self} returns 400"""
        # Get own user ID from /auth/me
        me_response = authenticated_client.get(f"{BASE_URL}/api/auth/me")
        my_id = me_response.json()["id"]
        
        response = authenticated_client.post(f"{BASE_URL}/api/sohba/follow/{my_id}")
        assert response.status_code == 400
        print("✅ Cannot follow self - properly rejected with 400")


class TestSohbaDeletePost:
    """Tests for post deletion"""
    
    def test_delete_own_post(self, authenticated_client):
        """DELETE /api/sohba/posts/{id} deletes own post"""
        # Create a post to delete
        create_response = authenticated_client.post(f"{BASE_URL}/api/sohba/posts", json={
            "content": f"TEST_delete_{uuid.uuid4().hex[:8]} - منشور للحذف",
            "category": "general"
        })
        post_id = create_response.json()["post"]["id"]
        print(f"Created post {post_id} for deletion test")
        
        # Delete the post
        delete_response = authenticated_client.delete(f"{BASE_URL}/api/sohba/posts/{post_id}")
        assert delete_response.status_code == 200
        data = delete_response.json()
        assert data.get("deleted") == True
        print(f"✅ Deleted post {post_id}")
        
        # Verify post no longer exists
        get_response = authenticated_client.get(f"{BASE_URL}/api/sohba/posts")
        post_ids = [p["id"] for p in get_response.json()["posts"]]
        assert post_id not in post_ids, "Deleted post should not appear in posts list"
        print(f"✅ Verified post {post_id} no longer exists")
    
    def test_delete_nonexistent_post(self, authenticated_client):
        """DELETE /api/sohba/posts/{invalid_id} returns 404"""
        fake_id = str(uuid.uuid4())
        response = authenticated_client.delete(f"{BASE_URL}/api/sohba/posts/{fake_id}")
        assert response.status_code == 404
        print("✅ Delete nonexistent post properly returns 404")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
