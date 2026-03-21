#!/usr/bin/env python3
"""
Kids Zone Islamic Content Backend Testing - Updated
Testing all Kids Zone Islamic content endpoints for proper content and emoji validation
"""

import requests
import json
import time
from typing import Dict, List, Any

# Backend URL from frontend/.env
BACKEND_URL = "https://day-night-design.preview.emergentagent.com"

class KidsZoneIslamicContentTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_result(self, test_name: str, status: str, response_time: float, details: str = ""):
        """Log test result"""
        self.results.append({
            "test": test_name,
            "status": status,
            "response_time": f"{response_time:.3f}s",
            "details": details
        })
        self.total_tests += 1
        if status == "PASSED":
            self.passed_tests += 1
            
    def test_endpoint(self, endpoint: str, expected_status: int = 200) -> Dict[str, Any]:
        """Test a single endpoint"""
        url = f"{BACKEND_URL}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code != expected_status:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "error": f"Expected {expected_status}, got {response.status_code}"
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
                    "error": "Invalid JSON response"
                }
                
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return {
                "success": False,
                "status_code": 0,
                "response_time": response_time,
                "error": str(e)
            }
    
    def check_no_christian_prayer_emoji(self, data: Any, endpoint: str) -> List[str]:
        """Check for 🙏 emoji (Christian prayer) in response data"""
        issues = []
        data_str = json.dumps(data, ensure_ascii=False)
        if "🙏" in data_str:
            issues.append(f"Found 🙏 (Christian prayer emoji) in {endpoint}")
        return issues
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        print("Testing health endpoint...")
        result = self.test_endpoint("/api/health")
        
        if not result["success"]:
            self.log_result("Health Check", "FAILED", result["response_time"], result["error"])
            return
            
        data = result["data"]
        if data.get("status") == "healthy":
            self.log_result("Health Check", "PASSED", result["response_time"], "Health check successful")
        else:
            self.log_result("Health Check", "FAILED", result["response_time"], f"Unexpected health status: {data}")
    
    def test_salah_endpoint(self):
        """Test Salah endpoint with Arabic locale"""
        print("Testing Salah endpoint (Arabic)...")
        result = self.test_endpoint("/api/kids-learn/salah?locale=ar")
        
        if not result["success"]:
            self.log_result("Salah (Arabic)", "FAILED", result["response_time"], result["error"])
            return
            
        data = result["data"]
        issues = []
        
        # Check for success field
        if not data.get("success"):
            issues.append("Response missing success=true")
            
        # Check for 11 steps
        steps = data.get("steps", [])
        if len(steps) != 11:
            issues.append(f"Expected 11 steps, got {len(steps)}")
        
        # Check required fields for each step
        required_fields = ["image_url", "position", "dhikr_ar", "dhikr_transliteration", "body_position"]
        for i, step in enumerate(steps):
            for field in required_fields:
                if field not in step:
                    issues.append(f"Step {i+1} missing field: {field}")
        
        # Check for Christian prayer emoji
        emoji_issues = self.check_no_christian_prayer_emoji(data, "Salah Arabic")
        issues.extend(emoji_issues)
        
        if issues:
            self.log_result("Salah (Arabic)", "FAILED", result["response_time"], "; ".join(issues))
        else:
            self.log_result("Salah (Arabic)", "PASSED", result["response_time"], f"11 steps with all required fields")
    
    def test_wudu_arabic_endpoint(self):
        """Test Wudu endpoint with Arabic locale"""
        print("Testing Wudu endpoint (Arabic)...")
        result = self.test_endpoint("/api/kids-learn/wudu?locale=ar")
        
        if not result["success"]:
            self.log_result("Wudu (Arabic)", "FAILED", result["response_time"], result["error"])
            return
            
        data = result["data"]
        issues = []
        
        # Check for success field
        if not data.get("success"):
            issues.append("Response missing success=true")
            
        # Check for 12 steps
        steps = data.get("steps", [])
        if len(steps) != 12:
            issues.append(f"Expected 12 steps, got {len(steps)}")
        
        # Check step 1 for Bismillah mention
        if steps and len(steps) > 0:
            step1_text = json.dumps(steps[0], ensure_ascii=False)
            if "النية والتسمية" not in step1_text and "البسملة" not in step1_text:
                issues.append("Step 1 should mention النية والتسمية (Bismillah)")
        
        # Check for Christian prayer emoji
        emoji_issues = self.check_no_christian_prayer_emoji(data, "Wudu Arabic")
        issues.extend(emoji_issues)
        
        if issues:
            self.log_result("Wudu (Arabic)", "FAILED", result["response_time"], "; ".join(issues))
        else:
            self.log_result("Wudu (Arabic)", "PASSED", result["response_time"], f"12 steps with Bismillah in step 1, no 🙏 emoji")
    
    def test_wudu_english_endpoint(self):
        """Test Wudu endpoint with English locale"""
        print("Testing Wudu endpoint (English)...")
        result = self.test_endpoint("/api/kids-learn/wudu?locale=en")
        
        if not result["success"]:
            self.log_result("Wudu (English)", "FAILED", result["response_time"], result["error"])
            return
            
        data = result["data"]
        issues = []
        
        # Check for success field
        if not data.get("success"):
            issues.append("Response missing success=true")
            
        # Check for 12 steps
        steps = data.get("steps", [])
        if len(steps) != 12:
            issues.append(f"Expected 12 steps, got {len(steps)}")
        
        # Check step 1 for Bismillah mention
        if steps and len(steps) > 0:
            step1_text = json.dumps(steps[0], ensure_ascii=False)
            if "Intention & Bismillah" not in step1_text and "Bismillah" not in step1_text:
                issues.append("Step 1 should be 'Intention & Bismillah'")
        
        # Check for Christian prayer emoji
        emoji_issues = self.check_no_christian_prayer_emoji(data, "Wudu English")
        issues.extend(emoji_issues)
        
        if issues:
            self.log_result("Wudu (English)", "FAILED", result["response_time"], "; ".join(issues))
        else:
            self.log_result("Wudu (English)", "PASSED", result["response_time"], f"12 steps with Bismillah in step 1, no 🙏 emoji")
    
    def test_islamic_pillars_arabic_endpoint(self):
        """Test Islamic Pillars endpoint with Arabic locale"""
        print("Testing Islamic Pillars endpoint (Arabic)...")
        result = self.test_endpoint("/api/kids-learn/islamic-pillars?locale=ar")
        
        if not result["success"]:
            self.log_result("Islamic Pillars (Arabic)", "FAILED", result["response_time"], result["error"])
            return
            
        data = result["data"]
        issues = []
        
        # Check for success field
        if not data.get("success"):
            issues.append("Response missing success=true")
            
        # Check for 5 pillars
        pillars = data.get("pillars", [])
        if len(pillars) != 5:
            issues.append(f"Expected 5 pillars, got {len(pillars)}")
        
        # Check Salah pillar has 🕌 emoji NOT 🙏
        salah_pillar = None
        for pillar in pillars:
            pillar_text = json.dumps(pillar, ensure_ascii=False)
            if "صلاة" in pillar_text or "الصلاة" in pillar_text:
                salah_pillar = pillar
                break
        
        if salah_pillar:
            salah_text = json.dumps(salah_pillar, ensure_ascii=False)
            if "🕌" not in salah_text:
                issues.append("Salah pillar should have 🕌 emoji")
            if "🙏" in salah_text:
                issues.append("Salah pillar should NOT have 🙏 emoji (Christian prayer)")
        
        # Check for Christian prayer emoji in entire response
        emoji_issues = self.check_no_christian_prayer_emoji(data, "Islamic Pillars Arabic")
        issues.extend(emoji_issues)
        
        if issues:
            self.log_result("Islamic Pillars (Arabic)", "FAILED", result["response_time"], "; ".join(issues))
        else:
            self.log_result("Islamic Pillars (Arabic)", "PASSED", result["response_time"], f"5 pillars, Salah has 🕌 emoji, no 🙏 emoji")
    
    def test_islamic_pillars_english_endpoint(self):
        """Test Islamic Pillars endpoint with English locale"""
        print("Testing Islamic Pillars endpoint (English)...")
        result = self.test_endpoint("/api/kids-learn/islamic-pillars?locale=en")
        
        if not result["success"]:
            self.log_result("Islamic Pillars (English)", "FAILED", result["response_time"], result["error"])
            return
            
        data = result["data"]
        issues = []
        
        # Check for success field
        if not data.get("success"):
            issues.append("Response missing success=true")
            
        # Check for 5 pillars
        pillars = data.get("pillars", [])
        if len(pillars) != 5:
            issues.append(f"Expected 5 pillars, got {len(pillars)}")
        
        # Check for Christian prayer emoji
        emoji_issues = self.check_no_christian_prayer_emoji(data, "Islamic Pillars English")
        issues.extend(emoji_issues)
        
        if issues:
            self.log_result("Islamic Pillars (English)", "FAILED", result["response_time"], "; ".join(issues))
        else:
            self.log_result("Islamic Pillars (English)", "PASSED", result["response_time"], f"5 pillars, no 🙏 emoji")
    
    def test_prophets_arabic_endpoint(self):
        """Test Prophets endpoint with Arabic locale - UPDATED to use correct endpoint"""
        print("Testing Prophets endpoint (Arabic) - checking both endpoints...")
        
        # First test the original endpoint that returns 6 prophets
        result_6 = self.test_endpoint("/api/kids-learn/prophets?locale=ar")
        
        # Then test the full endpoint that returns 25 prophets
        result_25 = self.test_endpoint("/api/kids-learn/prophets-full?locale=ar")
        
        if not result_25["success"]:
            self.log_result("Prophets (Arabic)", "FAILED", result_25["response_time"], result_25["error"])
            return
            
        data = result_25["data"]
        issues = []
        
        # Check for success field
        if not data.get("success"):
            issues.append("Response missing success=true")
            
        # Check for 25 prophets
        prophets = data.get("prophets", [])
        if len(prophets) != 25:
            issues.append(f"Expected 25 prophets, got {len(prophets)}")
        
        # Check Zakariya has 🤲 emoji NOT 🙏
        zakariya_prophet = None
        for prophet in prophets:
            prophet_text = json.dumps(prophet, ensure_ascii=False)
            if "زكريا" in prophet_text or "Zakariya" in prophet_text:
                zakariya_prophet = prophet
                break
        
        if zakariya_prophet:
            zakariya_text = json.dumps(zakariya_prophet, ensure_ascii=False)
            if "🤲" not in zakariya_text:
                issues.append("Zakariya should have 🤲 emoji")
            if "🙏" in zakariya_text:
                issues.append("Zakariya should NOT have 🙏 emoji (Christian prayer)")
        
        # Check for Christian prayer emoji in entire response
        emoji_issues = self.check_no_christian_prayer_emoji(data, "Prophets Arabic")
        issues.extend(emoji_issues)
        
        # Note about endpoint discrepancy
        if result_6["success"]:
            data_6 = result_6["data"]
            prophets_6 = data_6.get("prophets", [])
            issues.append(f"NOTE: /api/kids-learn/prophets returns {len(prophets_6)} prophets, but /api/kids-learn/prophets-full returns {len(prophets)} prophets")
        
        if issues:
            self.log_result("Prophets (Arabic)", "FAILED", result_25["response_time"], "; ".join(issues))
        else:
            self.log_result("Prophets (Arabic)", "PASSED", result_25["response_time"], f"25 prophets, Zakariya has 🤲 emoji, no 🙏 emoji")
    
    def run_all_tests(self):
        """Run all Kids Zone Islamic content tests"""
        print("=" * 80)
        print("KIDS ZONE ISLAMIC CONTENT BACKEND TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print()
        
        # Run all tests
        self.test_health_endpoint()
        self.test_salah_endpoint()
        self.test_wudu_arabic_endpoint()
        self.test_wudu_english_endpoint()
        self.test_islamic_pillars_arabic_endpoint()
        self.test_islamic_pillars_english_endpoint()
        self.test_prophets_arabic_endpoint()
        
        # Print results
        print("\n" + "=" * 80)
        print("TEST RESULTS SUMMARY")
        print("=" * 80)
        
        for result in self.results:
            status_symbol = "✅" if result["status"] == "PASSED" else "❌"
            print(f"{status_symbol} {result['test']} - {result['status']} ({result['response_time']})")
            if result["details"]:
                print(f"   Details: {result['details']}")
        
        print(f"\nTotal Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        # Critical issues summary
        failed_tests = [r for r in self.results if r["status"] == "FAILED"]
        if failed_tests:
            print("\n" + "=" * 80)
            print("CRITICAL ISSUES FOUND:")
            print("=" * 80)
            for test in failed_tests:
                print(f"❌ {test['test']}: {test['details']}")
        else:
            print("\n✅ ALL TESTS PASSED - No critical issues found")

if __name__ == "__main__":
    tester = KidsZoneIslamicContentTester()
    tester.run_all_tests()