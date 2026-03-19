"""
Iteration 9 Backend API Tests
Tests for:
1. Google Auth (Emergent OAuth) - session_id validation
2. Forgot Password endpoint
3. Email/Password login (existing feature)
4. Sohba posts API (existing feature verification)
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
if not BASE_URL:
    BASE_URL = "https://islamic-social-hub.preview.emergentagent.com"

# Test credentials
ADMIN_EMAIL = "mhmd321324t@gmail.com"
ADMIN_PASSWORD = "admin123"


class TestHealthAndBasics:
    """Basic API health tests"""
    
    def test_health_endpoint(self):
        """Test API health endpoint"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health endpoint working")
    
    def test_root_endpoint(self):
        """Test API root endpoint"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "المؤذن العالمي" in data.get("message", "")
        print("✅ Root endpoint working")


class TestForgotPassword:
    """Forgot password endpoint tests"""
    
    def test_forgot_password_with_email(self):
        """Test forgot password returns success message"""
        response = requests.post(
            f"{BASE_URL}/api/auth/forgot-password",
            json={"email": "test@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        # Should return a message (doesn't reveal if email exists)
        assert "message" in data
        assert "إذا كان البريد مسجلاً" in data["message"]
        print("✅ Forgot password returns success message")
    
    def test_forgot_password_without_email(self):
        """Test forgot password requires email"""
        response = requests.post(
            f"{BASE_URL}/api/auth/forgot-password",
            json={}
        )
        assert response.status_code == 400
        print("✅ Forgot password validates email requirement")
    
    def test_forgot_password_with_existing_email(self):
        """Test forgot password with existing admin email"""
        response = requests.post(
            f"{BASE_URL}/api/auth/forgot-password",
            json={"email": ADMIN_EMAIL}
        )
        assert response.status_code == 200
        data = response.json()
        # Should return same message to not reveal email existence
        assert "message" in data
        print("✅ Forgot password handles existing email correctly")


class TestGoogleAuth:
    """Google Auth (Emergent OAuth) endpoint tests"""
    
    def test_google_auth_requires_session_id(self):
        """Test POST /api/auth/google requires session_id"""
        response = requests.post(
            f"{BASE_URL}/api/auth/google",
            json={}
        )
        assert response.status_code == 400
        data = response.json()
        assert "session_id" in data.get("detail", "")
        print("✅ Google auth requires session_id")
    
    def test_google_auth_rejects_invalid_session(self):
        """Test POST /api/auth/google rejects invalid session_id"""
        response = requests.post(
            f"{BASE_URL}/api/auth/google",
            json={"session_id": "invalid-session-id-12345"}
        )
        # Should fail with 401 for invalid session
        assert response.status_code in [401, 400]
        print("✅ Google auth rejects invalid session_id")


class TestEmailPasswordLogin:
    """Email/Password authentication tests"""
    
    def test_login_with_valid_credentials(self):
        """Test login with valid admin credentials"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == ADMIN_EMAIL
        print(f"✅ Login successful for {ADMIN_EMAIL}")
        return data["access_token"]
    
    def test_login_with_invalid_credentials(self):
        """Test login with wrong password"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": "wrongpassword"}
        )
        assert response.status_code == 401
        print("✅ Login rejects invalid credentials")
    
    def test_login_with_nonexistent_email(self):
        """Test login with non-existent email"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": f"nonexistent{uuid.uuid4().hex[:6]}@test.com", "password": "anypassword"}
        )
        assert response.status_code == 401
        print("✅ Login rejects non-existent email")
    
    def test_get_user_profile_with_token(self):
        """Test GET /api/auth/me with valid token"""
        # First login
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        )
        token = login_response.json()["access_token"]
        
        # Get profile
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == ADMIN_EMAIL
        print("✅ User profile retrieval works with token")
    
    def test_get_user_profile_without_token(self):
        """Test GET /api/auth/me without token"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 401
        print("✅ User profile requires authentication")


class TestSohbaAPI:
    """Sohba social platform API tests"""
    
    def test_get_categories(self):
        """Test GET /api/sohba/categories returns category list"""
        response = requests.get(f"{BASE_URL}/api/sohba/categories")
        assert response.status_code == 200
        data = response.json()
        
        assert "categories" in data
        categories = data["categories"]
        assert len(categories) >= 5  # Should have multiple categories
        
        # Check category structure
        category_keys = [c["key"] for c in categories]
        assert "general" in category_keys
        assert "quran" in category_keys
        print(f"✅ Categories endpoint returns {len(categories)} categories")
    
    def test_get_posts_no_auth(self):
        """Test GET /api/sohba/posts without auth"""
        response = requests.get(f"{BASE_URL}/api/sohba/posts")
        assert response.status_code == 200
        data = response.json()
        
        assert "posts" in data
        assert "total" in data
        assert "page" in data
        print(f"✅ Posts endpoint returns {len(data['posts'])} posts")
    
    def test_get_posts_with_category_filter(self):
        """Test GET /api/sohba/posts with category filter"""
        response = requests.get(f"{BASE_URL}/api/sohba/posts?category=all")
        assert response.status_code == 200
        
        response2 = requests.get(f"{BASE_URL}/api/sohba/posts?category=quran")
        assert response2.status_code == 200
        print("✅ Posts endpoint filters by category")
    
    def test_create_post_requires_auth(self):
        """Test POST /api/sohba/posts requires authentication"""
        response = requests.post(
            f"{BASE_URL}/api/sohba/posts",
            json={"content": "Test post", "category": "general"}
        )
        assert response.status_code == 401
        print("✅ Create post requires authentication")
    
    def test_create_post_with_auth(self):
        """Test POST /api/sohba/posts creates post with valid auth"""
        # Login first
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        )
        token = login_response.json()["access_token"]
        
        test_id = uuid.uuid4().hex[:8]
        response = requests.post(
            f"{BASE_URL}/api/sohba/posts",
            headers={"Authorization": f"Bearer {token}"},
            json={"content": f"TEST_iter9_{test_id}", "category": "general"}
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "post" in data
        assert data["post"]["content"] == f"TEST_iter9_{test_id}"
        print("✅ Create post works with authentication")
        
        # Cleanup - delete the post
        post_id = data["post"]["id"]
        delete_response = requests.delete(
            f"{BASE_URL}/api/sohba/posts/{post_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert delete_response.status_code == 200
        print("✅ Test post cleaned up")


class TestSohbaInteractions:
    """Sohba post interaction tests (like, save, comment)"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        )
        return response.json()["access_token"]
    
    def test_like_requires_auth(self):
        """Test POST /api/sohba/posts/{id}/like requires auth"""
        response = requests.post(f"{BASE_URL}/api/sohba/posts/fake-id/like")
        assert response.status_code == 401
        print("✅ Like requires authentication")
    
    def test_save_requires_auth(self):
        """Test POST /api/sohba/posts/{id}/save requires auth"""
        response = requests.post(f"{BASE_URL}/api/sohba/posts/fake-id/save")
        assert response.status_code == 401
        print("✅ Save requires authentication")
    
    def test_comment_requires_auth(self):
        """Test POST /api/sohba/posts/{id}/comments requires auth"""
        response = requests.post(
            f"{BASE_URL}/api/sohba/posts/fake-id/comments",
            json={"content": "Test comment"}
        )
        assert response.status_code == 401
        print("✅ Comment requires authentication")
    
    def test_get_comments_public(self):
        """Test GET /api/sohba/posts/{id}/comments is public"""
        # Get a real post first
        posts_response = requests.get(f"{BASE_URL}/api/sohba/posts?limit=1")
        posts = posts_response.json().get("posts", [])
        
        if len(posts) > 0:
            post_id = posts[0]["id"]
            response = requests.get(f"{BASE_URL}/api/sohba/posts/{post_id}/comments")
            assert response.status_code == 200
            print("✅ Get comments is public")
        else:
            pytest.skip("No posts available for comment test")
    
    def test_my_stats_requires_auth(self):
        """Test GET /api/sohba/my-stats requires auth"""
        response = requests.get(f"{BASE_URL}/api/sohba/my-stats")
        assert response.status_code == 401
        print("✅ My stats requires authentication")
    
    def test_my_stats_with_auth(self, auth_token):
        """Test GET /api/sohba/my-stats with auth"""
        response = requests.get(
            f"{BASE_URL}/api/sohba/my-stats",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
        assert "followers" in data
        assert "following" in data
        print("✅ My stats works with authentication")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
