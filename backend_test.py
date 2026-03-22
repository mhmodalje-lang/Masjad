#!/usr/bin/env python3
"""
Baraka Market Monetization System Backend API Testing
Testing wallet, earning, transfer, transactions, leaderboard, and ad configuration APIs
"""

import requests
import json
import time
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://story-central-9.preview.emergentagent.com"

class BarakaMarketTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = []
        self.test_users = {
            "new_test_user": "new_test_user",
            "test_user_1": "test_user_1", 
            "test_earn_user": "test_earn_user",
            "parent_1": "parent_1",
            "kid_1": "kid_1"
        }
        
    def log_result(self, test_name: str, status: str, response_time: float, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "response_time": f"{response_time:.3f}s",
            "details": details
        }
        self.results.append(result)
        self.total_tests += 1
        if status == "PASSED":
            self.passed_tests += 1
        else:
            self.failed_tests.append(result)
            
    def test_get_request(self, endpoint: str, expected_status: int = 200) -> Dict[str, Any]:
        """Test a GET endpoint"""
        url = f"{BACKEND_URL}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code != expected_status:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": f"Expected {expected_status}, got {response.status_code}",
                    "response_text": response.text[:500] if response.text else "No response text"
                }
                
            try:
                data = response.json()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "data": data
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": "Invalid JSON response",
                    "response_text": response.text[:500]
                }
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return {
                "success": False,
                "status_code": 0,
                "response_time": response_time,
                "error": f"Request failed: {str(e)}"
            }

    def test_post_request(self, endpoint: str, data: dict = None, expected_status: int = 200) -> Dict[str, Any]:
        """Test a POST endpoint"""
        url = f"{BACKEND_URL}{endpoint}"
        start_time = time.time()
        
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=data, headers=headers, timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code != expected_status:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": f"Expected {expected_status}, got {response.status_code}",
                    "response_text": response.text[:500] if response.text else "No response text"
                }
                
            try:
                response_data = response.json()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "data": response_data
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": "Invalid JSON response",
                    "response_text": response.text[:500]
                }
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return {
                "success": False,
                "status_code": 0,
                "response_time": response_time,
                "error": f"Request failed: {str(e)}"
            }

    def test_wallet_creation_and_retrieval(self):
        """Test wallet creation and retrieval"""
        print("💰 Testing Wallet Creation and Retrieval...")
        
        # Test 1: Create new wallet
        result = self.test_get_request(f"/api/baraka/wallet/{self.test_users['new_test_user']}")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Wallet Creation (new_test_user)", "FAILED", result["response_time"], 
                              "Response success=false")
                return
            
            wallet = data.get("wallet", {})
            
            # Verify new wallet has 0 coins
            if wallet.get("blessing_coins") != 0:
                self.log_result("Wallet Creation (new_test_user)", "FAILED", result["response_time"], 
                              f"Expected 0 blessing_coins, got {wallet.get('blessing_coins')}")
                return
            
            if wallet.get("golden_bricks") != 0:
                self.log_result("Wallet Creation (new_test_user)", "FAILED", result["response_time"], 
                              f"Expected 0 golden_bricks, got {wallet.get('golden_bricks')}")
                return
            
            # Check required fields
            required_fields = ["user_id", "blessing_coins", "golden_bricks", "total_earned_coins", 
                             "total_earned_bricks", "ads_watched_today", "created_at"]
            missing_fields = [field for field in required_fields if field not in wallet]
            
            if missing_fields:
                self.log_result("Wallet Creation (new_test_user)", "FAILED", result["response_time"], 
                              f"Missing fields: {', '.join(missing_fields)}")
                return
            
            self.log_result("Wallet Creation (new_test_user)", "PASSED", result["response_time"], 
                          "New wallet created with 0 coins and all required fields")
            
        else:
            self.log_result("Wallet Creation (new_test_user)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test 2: Retrieve existing wallet
        result = self.test_get_request(f"/api/baraka/wallet/{self.test_users['test_user_1']}")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Wallet Retrieval (test_user_1)", "FAILED", result["response_time"], 
                              "Response success=false")
                return
            
            wallet = data.get("wallet", {})
            
            if wallet.get("user_id") != self.test_users['test_user_1']:
                self.log_result("Wallet Retrieval (test_user_1)", "FAILED", result["response_time"], 
                              f"Wrong user_id: expected {self.test_users['test_user_1']}, got {wallet.get('user_id')}")
                return
            
            self.log_result("Wallet Retrieval (test_user_1)", "PASSED", result["response_time"], 
                          f"Wallet retrieved with {wallet.get('blessing_coins', 0)} coins")
            
        else:
            self.log_result("Wallet Retrieval (test_user_1)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_earn_coins_functionality(self):
        """Test earning coins from rewarded videos"""
        print("🎬 Testing Earn Coins Functionality...")
        
        user_id = self.test_users['test_earn_user']
        
        # Get initial wallet state
        initial_result = self.test_get_request(f"/api/baraka/wallet/{user_id}")
        initial_coins = 0
        initial_ads_watched = 0
        
        if initial_result["success"] and initial_result["data"].get("success"):
            wallet = initial_result["data"].get("wallet", {})
            initial_coins = wallet.get("blessing_coins", 0)
            initial_ads_watched = wallet.get("ads_watched_today", 0)
        
        # Test 1: First earn coins request
        earn_data = {
            "ad_type": "rewarded_video",
            "placement": "baraka_market"
        }
        
        result = self.test_post_request(f"/api/baraka/earn?user_id={user_id}", earn_data)
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Earn Coins (First Request)", "FAILED", result["response_time"], 
                              f"Response success=false: {data.get('message', 'No message')}")
                return
            
            earned = data.get("earned", 0)
            wallet = data.get("wallet", {})
            ads_remaining = data.get("ads_remaining", 0)
            
            # Verify earned amount (should be 20)
            if earned != 20:
                self.log_result("Earn Coins (First Request)", "FAILED", result["response_time"], 
                              f"Expected 20 coins earned, got {earned}")
                return
            
            # Verify wallet update
            expected_coins = initial_coins + 20
            if wallet.get("blessing_coins") != expected_coins:
                self.log_result("Earn Coins (First Request)", "FAILED", result["response_time"], 
                              f"Expected {expected_coins} total coins, got {wallet.get('blessing_coins')}")
                return
            
            # Verify ads remaining decreased
            if ads_remaining >= 10:
                self.log_result("Earn Coins (First Request)", "FAILED", result["response_time"], 
                              f"Expected ads_remaining < 10, got {ads_remaining}")
                return
            
            self.log_result("Earn Coins (First Request)", "PASSED", result["response_time"], 
                          f"Earned 20 coins, total: {wallet.get('blessing_coins')}, ads remaining: {ads_remaining}")
            
        else:
            self.log_result("Earn Coins (First Request)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
            return
        
        # Test 2: Second earn coins request (should earn another 20)
        result = self.test_post_request(f"/api/baraka/earn?user_id={user_id}", earn_data)
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Earn Coins (Second Request)", "FAILED", result["response_time"], 
                              f"Response success=false: {data.get('message', 'No message')}")
                return
            
            earned = data.get("earned", 0)
            wallet = data.get("wallet", {})
            
            # Verify earned amount (should be 20 again)
            if earned != 20:
                self.log_result("Earn Coins (Second Request)", "FAILED", result["response_time"], 
                              f"Expected 20 coins earned, got {earned}")
                return
            
            # Verify total coins (should be initial + 40)
            expected_total = initial_coins + 40
            if wallet.get("blessing_coins") != expected_total:
                self.log_result("Earn Coins (Second Request)", "FAILED", result["response_time"], 
                              f"Expected {expected_total} total coins, got {wallet.get('blessing_coins')}")
                return
            
            self.log_result("Earn Coins (Second Request)", "PASSED", result["response_time"], 
                          f"Earned another 20 coins, total: {wallet.get('blessing_coins')}")
            
        else:
            self.log_result("Earn Coins (Second Request)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_transfer_golden_bricks(self):
        """Test transferring golden bricks to kids"""
        print("🧱 Testing Transfer Golden Bricks...")
        
        parent_id = self.test_users['parent_1']
        kid_id = self.test_users['kid_1']
        
        # Get initial wallet states
        parent_initial = self.test_get_request(f"/api/baraka/wallet/{parent_id}")
        kid_initial = self.test_get_request(f"/api/baraka/wallet/{kid_id}")
        
        initial_parent_bricks = 0
        initial_kid_bricks = 0
        
        if parent_initial["success"] and parent_initial["data"].get("success"):
            initial_parent_bricks = parent_initial["data"]["wallet"].get("golden_bricks", 0)
        
        if kid_initial["success"] and kid_initial["data"].get("success"):
            initial_kid_bricks = kid_initial["data"]["wallet"].get("golden_bricks", 0)
        
        # Test transfer
        transfer_data = {
            "kid_id": kid_id,
            "amount": 50
        }
        
        result = self.test_post_request(f"/api/baraka/transfer?user_id={parent_id}", transfer_data)
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Transfer Golden Bricks", "FAILED", result["response_time"], 
                              f"Response success=false: {data.get('message', 'No message')}")
                return
            
            transferred = data.get("transferred", 0)
            to_kid = data.get("to_kid", "")
            parent_wallet = data.get("parent_wallet", {})
            
            # Verify transfer amount
            if transferred != 50:
                self.log_result("Transfer Golden Bricks", "FAILED", result["response_time"], 
                              f"Expected 50 bricks transferred, got {transferred}")
                return
            
            # Verify recipient
            if to_kid != kid_id:
                self.log_result("Transfer Golden Bricks", "FAILED", result["response_time"], 
                              f"Expected transfer to {kid_id}, got {to_kid}")
                return
            
            # Verify parent wallet update
            expected_parent_bricks = initial_parent_bricks + 50
            if parent_wallet.get("golden_bricks") != expected_parent_bricks:
                self.log_result("Transfer Golden Bricks", "FAILED", result["response_time"], 
                              f"Expected parent to have {expected_parent_bricks} bricks, got {parent_wallet.get('golden_bricks')}")
                return
            
            self.log_result("Transfer Golden Bricks", "PASSED", result["response_time"], 
                          f"Transferred 50 golden bricks from {parent_id} to {kid_id}")
            
        else:
            self.log_result("Transfer Golden Bricks", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
            return
        
        # Verify kid received the bricks
        kid_result = self.test_get_request(f"/api/baraka/wallet/{kid_id}")
        
        if kid_result["success"]:
            data = kid_result["data"]
            
            if data.get("success"):
                wallet = data.get("wallet", {})
                expected_kid_bricks = initial_kid_bricks + 50
                
                if wallet.get("golden_bricks") == expected_kid_bricks:
                    self.log_result("Kid Wallet Verification", "PASSED", kid_result["response_time"], 
                                  f"Kid received 50 golden bricks, total: {wallet.get('golden_bricks')}")
                else:
                    self.log_result("Kid Wallet Verification", "FAILED", kid_result["response_time"], 
                                  f"Expected kid to have {expected_kid_bricks} bricks, got {wallet.get('golden_bricks')}")
            else:
                self.log_result("Kid Wallet Verification", "FAILED", kid_result["response_time"], 
                              "Failed to get kid wallet")
        else:
            self.log_result("Kid Wallet Verification", "FAILED", kid_result["response_time"], 
                          kid_result.get("error", "Unknown error"))

    def test_transactions_history(self):
        """Test transaction history retrieval"""
        print("📜 Testing Transactions History...")
        
        # Test transactions for earn user
        earn_user = self.test_users['test_earn_user']
        result = self.test_get_request(f"/api/baraka/transactions/{earn_user}")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Transactions (Earn User)", "FAILED", result["response_time"], 
                              "Response success=false")
                return
            
            transactions = data.get("transactions", [])
            total = data.get("total", 0)
            
            # Should have earn transactions
            earn_transactions = [tx for tx in transactions if tx.get("type") == "earn"]
            
            if len(earn_transactions) == 0:
                self.log_result("Transactions (Earn User)", "FAILED", result["response_time"], 
                              "No earn transactions found")
                return
            
            # Verify transaction structure
            for tx in earn_transactions[:2]:  # Check first 2 transactions
                required_fields = ["user_id", "type", "amount", "currency", "created_at"]
                missing_fields = [field for field in required_fields if field not in tx]
                
                if missing_fields:
                    self.log_result("Transactions (Earn User)", "FAILED", result["response_time"], 
                                  f"Missing fields in transaction: {', '.join(missing_fields)}")
                    return
            
            self.log_result("Transactions (Earn User)", "PASSED", result["response_time"], 
                          f"Found {len(earn_transactions)} earn transactions out of {total} total")
            
        else:
            self.log_result("Transactions (Earn User)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))
        
        # Test transactions for parent (should have transfer_out)
        parent_user = self.test_users['parent_1']
        result = self.test_get_request(f"/api/baraka/transactions/{parent_user}")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Transactions (Parent)", "FAILED", result["response_time"], 
                              "Response success=false")
                return
            
            transactions = data.get("transactions", [])
            
            # Should have transfer_out transactions
            transfer_transactions = [tx for tx in transactions if tx.get("type") == "transfer_out"]
            
            if len(transfer_transactions) == 0:
                self.log_result("Transactions (Parent)", "FAILED", result["response_time"], 
                              "No transfer_out transactions found")
                return
            
            self.log_result("Transactions (Parent)", "PASSED", result["response_time"], 
                          f"Found {len(transfer_transactions)} transfer_out transactions")
            
        else:
            self.log_result("Transactions (Parent)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_leaderboard(self):
        """Test leaderboard functionality"""
        print("🏆 Testing Leaderboard...")
        
        result = self.test_get_request("/api/baraka/leaderboard")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Leaderboard", "FAILED", result["response_time"], 
                              "Response success=false")
                return
            
            leaderboard = data.get("leaderboard", [])
            
            if len(leaderboard) == 0:
                self.log_result("Leaderboard", "FAILED", result["response_time"], 
                              "Empty leaderboard")
                return
            
            # Verify leaderboard structure
            for entry in leaderboard[:3]:  # Check first 3 entries
                required_fields = ["user_id", "blessing_coins", "total_earned_coins"]
                missing_fields = [field for field in required_fields if field not in entry]
                
                if missing_fields:
                    self.log_result("Leaderboard", "FAILED", result["response_time"], 
                                  f"Missing fields in leaderboard entry: {', '.join(missing_fields)}")
                    return
            
            # Verify sorting (should be sorted by total_earned_coins descending)
            is_sorted = True
            for i in range(len(leaderboard) - 1):
                if leaderboard[i].get("total_earned_coins", 0) < leaderboard[i + 1].get("total_earned_coins", 0):
                    is_sorted = False
                    break
            
            if not is_sorted:
                self.log_result("Leaderboard", "FAILED", result["response_time"], 
                              "Leaderboard not sorted by total_earned_coins descending")
                return
            
            self.log_result("Leaderboard", "PASSED", result["response_time"], 
                          f"Leaderboard with {len(leaderboard)} users, sorted correctly")
            
        else:
            self.log_result("Leaderboard", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_ad_configuration(self):
        """Test ad configuration retrieval"""
        print("⚙️ Testing Ad Configuration...")
        
        result = self.test_get_request("/api/admin/ads_config")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Ad Configuration", "FAILED", result["response_time"], 
                              "Response success=false")
                return
            
            config = data.get("config", {})
            
            # Check required fields
            required_fields = [
                "id", "rewards_enabled", "rewarded_video_enabled", "native_ads_enabled",
                "kids_zone_ads", "rewarded_video_coins", "transfer_bricks_amount",
                "daily_reward_limit", "admob_banner_id", "admob_rewarded_id"
            ]
            
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                self.log_result("Ad Configuration", "FAILED", result["response_time"], 
                              f"Missing fields: {', '.join(missing_fields)}")
                return
            
            # Verify COPPA compliance (kids_zone_ads should be False)
            if config.get("kids_zone_ads") is not False:
                self.log_result("Ad Configuration", "FAILED", result["response_time"], 
                              f"COPPA violation: kids_zone_ads is {config.get('kids_zone_ads')}, should be False")
                return
            
            # Verify default values
            if config.get("rewarded_video_coins") != 20:
                self.log_result("Ad Configuration", "FAILED", result["response_time"], 
                              f"Expected rewarded_video_coins=20, got {config.get('rewarded_video_coins')}")
                return
            
            if config.get("transfer_bricks_amount") != 50:
                self.log_result("Ad Configuration", "FAILED", result["response_time"], 
                              f"Expected transfer_bricks_amount=50, got {config.get('transfer_bricks_amount')}")
                return
            
            self.log_result("Ad Configuration", "PASSED", result["response_time"], 
                          f"Full config with COPPA compliance (kids_zone_ads=False)")
            
        else:
            self.log_result("Ad Configuration", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_ad_configuration_update_coppa(self):
        """Test ad configuration update with COPPA enforcement"""
        print("🔒 Testing Ad Configuration Update (COPPA)...")
        
        # Try to enable kids_zone_ads (should be forced to False)
        update_data = {
            "kids_zone_ads": True
        }
        
        result = self.test_post_request("/api/admin/ads_config", update_data)
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("Ad Config Update (COPPA)", "FAILED", result["response_time"], 
                              "Response success=false")
                return
            
            config = data.get("config", {})
            
            # Verify kids_zone_ads is still False (COPPA enforcement)
            if config.get("kids_zone_ads") is not False:
                self.log_result("Ad Config Update (COPPA)", "FAILED", result["response_time"], 
                              f"COPPA enforcement failed: kids_zone_ads is {config.get('kids_zone_ads')}, should be False")
                return
            
            # Verify updated_at field was set
            if not config.get("updated_at"):
                self.log_result("Ad Config Update (COPPA)", "FAILED", result["response_time"], 
                              "updated_at field not set")
                return
            
            self.log_result("Ad Config Update (COPPA)", "PASSED", result["response_time"], 
                          "COPPA enforcement working: kids_zone_ads forced to False")
            
        else:
            self.log_result("Ad Config Update (COPPA)", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_user_eligibility_check(self):
        """Test user ad eligibility check"""
        print("✅ Testing User Eligibility Check...")
        
        test_user = self.test_users['test_user_1']
        result = self.test_get_request(f"/api/admin/ads_config/check_user/{test_user}")
        
        if result["success"]:
            data = result["data"]
            
            if not data.get("success"):
                self.log_result("User Eligibility Check", "FAILED", result["response_time"], 
                              "Response success=false")
                return
            
            eligible = data.get("eligible")
            reason = data.get("reason", "")
            user_id = data.get("user_id", "")
            
            # Verify response structure
            if eligible is None:
                self.log_result("User Eligibility Check", "FAILED", result["response_time"], 
                              "Missing 'eligible' field")
                return
            
            if user_id != test_user:
                self.log_result("User Eligibility Check", "FAILED", result["response_time"], 
                              f"Wrong user_id: expected {test_user}, got {user_id}")
                return
            
            # For a normal user, should be eligible
            if eligible is True and reason == "eligible":
                self.log_result("User Eligibility Check", "PASSED", result["response_time"], 
                              f"User {test_user} is eligible for ads")
            else:
                self.log_result("User Eligibility Check", "PASSED", result["response_time"], 
                              f"User {test_user} eligibility: {eligible}, reason: {reason}")
            
        else:
            self.log_result("User Eligibility Check", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def test_api_health(self):
        """Test basic API health"""
        print("🏥 Testing API Health...")
        
        result = self.test_get_request("/api/health")
        
        if result["success"]:
            data = result["data"]
            if data.get("status") == "healthy":
                self.log_result("API Health Check", "PASSED", result["response_time"], 
                              f"Status: {data.get('status')}")
            else:
                self.log_result("API Health Check", "FAILED", result["response_time"], 
                              f"Unhealthy status: {data.get('status')}")
        else:
            self.log_result("API Health Check", "FAILED", result["response_time"], 
                          result.get("error", "Unknown error"))

    def run_all_tests(self):
        """Run all Baraka Market tests"""
        print("🚀 Starting Baraka Market Monetization System Backend API Tests...")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 70)
        
        # Run all test suites
        self.test_api_health()
        self.test_wallet_creation_and_retrieval()
        self.test_earn_coins_functionality()
        self.test_transfer_golden_bricks()
        self.test_transactions_history()
        self.test_leaderboard()
        self.test_ad_configuration()
        self.test_ad_configuration_update_coppa()
        self.test_user_eligibility_check()
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in self.failed_tests:
                print(f"  • {test['test']}: {test['details']}")
        
        print("\n✅ PASSED TESTS:")
        for result in self.results:
            if result["status"] == "PASSED":
                print(f"  • {result['test']}: {result['details']}")
        
        return {
            "total": self.total_tests,
            "passed": self.passed_tests,
            "failed": self.total_tests - self.passed_tests,
            "success_rate": self.passed_tests/self.total_tests*100 if self.total_tests > 0 else 0,
            "failed_tests": self.failed_tests
        }

if __name__ == "__main__":
    tester = BarakaMarketTester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open("/app/baraka_market_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": results,
            "detailed_results": tester.results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed results saved to: /app/baraka_market_test_results.json")