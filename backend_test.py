#!/usr/bin/env python3
"""
Comprehensive Backend Testing for AzanHikaya Multilingual Endpoints
==================================================================
Testing all multilingual backend endpoints with multiple locales:
ar, en, de, fr, tr, ru, sv, nl, el

Endpoints to test:
1. Asma Al-Husna (99 Names of Allah)
2. Gifts List
3. Payment Packages
4. Credit Packages
5. Localization Strings
6. Supported Localizations
7. Store Items
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://backend-localization.preview.emergentagent.com"

# Test locales
LOCALES = ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"]

class MultilingualBackendTester:
    def __init__(self):
        self.session = None
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def log_result(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            print(f"✅ {test_name}: {status}")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name}: {status}")
            if details:
                print(f"   Details: {details}")
        
        self.results.append({
            "test": test_name,
            "status": status,
            "details": details
        })

    async def test_endpoint(self, endpoint: str, expected_keys: List[str] = None, 
                          expected_count: int = None, test_name: str = "") -> Dict[str, Any]:
        """Test a single endpoint"""
        try:
            url = f"{BACKEND_URL}/api{endpoint}"
            async with self.session.get(url) as response:
                if response.status != 200:
                    self.log_result(test_name, f"FAIL - HTTP {response.status}")
                    return {"status": "fail", "error": f"HTTP {response.status}"}
                
                try:
                    data = await response.json()
                except json.JSONDecodeError as e:
                    self.log_result(test_name, f"FAIL - Invalid JSON: {str(e)}")
                    return {"status": "fail", "error": f"Invalid JSON: {str(e)}"}
                
                # Validate expected keys
                if expected_keys:
                    missing_keys = [key for key in expected_keys if key not in data]
                    if missing_keys:
                        self.log_result(test_name, f"FAIL - Missing keys: {missing_keys}")
                        return {"status": "fail", "error": f"Missing keys: {missing_keys}"}
                
                # Validate expected count
                if expected_count is not None:
                    if "names" in data and len(data["names"]) != expected_count:
                        self.log_result(test_name, f"FAIL - Expected {expected_count} items, got {len(data['names'])}")
                        return {"status": "fail", "error": f"Count mismatch"}
                    elif "gifts" in data and len(data["gifts"]) != expected_count:
                        self.log_result(test_name, f"FAIL - Expected {expected_count} gifts, got {len(data['gifts'])}")
                        return {"status": "fail", "error": f"Count mismatch"}
                
                self.log_result(test_name, "PASS")
                return {"status": "pass", "data": data}
                
        except Exception as e:
            self.log_result(test_name, f"FAIL - Exception: {str(e)}")
            return {"status": "fail", "error": str(e)}

    async def test_asma_al_husna(self):
        """Test Asma Al-Husna endpoints for all locales"""
        print("\n🔸 Testing Asma Al-Husna (99 Names of Allah)")
        print("=" * 60)
        
        for locale in LOCALES:
            endpoint = f"/asma-al-husna?locale={locale}"
            test_name = f"Asma Al-Husna ({locale})"
            
            result = await self.test_endpoint(
                endpoint, 
                expected_keys=["names", "total"],
                expected_count=99,
                test_name=test_name
            )
            
            if result["status"] == "pass":
                data = result["data"]
                # Verify total is 99
                if data.get("total") != 99:
                    self.log_result(f"{test_name} - Total Check", f"FAIL - Expected total=99, got {data.get('total')}")
                else:
                    # Verify each name has required fields
                    sample_name = data["names"][0] if data["names"] else {}
                    required_fields = ["num", "ar", "transliteration", "meaning"]
                    missing_fields = [field for field in required_fields if field not in sample_name]
                    
                    if missing_fields:
                        self.log_result(f"{test_name} - Structure Check", f"FAIL - Missing fields: {missing_fields}")
                    else:
                        # Check if Arabic text is present in non-Arabic locales (should not leak)
                        if locale != "ar" and isinstance(sample_name.get("meaning"), str):
                            # This is expected - meaning should be localized string
                            pass
                        self.log_result(f"{test_name} - Structure Check", "PASS")

    async def test_gifts_list(self):
        """Test Gifts List endpoints for multiple locales"""
        print("\n🔸 Testing Gifts List")
        print("=" * 60)
        
        test_locales = ["en", "de", "nl"]  # Test subset as specified in review
        
        for locale in test_locales:
            endpoint = f"/gifts/list?locale={locale}"
            test_name = f"Gifts List ({locale})"
            
            result = await self.test_endpoint(
                endpoint,
                expected_keys=["gifts"],
                test_name=test_name
            )
            
            if result["status"] == "pass":
                data = result["data"]
                gifts = data.get("gifts", [])
                
                if len(gifts) != 12:
                    self.log_result(f"{test_name} - Count Check", f"FAIL - Expected 12 gifts, got {len(gifts)}")
                else:
                    self.log_result(f"{test_name} - Count Check", "PASS")
                
                # Verify gift structure
                if gifts:
                    sample_gift = gifts[0]
                    required_fields = ["id", "name", "emoji", "price_credits", "description"]
                    missing_fields = [field for field in required_fields if field not in sample_gift]
                    
                    if missing_fields:
                        self.log_result(f"{test_name} - Structure Check", f"FAIL - Missing fields: {missing_fields}")
                    else:
                        self.log_result(f"{test_name} - Structure Check", "PASS")

    async def test_payment_packages(self):
        """Test Payment Packages endpoints for multiple locales"""
        print("\n🔸 Testing Payment Packages")
        print("=" * 60)
        
        test_locales = ["en", "fr", "ru"]  # Test subset as specified in review
        
        for locale in test_locales:
            endpoint = f"/payments/packages?locale={locale}"
            test_name = f"Payment Packages ({locale})"
            
            result = await self.test_endpoint(
                endpoint,
                expected_keys=["packages"],
                test_name=test_name
            )
            
            if result["status"] == "pass":
                data = result["data"]
                packages = data.get("packages", [])
                
                # Verify package structure
                if packages:
                    sample_package = packages[0]
                    if "name" not in sample_package:
                        self.log_result(f"{test_name} - Structure Check", "FAIL - Missing 'name' field")
                    else:
                        self.log_result(f"{test_name} - Structure Check", "PASS")

    async def test_credit_packages(self):
        """Test Credit Packages endpoints for multiple locales"""
        print("\n🔸 Testing Credit Packages")
        print("=" * 60)
        
        test_locales = ["en", "tr"]  # Test subset as specified in review
        
        for locale in test_locales:
            endpoint = f"/credits/packages?locale={locale}"
            test_name = f"Credit Packages ({locale})"
            
            result = await self.test_endpoint(
                endpoint,
                expected_keys=["packages"],
                test_name=test_name
            )
            
            if result["status"] == "pass":
                data = result["data"]
                packages = data.get("packages", [])
                
                # Verify package structure
                if packages:
                    sample_package = packages[0]
                    if "label" not in sample_package:
                        self.log_result(f"{test_name} - Structure Check", "FAIL - Missing 'label' field")
                    else:
                        self.log_result(f"{test_name} - Structure Check", "PASS")

    async def test_localization_strings(self):
        """Test Localization Strings endpoints for all 10 languages"""
        print("\n🔸 Testing Localization Strings (All 10 Languages)")
        print("=" * 60)
        
        for locale in LOCALES:
            endpoint = f"/localization/strings/{locale}"
            test_name = f"Localization Strings ({locale})"
            
            result = await self.test_endpoint(
                endpoint,
                expected_keys=["lang", "strings", "dir"],
                test_name=test_name
            )
            
            if result["status"] == "pass":
                data = result["data"]
                strings = data.get("strings", {})
                
                # Verify required UI string keys
                required_keys = ["home", "quran", "prayer_times", "settings"]
                missing_keys = [key for key in required_keys if key not in strings]
                
                if missing_keys:
                    self.log_result(f"{test_name} - Keys Check", f"FAIL - Missing keys: {missing_keys}")
                else:
                    self.log_result(f"{test_name} - Keys Check", "PASS")
                
                # Verify direction is correct
                expected_dir = "rtl" if locale == "ar" else "ltr"
                if data.get("dir") != expected_dir:
                    self.log_result(f"{test_name} - Direction Check", f"FAIL - Expected {expected_dir}, got {data.get('dir')}")
                else:
                    self.log_result(f"{test_name} - Direction Check", "PASS")

    async def test_supported_localizations(self):
        """Test Supported Localizations endpoint"""
        print("\n🔸 Testing Supported Localizations")
        print("=" * 60)
        
        endpoint = "/localization/supported"
        test_name = "Supported Localizations"
        
        result = await self.test_endpoint(
            endpoint,
            expected_keys=["ui_languages", "store_listing", "seo_keywords"],
            test_name=test_name
        )
        
        if result["status"] == "pass":
            data = result["data"]
            ui_languages = data.get("ui_languages", [])
            
            # Verify all 10 languages are present
            expected_codes = ["ar", "en", "de", "de-AT", "fr", "tr", "ru", "sv", "nl", "el"]
            actual_codes = [lang.get("code") for lang in ui_languages if isinstance(lang, dict)]
            
            missing_codes = [code for code in expected_codes if code not in actual_codes]
            if missing_codes:
                self.log_result(f"{test_name} - Languages Check", f"FAIL - Missing language codes: {missing_codes}")
            else:
                self.log_result(f"{test_name} - Languages Check", "PASS")
            
            # Verify store_listing has keys for all languages
            store_listing = data.get("store_listing", {})
            missing_store_keys = [code for code in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] if code not in store_listing]
            if missing_store_keys:
                self.log_result(f"{test_name} - Store Listing Check", f"FAIL - Missing store listing keys: {missing_store_keys}")
            else:
                self.log_result(f"{test_name} - Store Listing Check", "PASS")
            
            # Verify seo_keywords has keys for all languages
            seo_keywords = data.get("seo_keywords", {})
            missing_seo_keys = [code for code in ["ar", "en", "de", "fr", "tr", "ru", "sv", "nl", "el"] if code not in seo_keywords]
            if missing_seo_keys:
                self.log_result(f"{test_name} - SEO Keywords Check", f"FAIL - Missing SEO keyword keys: {missing_seo_keys}")
            else:
                self.log_result(f"{test_name} - SEO Keywords Check", "PASS")

    async def test_store_items(self):
        """Test Store Items endpoints for multiple locales"""
        print("\n🔸 Testing Store Items")
        print("=" * 60)
        
        test_locales = ["en", "de"]  # Test subset as specified in review
        
        for locale in test_locales:
            endpoint = f"/store/items?locale={locale}"
            test_name = f"Store Items ({locale})"
            
            result = await self.test_endpoint(
                endpoint,
                expected_keys=["items"],
                test_name=test_name
            )
            
            if result["status"] == "pass":
                data = result["data"]
                items = data.get("items", [])
                
                # Verify item structure
                if items:
                    sample_item = items[0]
                    required_fields = ["name", "description", "price_gold", "category"]
                    missing_fields = [field for field in required_fields if field not in sample_item]
                    
                    if missing_fields:
                        self.log_result(f"{test_name} - Structure Check", f"FAIL - Missing fields: {missing_fields}")
                    else:
                        self.log_result(f"{test_name} - Structure Check", "PASS")

    async def test_arabic_text_leakage(self):
        """Test that Arabic text doesn't leak into non-Arabic locale responses"""
        print("\n🔸 Testing Arabic Text Leakage Prevention")
        print("=" * 60)
        
        # Test a few non-Arabic locales for Arabic text leakage
        test_locales = ["en", "de", "fr"]
        
        for locale in test_locales:
            # Test Asma Al-Husna for Arabic leakage
            endpoint = f"/asma-al-husna?locale={locale}"
            test_name = f"Arabic Leakage Check - Asma Al-Husna ({locale})"
            
            result = await self.test_endpoint(endpoint, test_name=test_name)
            
            if result["status"] == "pass":
                data = result["data"]
                names = data.get("names", [])
                
                if names:
                    sample_name = names[0]
                    meaning = sample_name.get("meaning", "")
                    
                    # Check if meaning contains Arabic characters (basic check)
                    has_arabic = any('\u0600' <= char <= '\u06FF' for char in str(meaning))
                    
                    if has_arabic and locale != "ar":
                        self.log_result(f"{test_name} - Meaning Field", "FAIL - Arabic text found in non-Arabic locale")
                    else:
                        self.log_result(f"{test_name} - Meaning Field", "PASS")
                    
                    # The 'ar' field should always contain Arabic (this is expected)
                    ar_field = sample_name.get("ar", "")
                    has_arabic_in_ar = any('\u0600' <= char <= '\u06FF' for char in str(ar_field))
                    
                    if not has_arabic_in_ar:
                        self.log_result(f"{test_name} - AR Field", "FAIL - Arabic field should contain Arabic text")
                    else:
                        self.log_result(f"{test_name} - AR Field", "PASS")

    async def run_all_tests(self):
        """Run all multilingual backend tests"""
        print("🚀 Starting Comprehensive Multilingual Backend Testing")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Testing Locales: {', '.join(LOCALES)}")
        print("=" * 80)
        
        # Run all test suites
        await self.test_asma_al_husna()
        await self.test_gifts_list()
        await self.test_payment_packages()
        await self.test_credit_packages()
        await self.test_localization_strings()
        await self.test_supported_localizations()
        await self.test_store_items()
        await self.test_arabic_text_leakage()
        
        # Print summary
        print("\n" + "=" * 80)
        print("🏁 TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%" if self.total_tests > 0 else "0%")
        
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if result["status"] != "PASS":
                    print(f"  - {result['test']}: {result['status']}")
                    if result["details"]:
                        print(f"    {result['details']}")
        
        print("\n" + "=" * 80)
        return self.failed_tests == 0

async def main():
    """Main test runner"""
    async with MultilingualBackendTester() as tester:
        success = await tester.run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())