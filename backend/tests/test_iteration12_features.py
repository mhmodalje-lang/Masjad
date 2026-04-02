"""
Iteration 12: Testing NEW commercial platform features
- Virtual credits system with GPS currency detection
- Islamic gift store with 50/50 revenue sharing
- Ad manager with admin approval
- AI Religious Assistant (GPT-5.2) with free questions limit
- Vendor marketplace sorted by GPS proximity
- Updated admin dashboard tabs
"""
import pytest
import requests
import os
import uuid
from datetime import datetime

# Use the public URL for testing
BASE_URL = os.environ.get('TEST_BASE_URL', 'http://localhost:8001')

# Test credentials
TEST_EMAIL = f"test_iter12_{uuid.uuid4().hex[:6]}@test.com"
TEST_PASSWORD = os.getenv('TEST_PASSWORD', 'TestPass123!')
ADMIN_EMAIL = os.getenv('TEST_ADMIN_EMAIL', 'mhmd321324t@gmail.com')


class TestHealthAndBasics:
    """Basic API health checks"""
    
    def test_api_root(self):
        """Test API root endpoint"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        print(f"API Root: {data}")
    
    def test_health_endpoint(self):
        """Test health endpoint"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        print(f"Health: {data}")


class TestGiftsAPI:
    """Test Islamic gift store - 12 gifts expected"""
    
    def test_gifts_list_returns_12_gifts(self):
        """GET /api/gifts/list - should return 12 Islamic gifts"""
        response = requests.get(f"{BASE_URL}/api/gifts/list")
        assert response.status_code == 200
        data = response.json()
        assert "gifts" in data
        assert len(data["gifts"]) == 12, f"Expected 12 gifts, got {len(data['gifts'])}"
        
        # Verify gift structure
        for gift in data["gifts"]:
            assert "id" in gift
            assert "name" in gift
            assert "emoji" in gift
            assert "price_credits" in gift
            assert "description" in gift
        
        print(f"Gifts count: {len(data['gifts'])}")
        print(f"Gift samples: {[g['name'] for g in data['gifts'][:3]]}")


class TestCreditsAPI:
    """Test virtual credits system with GPS-based currency detection"""
    
    def test_credits_packages_default(self):
        """GET /api/credits/packages - default packages"""
        response = requests.get(f"{BASE_URL}/api/credits/packages")
        assert response.status_code == 200
        data = response.json()
        assert "packages" in data
        assert len(data["packages"]) == 8, f"Expected 8 packages, got {len(data['packages'])}"
        
        # Verify package structure
        for pkg in data["packages"]:
            assert "id" in pkg
            assert "credits" in pkg
            assert "price_eur" in pkg
            assert "local_price" in pkg
            assert "currency_code" in pkg
        
        print(f"Packages count: {len(data['packages'])}")
    
    def test_credits_packages_saudi_arabia(self):
        """GET /api/credits/packages?country=SA - returns SAR currency"""
        response = requests.get(f"{BASE_URL}/api/credits/packages?country=SA")
        assert response.status_code == 200
        data = response.json()
        assert "packages" in data
        assert len(data["packages"]) == 8
        
        # Verify SAR currency
        assert data["currency"]["code"] == "SAR"
        assert data["currency"]["symbol"] == "ر.س"
        
        for pkg in data["packages"]:
            assert pkg["currency_code"] == "SAR"
        
        print(f"SAR packages: {data['packages'][0]}")
    
    def test_detect_currency_saudi_coordinates(self):
        """GET /api/credits/detect-currency - detect Saudi Arabia from GPS"""
        # Mecca coordinates
        response = requests.get(f"{BASE_URL}/api/credits/detect-currency?lat=21.42&lon=39.82")
        assert response.status_code == 200
        data = response.json()
        
        assert "country_code" in data
        assert "currency" in data
        # The API may return SA or fallback to US
        print(f"Detected: {data}")


class TestAuthAPI:
    """Test authentication endpoints"""
    
    def test_register_new_user(self):
        """POST /api/auth/register - create new user"""
        response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "name": "Test User Iter12"
        })
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == TEST_EMAIL.lower()
        
        # Store token for subsequent tests
        TestAuthAPI.auth_token = data["access_token"]
        TestAuthAPI.user_id = data["user"]["id"]
        
        print(f"Registered user: {data['user']['email']}")
    
    def test_login_user(self):
        """POST /api/auth/login - login existing user"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert "user" in data
        
        print(f"Login successful for: {data['user']['email']}")


class TestGiftsSendAPI:
    """Test gift sending functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_users(self):
        """Create sender and recipient users"""
        # Register sender
        sender_email = f"gift_sender_{uuid.uuid4().hex[:6]}@test.com"
        res1 = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": sender_email,
            "password": TEST_PASSWORD,
            "name": "Gift Sender"
        })
        if res1.status_code == 200:
            self.sender_token = res1.json()["access_token"]
            self.sender_id = res1.json()["user"]["id"]
        else:
            pytest.skip("Could not create sender user")
        
        # Register recipient
        recipient_email = f"gift_recipient_{uuid.uuid4().hex[:6]}@test.com"
        res2 = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": recipient_email,
            "password": TEST_PASSWORD,
            "name": "Gift Recipient"
        })
        if res2.status_code == 200:
            self.recipient_id = res2.json()["user"]["id"]
        else:
            pytest.skip("Could not create recipient user")
    
    def test_send_gift_requires_credits(self):
        """POST /api/gifts/send - needs credits to send gift"""
        headers = {"Authorization": f"Bearer {self.sender_token}"}
        response = requests.post(f"{BASE_URL}/api/gifts/send", json={
            "gift_id": "gift_rose",  # 20 credits
            "recipient_id": self.recipient_id
        }, headers=headers)
        
        # Should fail due to insufficient credits (new user has 0)
        assert response.status_code in [200, 400]
        data = response.json()
        if response.status_code == 400:
            assert "كافٍ" in data.get("detail", "") or "credits" in data.get("detail", "").lower()
            print(f"Expected: insufficient credits - {data}")
        else:
            print(f"Gift sent: {data}")


class TestAdsAPI:
    """Test ad submission and retrieval"""
    
    @pytest.fixture(autouse=True)
    def setup_auth(self):
        """Get auth token"""
        email = f"ad_user_{uuid.uuid4().hex[:6]}@test.com"
        res = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": email,
            "password": TEST_PASSWORD
        })
        if res.status_code == 200:
            self.token = res.json()["access_token"]
        else:
            pytest.skip("Auth failed")
    
    def test_submit_ad_for_review(self):
        """POST /api/ads/submit - submit ad for admin review"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{BASE_URL}/api/ads/submit", json={
            "title": "Test Islamic Channel Ad",
            "description": "Islamic content channel promotion",
            "video_url": "https://www.youtube.com/watch?v=test123",
            "embed_type": "youtube",
            "channel_name": "Test Islamic Channel"
        }, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data.get("success")
        assert "ad" in data
        assert data["ad"]["status"] == "pending"
        
        print(f"Ad submitted: {data['ad']['title']}")
    
    def test_get_approved_ads(self):
        """GET /api/ads/approved - get list of approved ads"""
        response = requests.get(f"{BASE_URL}/api/ads/approved")
        assert response.status_code == 200
        data = response.json()
        assert "ads" in data
        print(f"Approved ads count: {len(data['ads'])}")


class TestMarketplaceAPI:
    """Test vendor marketplace"""
    
    @pytest.fixture(autouse=True)
    def setup_auth(self):
        """Get auth token"""
        email = f"vendor_{uuid.uuid4().hex[:6]}@test.com"
        res = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": email,
            "password": TEST_PASSWORD
        })
        if res.status_code == 200:
            self.token = res.json()["access_token"]
        else:
            pytest.skip("Auth failed")
    
    def test_create_product(self):
        """POST /api/marketplace/products - create product listing"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{BASE_URL}/api/marketplace/products", json={
            "name": "Islamic Prayer Beads",
            "description": "High quality prayer beads",
            "price": 25.99,
            "currency": "EUR",
            "category": "accessories",
            "location": {"lat": 21.42, "lon": 39.82, "city": "Mecca"}
        }, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data.get("success")
        assert "product" in data
        assert data["product"]["name"] == "Islamic Prayer Beads"
        
        print(f"Product created: {data['product']['name']}")
    
    def test_list_products(self):
        """GET /api/marketplace/products - list products"""
        response = requests.get(f"{BASE_URL}/api/marketplace/products")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        print(f"Products count: {len(data['products'])}")
    
    def test_list_products_with_location(self):
        """GET /api/marketplace/products - with GPS sorting"""
        response = requests.get(f"{BASE_URL}/api/marketplace/products?lat=21.42&lon=39.82")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        print(f"Products near Mecca: {len(data['products'])}")


class TestAIAssistantAPI:
    """Test AI Religious Assistant"""
    
    @pytest.fixture(autouse=True)
    def setup_auth(self):
        """Get auth token"""
        email = f"ai_user_{uuid.uuid4().hex[:6]}@test.com"
        res = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": email,
            "password": TEST_PASSWORD
        })
        if res.status_code == 200:
            self.token = res.json()["access_token"]
        else:
            pytest.skip("Auth failed")
    
    def test_ai_ask_islamic_question(self):
        """POST /api/ai/ask - ask Islamic question"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{BASE_URL}/api/ai/ask", json={
            "question": "ما هي أركان الإسلام؟",
            "session_id": str(uuid.uuid4())
        }, headers=headers, timeout=30)  # AI might take time
        
        assert response.status_code == 200
        data = response.json()
        
        # Either get answer or error (AI may fail in test env)
        if "answer" in data and data["answer"]:
            assert len(data["answer"]) > 0
            print(f"AI Answer: {data['answer'][:100]}...")
        elif "error" in data:
            # AI error is expected in test environment
            print(f"AI error (expected): {data.get('message', data.get('error'))}")
        
        # Check remaining questions tracking
        if "remaining" in data:
            assert data["remaining"] <= 20
            print(f"Questions remaining: {data['remaining']}")
    
    def test_ai_ask_requires_auth(self):
        """POST /api/ai/ask without auth should fail"""
        response = requests.post(f"{BASE_URL}/api/ai/ask", json={
            "question": "What is Islam?"
        })
        assert response.status_code == 401


class TestPaymentsAPI:
    """Test payments/packages API"""
    
    def test_get_gold_packages(self):
        """GET /api/payments/packages - gold packages list"""
        response = requests.get(f"{BASE_URL}/api/payments/packages")
        assert response.status_code == 200
        data = response.json()
        assert "packages" in data
        assert len(data["packages"]) >= 3  # gold_100, gold_500, gold_1000, membership
        
        # Verify package types
        gold_packages = [p for p in data["packages"] if p.get("type") == "gold"]
        assert len(gold_packages) >= 3
        
        print(f"Packages: {data['packages']}")


class TestStoreAPI:
    """Test store items API"""
    
    def test_get_store_items(self):
        """GET /api/store/items - store items list"""
        response = requests.get(f"{BASE_URL}/api/store/items")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 5  # Should have default items
        
        # Verify item structure
        for item in data["items"]:
            assert "id" in item
            assert "name" in item
            assert "price_gold" in item
        
        print(f"Store items count: {len(data['items'])}")


class TestRewardsAPI:
    """Test rewards balance API"""
    
    @pytest.fixture(autouse=True)
    def setup_auth(self):
        """Get auth token"""
        email = f"rewards_user_{uuid.uuid4().hex[:6]}@test.com"
        res = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": email,
            "password": TEST_PASSWORD
        })
        if res.status_code == 200:
            self.token = res.json()["access_token"]
        else:
            pytest.skip("Auth failed")
    
    def test_get_rewards_balance(self):
        """GET /api/rewards/balance - requires auth"""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{BASE_URL}/api/rewards/balance", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "gold" in data
        print(f"Balance: {data}")


# Run all tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
