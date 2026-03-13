"""
Iteration 11 Tests: New Features Testing
- Store Items API (6 items)
- Rewards Balance API (401 without auth)
- Rewards Claim API (daily_login with auth)
- File Upload API (base64 data + auth)
- Auth Register + Login
- Membership Status API
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test user credentials
TEST_EMAIL = f"test_iter11_{uuid.uuid4().hex[:8]}@test.com"
TEST_PASSWORD = "TestPass123!"
TEST_TOKEN = None


class TestHealthAndBasics:
    """Basic health and status checks"""

    def test_health_endpoint(self):
        """1. Health check should return status healthy"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        print("✅ Health endpoint OK")

    def test_root_endpoint(self):
        """2. Root API endpoint returns version info"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        print("✅ Root endpoint OK")


class TestStoreAPI:
    """Store Items API Tests - Should return 6 store items"""

    def test_get_store_items(self):
        """3. GET /api/store/items should return 6 items"""
        response = requests.get(f"{BASE_URL}/api/store/items")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        items = data["items"]
        assert len(items) == 6, f"Expected 6 store items, got {len(items)}"
        
        # Verify item structure
        required_fields = ["id", "name", "description", "price_gold", "category"]
        for item in items:
            for field in required_fields:
                assert field in item, f"Missing field {field} in store item"
        
        # Verify categories exist
        categories = set(item["category"] for item in items)
        expected_categories = {"frame", "theme", "badge", "effect", "membership", "charity"}
        assert categories == expected_categories, f"Expected categories {expected_categories}, got {categories}"
        print(f"✅ Store items: {len(items)} items with categories {categories}")

    def test_store_items_filter_by_category(self):
        """4. GET /api/store/items with category filter"""
        response = requests.get(f"{BASE_URL}/api/store/items?category=theme")
        assert response.status_code == 200
        data = response.json()
        items = data.get("items", [])
        # When filtering by theme, should get only theme items
        for item in items:
            assert item["category"] == "theme"
        print(f"✅ Store filter by category works: {len(items)} theme items")


class TestRewardsAPIUnauthorized:
    """Rewards API Tests - Should return 401 without auth"""

    def test_rewards_balance_unauthorized(self):
        """5. GET /api/rewards/balance should return 401 without auth"""
        response = requests.get(f"{BASE_URL}/api/rewards/balance")
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print("✅ Rewards balance returns 401 without auth")

    def test_rewards_claim_unauthorized(self):
        """6. POST /api/rewards/claim should return 401 without auth"""
        response = requests.post(
            f"{BASE_URL}/api/rewards/claim",
            json={"reward_type": "daily_login"}
        )
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print("✅ Rewards claim returns 401 without auth")

    def test_rewards_history_unauthorized(self):
        """7. GET /api/rewards/history should return 401 without auth"""
        response = requests.get(f"{BASE_URL}/api/rewards/history")
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print("✅ Rewards history returns 401 without auth")


class TestAuthRegisterLogin:
    """Auth Register and Login Tests"""

    def test_register_new_user(self):
        """8. POST /api/auth/register creates new user"""
        global TEST_TOKEN
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD, "name": "Test User 11"}
        )
        assert response.status_code == 200, f"Register failed: {response.text}"
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == TEST_EMAIL.lower()
        TEST_TOKEN = data["access_token"]
        print(f"✅ User registered: {TEST_EMAIL}")

    def test_login_existing_user(self):
        """9. POST /api/auth/login with valid credentials"""
        global TEST_TOKEN
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        TEST_TOKEN = data["access_token"]
        print(f"✅ User logged in: {TEST_EMAIL}")

    def test_login_invalid_credentials(self):
        """10. POST /api/auth/login with invalid credentials returns 401"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": "nonexistent@test.com", "password": "wrongpass"}
        )
        assert response.status_code == 401
        print("✅ Invalid login returns 401")


class TestRewardsAPIAuthorized:
    """Rewards API Tests with authentication"""

    @pytest.fixture(autouse=True)
    def ensure_token(self):
        """Ensure we have a valid token before running tests"""
        global TEST_TOKEN
        if not TEST_TOKEN:
            # Register/login to get token
            response = requests.post(
                f"{BASE_URL}/api/auth/register",
                json={"email": TEST_EMAIL, "password": TEST_PASSWORD, "name": "Test User 11"}
            )
            if response.status_code == 400:  # Already exists
                response = requests.post(
                    f"{BASE_URL}/api/auth/login",
                    json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
                )
            if response.status_code == 200:
                TEST_TOKEN = response.json().get("access_token")

    def test_rewards_balance_authorized(self):
        """11. GET /api/rewards/balance with auth returns balance"""
        global TEST_TOKEN
        if not TEST_TOKEN:
            pytest.skip("No auth token available")
        
        response = requests.get(
            f"{BASE_URL}/api/rewards/balance",
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        assert "gold" in data
        assert "total_earned" in data
        assert "streak" in data
        print(f"✅ Rewards balance: gold={data['gold']}, streak={data['streak']}")

    def test_claim_daily_login_reward(self):
        """12. POST /api/rewards/claim with daily_login reward"""
        global TEST_TOKEN
        if not TEST_TOKEN:
            pytest.skip("No auth token available")
        
        response = requests.post(
            f"{BASE_URL}/api/rewards/claim",
            json={"reward_type": "daily_login"},
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        assert "gold" in data
        assert "message" in data
        # Either earned gold or already claimed today
        print(f"✅ Daily login claim: {data['message']}")

    def test_claim_invalid_reward_type(self):
        """13. POST /api/rewards/claim with invalid reward type returns 400"""
        global TEST_TOKEN
        if not TEST_TOKEN:
            pytest.skip("No auth token available")
        
        response = requests.post(
            f"{BASE_URL}/api/rewards/claim",
            json={"reward_type": "invalid_type"},
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )
        assert response.status_code == 400
        print("✅ Invalid reward type returns 400")


class TestFileUploadAPI:
    """File Upload API Tests"""

    def test_file_upload_unauthorized(self):
        """14. POST /api/upload/file returns 401 without auth"""
        response = requests.post(
            f"{BASE_URL}/api/upload/file",
            json={"data": "base64data", "filename": "test.jpg"}
        )
        assert response.status_code == 401
        print("✅ File upload returns 401 without auth")

    def test_file_upload_with_base64(self):
        """15. POST /api/upload/file with base64 image data"""
        global TEST_TOKEN
        if not TEST_TOKEN:
            pytest.skip("No auth token available")
        
        # Small base64 encoded 1x1 red PNG
        base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="
        
        response = requests.post(
            f"{BASE_URL}/api/upload/file",
            json={"data": base64_image, "filename": "test_iter11.png"},
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        assert "url" in data
        assert "filename" in data
        assert data["url"].startswith("/api/uploads/")
        print(f"✅ File uploaded: {data['url']}")

    def test_file_upload_empty_data(self):
        """16. POST /api/upload/file with empty data returns 400"""
        global TEST_TOKEN
        if not TEST_TOKEN:
            pytest.skip("No auth token available")
        
        response = requests.post(
            f"{BASE_URL}/api/upload/file",
            json={"data": "", "filename": "test.jpg"},
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )
        assert response.status_code == 400
        print("✅ Empty file upload returns 400")


class TestMembershipAPI:
    """Membership Status API Tests"""

    def test_membership_status_unauthorized(self):
        """17. GET /api/membership/status returns 401 without auth"""
        response = requests.get(f"{BASE_URL}/api/membership/status")
        assert response.status_code == 401
        print("✅ Membership status returns 401 without auth")

    def test_membership_status_authorized(self):
        """18. GET /api/membership/status with auth returns status"""
        global TEST_TOKEN
        if not TEST_TOKEN:
            pytest.skip("No auth token available")
        
        response = requests.get(
            f"{BASE_URL}/api/membership/status",
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        assert "active" in data
        assert "plan" in data
        # New user should have free plan
        assert data["plan"] == "free" or data["active"] == False
        print(f"✅ Membership status: plan={data['plan']}, active={data['active']}")


class TestStorePurchase:
    """Store Purchase API Tests"""

    def test_buy_with_gold_unauthorized(self):
        """19. POST /api/store/buy-gold returns 401 without auth"""
        response = requests.post(
            f"{BASE_URL}/api/store/buy-gold",
            json={"item_id": "some-id"}
        )
        assert response.status_code == 401
        print("✅ Store buy returns 401 without auth")

    def test_my_purchases_unauthorized(self):
        """20. GET /api/store/my-purchases returns 401 without auth"""
        response = requests.get(f"{BASE_URL}/api/store/my-purchases")
        assert response.status_code == 401
        print("✅ My purchases returns 401 without auth")

    def test_my_purchases_authorized(self):
        """21. GET /api/store/my-purchases with auth returns purchases list"""
        global TEST_TOKEN
        if not TEST_TOKEN:
            pytest.skip("No auth token available")
        
        response = requests.get(
            f"{BASE_URL}/api/store/my-purchases",
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        assert "purchases" in data
        assert isinstance(data["purchases"], list)
        print(f"✅ My purchases: {len(data['purchases'])} items")


class TestSohbaAPIs:
    """Sohba Social Platform API Tests"""

    def test_sohba_categories(self):
        """22. GET /api/sohba/categories returns categories"""
        response = requests.get(f"{BASE_URL}/api/sohba/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert len(data["categories"]) >= 5
        print(f"✅ Sohba categories: {len(data['categories'])} categories")

    def test_sohba_posts(self):
        """23. GET /api/sohba/posts returns posts"""
        response = requests.get(f"{BASE_URL}/api/sohba/posts")
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
        assert "total" in data
        print(f"✅ Sohba posts: {len(data['posts'])} posts, total={data['total']}")


class TestIslamicTools:
    """Islamic Tools API Tests"""

    def test_prayer_times(self):
        """24. GET /api/prayer-times returns prayer times"""
        response = requests.get(f"{BASE_URL}/api/prayer-times?lat=24.68&lon=46.72")
        assert response.status_code == 200
        data = response.json()
        assert "times" in data or "success" in data
        print("✅ Prayer times API works")

    def test_daily_hadith(self):
        """25. GET /api/daily-hadith returns hadith"""
        response = requests.get(f"{BASE_URL}/api/daily-hadith")
        assert response.status_code == 200
        data = response.json()
        assert "hadith" in data
        assert "text" in data["hadith"]
        print(f"✅ Daily hadith: {data['hadith']['text'][:50]}...")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
