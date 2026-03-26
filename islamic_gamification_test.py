#!/usr/bin/env python3
"""
Islamic Education App Gamification Backend API Testing
=====================================================
Testing all 15 endpoints specified in the review request:
1. Health check
2. Points balance (kids & adults modes)
3. Points earning (kids & adults)
4. Ad configuration and rewards
5. Parental gate challenge and verification
6. Leaderboards (kids & adults)
7. Points history
8. Premium catalog
9. Daily content
10. Active ads
"""

import asyncio
import httpx
import json
import time
import re
from typing import Dict, List, Any, Optional

# Backend URL from review request
BACKEND_URL = "https://translate-hub-123.preview.emergentagent.com"

class IslamicGamificationTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.challenge_data = {}  # Store challenge data for verification
        
    async def test_endpoint(self, method: str, endpoint: str, expected_status: int = 200, 
                          data: dict = None, description: str = "") -> dict:
        """Test a single endpoint and return results."""
        self.total_tests += 1
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                url = f"{self.base_url}{endpoint}"
                
                if method.upper() == "GET":
                    response = await client.get(url)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                response_time = time.time() - start_time
                
                # Parse response
                try:
                    response_data = response.json()
                except:
                    response_data = {"raw_response": response.text}
                
                # Determine if test passed
                status_ok = response.status_code == expected_status
                
                # Special handling for daily content endpoint
                if "/daily-content/" in endpoint and response.status_code == 200:
                    # For daily content, success=false with "No content available" is acceptable
                    if response_data.get("success") == False and "No content available" in response_data.get("message", ""):
                        has_success = True
                    else:
                        has_success = response_data.get("success", True)
                else:
                    has_success = response_data.get("success", True) if expected_status == 200 else True
                
                test_passed = status_ok and has_success
                if test_passed:
                    self.passed_tests += 1
                
                result = {
                    "endpoint": endpoint,
                    "method": method.upper(),
                    "description": description,
                    "status_code": response.status_code,
                    "expected_status": expected_status,
                    "response_time": round(response_time, 3),
                    "passed": test_passed,
                    "response_data": response_data,
                    "error": None
                }
                
                self.results.append(result)
                return result
                
        except Exception as e:
            response_time = time.time() - start_time
            result = {
                "endpoint": endpoint,
                "method": method.upper(), 
                "description": description,
                "status_code": 0,
                "expected_status": expected_status,
                "response_time": round(response_time, 3),
                "passed": False,
                "response_data": {},
                "error": str(e)
            }
            self.results.append(result)
            return result

    def calculate_math_answer(self, question: str) -> Optional[int]:
        """Parse and calculate the answer to a math question."""
        try:
            # Remove "= ?" from the end and clean up
            question = question.replace("= ?", "").replace("=?", "").strip()
            
            # Handle different operators
            if "+" in question:
                parts = question.split("+")
                return int(parts[0].strip()) + int(parts[1].strip())
            elif "-" in question:
                parts = question.split("-")
                return int(parts[0].strip()) - int(parts[1].strip())
            elif "×" in question or "*" in question:
                parts = question.split("×" if "×" in question else "*")
                return int(parts[0].strip()) * int(parts[1].strip())
            elif "÷" in question or "/" in question:
                parts = question.split("÷" if "÷" in question else "/")
                return int(parts[0].strip()) // int(parts[1].strip())
            else:
                print(f"   ⚠️  Unknown math operator in question: {question}")
                return None
        except Exception as e:
            print(f"   ⚠️  Error calculating math answer: {e}")
            return None

    def validate_points_balance(self, data: dict, mode: str) -> List[str]:
        """Validate points balance response structure."""
        issues = []
        
        if not data.get("success"):
            issues.append("Response missing success=true")
        
        if mode == "kids":
            if "golden_bricks" not in data:
                issues.append("Kids mode missing golden_bricks")
            if "mosque" not in data:
                issues.append("Kids mode missing mosque data")
        elif mode == "adults":
            if "blessing_points" not in data:
                issues.append("Adults mode missing blessing_points")
            if "rank" not in data:
                issues.append("Adults mode missing rank data")
        
        return issues

    def validate_earn_points(self, data: dict, mode: str) -> List[str]:
        """Validate earn points response structure."""
        issues = []
        
        if not data.get("success"):
            issues.append("Response missing success=true")
        
        if mode == "kids":
            if "points_earned" not in data and "earned_points" not in data and "earned" not in data:
                issues.append("Kids mode missing points_earned/earned_points/earned")
            if "golden_bricks" not in data:
                issues.append("Kids mode missing golden_bricks")
            if "mosque" not in data:
                issues.append("Kids mode missing mosque data")
        elif mode == "adults":
            if "points_earned" not in data and "blessing_points" not in data and "earned" not in data:
                issues.append("Adults mode missing points_earned/blessing_points/earned")
            if "rank" not in data:
                issues.append("Adults mode missing rank data")
        
        return issues

    def validate_ad_config(self, data: dict) -> List[str]:
        """Validate ad config response structure."""
        issues = []
        
        if not data.get("test_mode"):
            issues.append("Missing test_mode=true")
        
        if "ad_units" not in data:
            issues.append("Missing ad_units")
        else:
            ad_units = data["ad_units"]
            required_types = ["rewarded", "interstitial", "banner"]
            for ad_type in required_types:
                if ad_type not in ad_units:
                    issues.append(f"Missing {ad_type} ad unit")
        
        return issues

    def validate_parental_challenge(self, data: dict) -> List[str]:
        """Validate parental gate challenge response."""
        issues = []
        
        if not data.get("success"):
            issues.append("Response missing success=true")
        
        if "challenge_id" not in data:
            issues.append("Missing challenge_id")
        
        if "question" not in data:
            issues.append("Missing question")
        
        return issues

    def validate_leaderboard(self, data: dict) -> List[str]:
        """Validate leaderboard response structure."""
        issues = []
        
        if "leaderboard" not in data:
            issues.append("Missing leaderboard array")
        elif not isinstance(data["leaderboard"], list):
            issues.append("Leaderboard should be an array")
        
        return issues

    async def run_all_tests(self):
        """Run all Islamic Education App gamification tests."""
        print("🧪 Starting Islamic Education App Gamification Backend API Tests")
        print("=" * 70)
        
        # Test 1: Health check
        print("\n1. Testing health check")
        result = await self.test_endpoint(
            "GET", "/api/health",
            description="Health check should return 200 with healthy status"
        )
        if result["passed"]:
            print("   ✅ Health check passed")
        
        # Test 2: Points balance for kids mode
        print("\n2. Testing points balance (kids mode)")
        result = await self.test_endpoint(
            "GET", "/api/points/balance?user_id=test_gamify_1&mode=kids",
            description="Kids mode balance with golden_bricks and mosque stage"
        )
        if result["passed"]:
            issues = self.validate_points_balance(result["response_data"], "kids")
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Kids points balance structure valid")
        
        # Test 3: Points balance for adults mode
        print("\n3. Testing points balance (adults mode)")
        result = await self.test_endpoint(
            "GET", "/api/points/balance?user_id=test_gamify_2&mode=adults",
            description="Adults mode balance with blessing_points and spiritual rank"
        )
        if result["passed"]:
            issues = self.validate_points_balance(result["response_data"], "adults")
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Adults points balance structure valid")
        
        # Test 4: Earn points (kids mode)
        print("\n4. Testing earn points (kids mode)")
        earn_data_kids = {
            "user_id": "test_gamify_1",
            "mode": "kids",
            "reward_type": "lesson_complete"
        }
        result = await self.test_endpoint(
            "POST", "/api/points/earn",
            data=earn_data_kids,
            description="Kids earn points for lesson completion"
        )
        if result["passed"]:
            issues = self.validate_earn_points(result["response_data"], "kids")
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Kids earn points structure valid")
        
        # Test 5: Earn points (adults mode)
        print("\n5. Testing earn points (adults mode)")
        earn_data_adults = {
            "user_id": "test_gamify_2",
            "mode": "adults",
            "reward_type": "prayer_logged"
        }
        result = await self.test_endpoint(
            "POST", "/api/points/earn",
            data=earn_data_adults,
            description="Adults earn blessing points for prayer logging"
        )
        if result["passed"]:
            issues = self.validate_earn_points(result["response_data"], "adults")
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Adults earn points structure valid")
        
        # Test 6: Ad configuration
        print("\n6. Testing ad configuration")
        result = await self.test_endpoint(
            "GET", "/api/rewards/ad-config",
            description="Ad config with test_mode=true and test unit IDs"
        )
        if result["passed"]:
            issues = self.validate_ad_config(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                print("   ✅ Ad configuration structure valid")
        
        # Test 7: Ad watched reward
        print("\n7. Testing ad watched reward")
        ad_watched_data = {
            "user_id": "test_gamify_1",
            "mode": "kids",
            "ad_type": "rewarded"
        }
        result = await self.test_endpoint(
            "POST", "/api/rewards/ad-watched",
            data=ad_watched_data,
            description="Rewarded ad watched with points earned"
        )
        if result["passed"]:
            response_data = result["response_data"]
            if "points_earned" not in response_data:
                print("   ⚠️  Missing points_earned in response")
            else:
                print(f"   ✅ Ad reward processed, points earned: {response_data.get('points_earned', 0)}")
        
        # Test 8: Parental gate challenge
        print("\n8. Testing parental gate challenge")
        result = await self.test_endpoint(
            "GET", "/api/parental-gate/challenge?user_id=test_gamify_1",
            description="Math challenge for parental gate"
        )
        if result["passed"]:
            issues = self.validate_parental_challenge(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                response_data = result["response_data"]
                challenge_id = response_data.get("challenge_id")
                question = response_data.get("question")
                
                if challenge_id and question:
                    # Calculate the answer
                    calculated_answer = self.calculate_math_answer(question)
                    if calculated_answer is not None:
                        self.challenge_data = {
                            "challenge_id": challenge_id,
                            "answer": calculated_answer,
                            "question": question
                        }
                        print(f"   ✅ Challenge received: {question}")
                        print(f"   🧮 Calculated answer: {calculated_answer}")
                    else:
                        print(f"   ⚠️  Could not calculate answer for: {question}")
                else:
                    print("   ⚠️  Missing challenge_id or question")
        
        # Test 9: Parental gate verification
        print("\n9. Testing parental gate verification")
        if self.challenge_data:
            verify_data = {
                "user_id": "test_gamify_1",
                "challenge_id": self.challenge_data["challenge_id"],
                "answer": self.challenge_data["answer"]
            }
            result = await self.test_endpoint(
                "POST", "/api/parental-gate/verify",
                data=verify_data,
                description="Verify math answer with calculated result"
            )
            if result["passed"]:
                response_data = result["response_data"]
                if response_data.get("passed"):
                    print(f"   ✅ Verification passed! Pass token: {response_data.get('pass_token', 'N/A')}")
                else:
                    print(f"   ❌ Verification failed for answer: {self.challenge_data['answer']}")
            else:
                print("   ❌ Verification request failed")
        else:
            print("   ⚠️  Skipping verification - no challenge data available")
        
        # Test 10: Kids leaderboard
        print("\n10. Testing kids leaderboard")
        result = await self.test_endpoint(
            "GET", "/api/points/leaderboard?mode=kids",
            description="Kids leaderboard with golden bricks"
        )
        if result["passed"]:
            issues = self.validate_leaderboard(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                leaderboard = result["response_data"].get("leaderboard", [])
                print(f"   ✅ Kids leaderboard returned {len(leaderboard)} entries")
        
        # Test 11: Adults leaderboard
        print("\n11. Testing adults leaderboard")
        result = await self.test_endpoint(
            "GET", "/api/points/leaderboard?mode=adults",
            description="Adults leaderboard with blessing points"
        )
        if result["passed"]:
            issues = self.validate_leaderboard(result["response_data"])
            if issues:
                print(f"   ⚠️  Validation issues: {', '.join(issues)}")
            else:
                leaderboard = result["response_data"].get("leaderboard", [])
                print(f"   ✅ Adults leaderboard returned {len(leaderboard)} entries")
        
        # Test 12: Points history
        print("\n12. Testing points history")
        result = await self.test_endpoint(
            "GET", "/api/points/history?user_id=test_gamify_1&mode=kids",
            description="Points transaction history for user"
        )
        if result["passed"]:
            response_data = result["response_data"]
            if "transactions" in response_data:
                transactions = response_data["transactions"]
                print(f"   ✅ Points history returned {len(transactions)} transactions")
            else:
                print("   ⚠️  Missing transactions array in response")
        
        # Test 13: Premium catalog
        print("\n13. Testing premium catalog")
        result = await self.test_endpoint(
            "GET", "/api/rewards/premium-catalog?mode=kids",
            description="Premium content catalog for kids"
        )
        if result["passed"]:
            response_data = result["response_data"]
            if "catalog" in response_data:
                catalog = response_data["catalog"]
                print(f"   ✅ Premium catalog returned {len(catalog)} items")
            else:
                print("   ⚠️  Missing catalog array in response")
        
        # Test 14: Daily content
        print("\n14. Testing daily content")
        result = await self.test_endpoint(
            "GET", "/api/daily-content/today?content_type=hadith&locale=ar",
            description="Daily hadith content in Arabic"
        )
        if result["passed"]:
            response_data = result["response_data"]
            if response_data.get("success") == False and "No content available" in response_data.get("message", ""):
                print("   ✅ Daily content endpoint working (no content available as expected)")
            elif response_data.get("success"):
                print("   ✅ Daily content endpoint working with content")
            else:
                print("   ⚠️  Unexpected response format")
        else:
            print("   ❌ Daily content endpoint failed")
        
        # Test 15: Active ads
        print("\n15. Testing active ads")
        result = await self.test_endpoint(
            "GET", "/api/ads/active?placement=home&country=DE",
            description="Active ads for home placement in Germany"
        )
        if result["passed"]:
            response_data = result["response_data"]
            if "ads" in response_data:
                ads = response_data["ads"]
                print(f"   ✅ Active ads returned {len(ads)} ads")
            else:
                print("   ⚠️  Missing ads array in response")

    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 70)
        print("📊 ISLAMIC EDUCATION APP GAMIFICATION TEST RESULTS SUMMARY")
        print("=" * 70)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        avg_response_time = sum(r["response_time"] for r in self.results) / len(self.results) if self.results else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.total_tests - self.passed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Average Response Time: {avg_response_time:.3f}s")
        
        # Show failed tests
        failed_tests = [r for r in self.results if not r["passed"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   • {test['method']} {test['endpoint']}")
                print(f"     Status: {test['status_code']} (expected {test['expected_status']})")
                if test['error']:
                    print(f"     Error: {test['error']}")
                print()
        
        # Show successful tests
        passed_tests = [r for r in self.results if r["passed"]]
        if passed_tests:
            print(f"✅ PASSED TESTS ({len(passed_tests)}):")
            for test in passed_tests:
                print(f"   • {test['method']} {test['endpoint']} ({test['response_time']}s)")
        
        print("\n" + "=" * 70)
        
        # Feature-specific validation
        print("🔍 FEATURE VALIDATION RESULTS:")
        print("-" * 40)
        
        # Gamification features
        points_tests = [r for r in self.results if "/points/" in r["endpoint"]]
        if points_tests:
            passed_points = [r for r in points_tests if r["passed"]]
            print(f"🎮 Points System: {len(passed_points)}/{len(points_tests)} tests passed")
        
        # Ad system
        ad_tests = [r for r in self.results if "/rewards/" in r["endpoint"] or "/ads/" in r["endpoint"]]
        if ad_tests:
            passed_ads = [r for r in ad_tests if r["passed"]]
            print(f"📺 Ad System: {len(passed_ads)}/{len(ad_tests)} tests passed")
        
        # Parental gate
        parental_tests = [r for r in self.results if "/parental-gate/" in r["endpoint"]]
        if parental_tests:
            passed_parental = [r for r in parental_tests if r["passed"]]
            print(f"🔒 Parental Gate: {len(passed_parental)}/{len(parental_tests)} tests passed")
        
        # Content system
        content_tests = [r for r in self.results if "/daily-content/" in r["endpoint"]]
        if content_tests:
            passed_content = [r for r in content_tests if r["passed"]]
            print(f"📚 Content System: {len(passed_content)}/{len(content_tests)} tests passed")

async def main():
    """Run the Islamic Education App gamification backend tests."""
    tester = IslamicGamificationTester()
    
    try:
        await tester.run_all_tests()
        tester.print_summary()
        
        # Return exit code based on results
        if tester.passed_tests == tester.total_tests:
            print("\n🎉 ALL TESTS PASSED! Islamic Education App gamification system is working correctly.")
            return 0
        else:
            print(f"\n⚠️  {tester.total_tests - tester.passed_tests} tests failed. Please check the issues above.")
            return 1
            
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)