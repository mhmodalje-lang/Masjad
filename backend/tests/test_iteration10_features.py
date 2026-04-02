"""
Iteration 10 Tests: Professional TopNav, Emerald+Gold CSS Theme, Text Overflow Fixes
Tests key backend APIs that power the updated UI features.
"""
import pytest
import requests
import os
import json

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test Credentials
ADMIN_EMAIL = os.getenv('TEST_ADMIN_EMAIL', 'mhmd321324t@gmail.com')
ADMIN_PASSWORD = os.getenv('TEST_ADMIN_PASSWORD', 'admin123')


class TestHealthAndStatus:
    """Health check APIs"""
    
    def test_api_health(self):
        """Check API health endpoint"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        print("✅ Health API working")
    
    def test_api_root(self):
        """Check API root endpoint"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["status"] == "running"
        print("✅ API root working")


class TestAuthAPIs:
    """Authentication API tests"""
    
    def test_login_success(self):
        """Login with valid admin credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == ADMIN_EMAIL
        print(f"✅ Login successful for {ADMIN_EMAIL}")
    
    def test_login_invalid_password(self):
        """Login with wrong password returns 401"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        print("✅ Login correctly rejects invalid password")
    
    def test_google_auth_requires_session_id(self):
        """Google auth endpoint requires session_id"""
        response = requests.post(f"{BASE_URL}/api/auth/google", json={})
        assert response.status_code == 400
        print("✅ Google auth correctly requires session_id")
    
    def test_forgot_password_api(self):
        """Forgot password API returns success message"""
        response = requests.post(f"{BASE_URL}/api/auth/forgot-password", json={
            "email": ADMIN_EMAIL
        })
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("✅ Forgot password API working")
    
    def test_forgot_password_requires_email(self):
        """Forgot password requires email parameter"""
        response = requests.post(f"{BASE_URL}/api/auth/forgot-password", json={})
        assert response.status_code == 400
        print("✅ Forgot password correctly requires email")
    
    def test_auth_me_unauthorized(self):
        """Get me without token returns 401"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 401
        print("✅ Auth/me correctly requires authentication")


class TestSohbaAPIs:
    """Sohba social platform API tests"""
    
    def test_get_categories(self):
        """Get sohba categories"""
        response = requests.get(f"{BASE_URL}/api/sohba/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert len(data["categories"]) > 0
        # Check for expected categories
        category_keys = [c["key"] for c in data["categories"]]
        assert "general" in category_keys
        assert "quran" in category_keys
        print(f"✅ Sohba categories: {len(data['categories'])} categories found")
    
    def test_get_posts(self):
        """Get sohba posts"""
        response = requests.get(f"{BASE_URL}/api/sohba/posts?category=all")
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
        assert "total" in data
        assert "has_more" in data
        print(f"✅ Sohba posts: {data['total']} total posts")
    
    def test_get_posts_by_category(self):
        """Get sohba posts filtered by category"""
        response = requests.get(f"{BASE_URL}/api/sohba/posts?category=general")
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
        print(f"✅ Sohba posts by category: {len(data['posts'])} posts in 'general'")
    
    def test_get_post_comments(self):
        """Get comments for a post (even if empty)"""
        # First get a post
        posts_response = requests.get(f"{BASE_URL}/api/sohba/posts?category=all&limit=1")
        assert posts_response.status_code == 200
        posts_data = posts_response.json()
        
        if posts_data["posts"]:
            post_id = posts_data["posts"][0]["id"]
            response = requests.get(f"{BASE_URL}/api/sohba/posts/{post_id}/comments")
            assert response.status_code == 200
            data = response.json()
            assert "comments" in data
            print("✅ Post comments API working")
        else:
            pytest.skip("No posts available to test comments")
    
    def test_like_post_requires_auth(self):
        """Like post requires authentication"""
        response = requests.post(f"{BASE_URL}/api/sohba/posts/fake-id/like", json={})
        assert response.status_code == 401
        print("✅ Like post correctly requires auth")
    
    def test_create_post_requires_auth(self):
        """Create post requires authentication"""
        response = requests.post(f"{BASE_URL}/api/sohba/posts", json={
            "content": "Test post",
            "category": "general"
        })
        assert response.status_code == 401
        print("✅ Create post correctly requires auth")


class TestAuthenticatedSohbaAPIs:
    """Sohba APIs that require authentication"""
    
    @pytest.fixture(scope="class")
    def auth_headers(self):
        """Get auth token and headers"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        assert response.status_code == 200
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_get_my_stats(self, auth_headers):
        """Get user stats when authenticated"""
        response = requests.get(f"{BASE_URL}/api/sohba/my-stats", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
        assert "followers" in data
        assert "following" in data
        print(f"✅ My stats: posts={data['posts']}, followers={data['followers']}")
    
    def test_create_and_delete_post(self, auth_headers):
        """Create a post and then delete it"""
        # Create post
        create_response = requests.post(f"{BASE_URL}/api/sohba/posts", 
            headers=auth_headers,
            json={
                "content": "TEST_iter10 - Test post for iteration 10",
                "category": "general"
            }
        )
        assert create_response.status_code == 200
        post = create_response.json()["post"]
        post_id = post["id"]
        print(f"✅ Created test post: {post_id}")
        
        # Verify post exists in feed
        feed_response = requests.get(f"{BASE_URL}/api/sohba/posts?category=all", 
            headers=auth_headers)
        assert feed_response.status_code == 200
        
        # Delete post
        delete_response = requests.delete(f"{BASE_URL}/api/sohba/posts/{post_id}",
            headers=auth_headers)
        assert delete_response.status_code == 200
        print(f"✅ Deleted test post: {post_id}")


class TestPrayerTimesAPIs:
    """Prayer times API tests"""
    
    def test_prayer_times(self):
        """Get prayer times for Mecca"""
        response = requests.get(f"{BASE_URL}/api/prayer-times", params={
            "lat": 21.4225,
            "lon": 39.8262,
            "method": 4,
            "school": 0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "times" in data
        times = data["times"]
        assert "fajr" in times
        assert "dhuhr" in times
        assert "asr" in times
        assert "maghrib" in times
        assert "isha" in times
        print(f"✅ Prayer times: Fajr={times['fajr']}, Maghrib={times['maghrib']}")
    
    def test_hijri_date(self):
        """Get hijri date"""
        response = requests.get(f"{BASE_URL}/api/hijri-date", params={
            "lat": 21.4225,
            "lon": 39.8262
        })
        assert response.status_code == 200
        data = response.json()
        assert "hijriDate" in data
        print(f"✅ Hijri date: {data['hijriDate']}")
    
    def test_daily_hadith(self):
        """Get daily hadith"""
        response = requests.get(f"{BASE_URL}/api/daily-hadith")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "hadith" in data
        hadith = data["hadith"]
        assert "text" in hadith
        assert "narrator" in hadith
        assert "source" in hadith
        print(f"✅ Daily hadith loaded (from {hadith['source']})")


class TestMosqueAPIs:
    """Mosque search API tests"""
    
    def test_mosque_search(self):
        """Search mosques near Mecca"""
        response = requests.get(f"{BASE_URL}/api/mosques/search", params={
            "lat": 21.4225,
            "lon": 39.8262,
            "radius": 5000
        })
        assert response.status_code == 200
        data = response.json()
        assert "mosques" in data
        assert "count" in data
        print(f"✅ Mosque search: {data['count']} mosques found")


class TestAdminAPIs:
    """Admin API tests (require admin authentication)"""
    
    @pytest.fixture(scope="class")
    def admin_headers(self):
        """Get admin auth token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        assert response.status_code == 200
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_admin_stats(self, admin_headers):
        """Get admin dashboard stats"""
        response = requests.get(f"{BASE_URL}/api/admin/stats", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "stats" in data
        stats = data["stats"]
        assert "total_users" in stats
        print(f"✅ Admin stats: {stats['total_users']} total users")
    
    def test_admin_settings(self, admin_headers):
        """Get admin settings"""
        response = requests.get(f"{BASE_URL}/api/admin/settings", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "app_name" in data or "key" in data
        print("✅ Admin settings loaded")


class TestUIIntegrationPoints:
    """Test APIs that support the UI features"""
    
    def test_sohba_posts_have_required_fields(self):
        """Verify sohba posts have all fields needed for UI"""
        response = requests.get(f"{BASE_URL}/api/sohba/posts?category=all&limit=5")
        assert response.status_code == 200
        data = response.json()
        
        if data["posts"]:
            post = data["posts"][0]
            # Check required fields for grid card
            required_fields = ["id", "author_id", "author_name", "content", "category", 
                            "created_at", "likes_count", "comments_count", "liked", "saved"]
            for field in required_fields:
                assert field in post, f"Missing field: {field}"
            print("✅ Sohba posts have all required UI fields")
        else:
            print("⚠️ No posts to verify fields")
    
    def test_categories_have_labels(self):
        """Verify categories have labels for UI tabs"""
        response = requests.get(f"{BASE_URL}/api/sohba/categories")
        assert response.status_code == 200
        data = response.json()
        
        for cat in data["categories"]:
            assert "key" in cat
            assert "label" in cat
            # Labels should be Arabic text
            assert len(cat["label"]) > 0
        print("✅ All categories have labels for UI tabs")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
