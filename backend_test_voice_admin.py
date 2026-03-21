#!/usr/bin/env python3
"""
Backend Test Suite - Voice Search & Admin Testing
Testing new endpoints: voice-search, admin/stats, admin/contacts, donations/list
"""
import requests
import json
import sys
from datetime import datetime

# Backend URL from frontend .env
BACKEND_URL = "https://kids-platform-review.preview.emergentagent.com/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log(message, color=Colors.WHITE):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] {message}{Colors.END}")

def test_endpoint(method, url, headers=None, json_data=None, expected_status=200, description=""):
    """Test a single endpoint and return response data"""
    log(f"🔄 {method} {url} - {description}", Colors.CYAN)
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=json_data, timeout=30)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=json_data, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            log(f"❌ Unsupported method: {method}", Colors.RED)
            return None
        
        if response.status_code == expected_status:
            log(f"✅ {description} - Status: {response.status_code}", Colors.GREEN)
            try:
                return response.json()
            except:
                return {"status": "success", "text": response.text}
        else:
            log(f"❌ {description} - Expected: {expected_status}, Got: {response.status_code}", Colors.RED)
            try:
                error_data = response.json()
                log(f"   Error: {error_data}", Colors.RED)
            except:
                log(f"   Error: {response.text}", Colors.RED)
            return None
            
    except requests.exceptions.Timeout:
        log(f"⏱️ {description} - Request timed out", Colors.YELLOW)
        return None
    except requests.exceptions.ConnectionError:
        log(f"🔌 {description} - Connection error", Colors.RED)
        return None
    except Exception as e:
        log(f"💥 {description} - Exception: {str(e)}", Colors.RED)
        return None

def main():
    log("🚀 VOICE SEARCH & ADMIN TESTING: New Backend API Endpoints", Colors.BOLD)
    log("Testing: voice-search, admin/stats, admin/contacts, donations/list", Colors.CYAN)
    log("="*80, Colors.BLUE)
    
    # Store test tokens
    user_token = None
    admin_token = None
    
    # ==================== TEST 1: Register Regular User ====================
    log("\n📝 Test 1: User Registration for Voice Search", Colors.BOLD)
    register_data = {
        "name": "تست", 
        "email": "voicetest@test.com", 
        "password": "test123"
    }
    
    response = test_endpoint(
        "POST", 
        f"{BACKEND_URL}/auth/register",
        json_data=register_data,
        description="Register user for voice search"
    )
    
    if response and "access_token" in response:
        user_token = response["access_token"]
        log(f"✅ User auth token obtained: {user_token[:20]}...", Colors.GREEN)
    else:
        # Try login if registration failed (user might already exist)
        log("Registration failed - trying login...", Colors.YELLOW)
        login_data = {
            "email": "voicetest@test.com",
            "password": "test123"
        }
        
        login_response = test_endpoint(
            "POST",
            f"{BACKEND_URL}/auth/login",
            json_data=login_data,
            description="Login existing user"
        )
        
        if login_response and "access_token" in login_response:
            user_token = login_response["access_token"]
            log(f"✅ User auth token obtained from login: {user_token[:20]}...", Colors.GREEN)
        else:
            log("❌ Failed to get user auth token - continuing with admin tests", Colors.RED)
    
    # ==================== TEST 2: Voice Search API ====================
    if user_token:
        log("\n🎤 Test 2: POST /api/stories/voice-search", Colors.BOLD)
        headers = {"Authorization": f"Bearer {user_token}"}
        voice_search_data = {
            "query": "أريد قصة عن الاستغفار والتوبة"
        }
        
        response = test_endpoint(
            "POST",
            f"{BACKEND_URL}/stories/voice-search",
            headers=headers,
            json_data=voice_search_data,
            description="AI-powered voice search"
        )
        
        if response:
            log("✅ Voice search endpoint working", Colors.GREEN)
            
            # Check expected fields
            if "stories" in response:
                stories = response["stories"]
                log(f"   ✅ Found {len(stories)} stories", Colors.GREEN)
                
                # Check story structure
                if len(stories) > 0:
                    story = stories[0]
                    expected_fields = ["id", "title", "content", "category", "likes_count", "comments_count"]
                    for field in expected_fields:
                        if field in story:
                            log(f"      ✅ Story has {field}: {story[field] if field != 'content' else '...'}", Colors.CYAN)
                        else:
                            log(f"      ❌ Story missing {field}", Colors.RED)
                else:
                    log("   ℹ️ No stories found for this query", Colors.CYAN)
            else:
                log("   ❌ Missing 'stories' field in response", Colors.RED)
            
            if "ai_response" in response:
                ai_response = response["ai_response"]
                log(f"   ✅ AI response: {ai_response[:100]}..." if ai_response else "   ✅ AI response: (empty)", Colors.CYAN)
            else:
                log("   ❌ Missing 'ai_response' field", Colors.RED)
            
            if "keywords" in response:
                keywords = response["keywords"]
                log(f"   ✅ Keywords: {keywords}", Colors.CYAN)
            else:
                log("   ❌ Missing 'keywords' field", Colors.RED)
        else:
            log("❌ Voice search failed", Colors.RED)
    
    # ==================== TEST 3: Admin Login ====================
    log("\n👑 Test 3: Admin Login", Colors.BOLD)
    
    # Try first admin email
    admin_login_data = {
        "email": "mhmd321324t@gmail.com", 
        "password": "123456"
    }
    
    response = test_endpoint(
        "POST",
        f"{BACKEND_URL}/auth/login",
        json_data=admin_login_data,
        description="Login admin user (mhmd321324t@gmail.com)"
    )
    
    if response and "access_token" in response:
        admin_token = response["access_token"]
        log(f"✅ Admin auth token obtained: {admin_token[:20]}...", Colors.GREEN)
    else:
        # Try registering with second admin email
        log("First admin login failed - trying second admin registration...", Colors.YELLOW)
        admin_register_data = {
            "name": "Admin", 
            "email": "mohammedalrejab@gmail.com", 
            "password": "admin123"
        }
        
        register_response = test_endpoint(
            "POST",
            f"{BACKEND_URL}/auth/register",
            json_data=admin_register_data,
            description="Register admin user (mohammedalrejab@gmail.com)"
        )
        
        if register_response and "access_token" in register_response:
            admin_token = register_response["access_token"]
            log(f"✅ Admin auth token obtained from registration: {admin_token[:20]}...", Colors.GREEN)
        else:
            # Try login with second admin email
            log("Admin registration failed - trying login...", Colors.YELLOW)
            admin_login_data2 = {
                "email": "mohammedalrejab@gmail.com", 
                "password": "admin123"
            }
            
            login_response = test_endpoint(
                "POST",
                f"{BACKEND_URL}/auth/login",
                json_data=admin_login_data2,
                description="Login admin user (mohammedalrejab@gmail.com)"
            )
            
            if login_response and "access_token" in login_response:
                admin_token = login_response["access_token"]
                log(f"✅ Admin auth token obtained from login: {admin_token[:20]}...", Colors.GREEN)
            else:
                log("❌ Failed to get admin auth token - admin tests will fail", Colors.RED)
    
    # ==================== TEST 4: Admin Stats API ====================
    if admin_token:
        log("\n📊 Test 4: GET /api/admin/stats", Colors.BOLD)
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        response = test_endpoint(
            "GET",
            f"{BACKEND_URL}/admin/stats",
            headers=headers,
            description="Admin statistics with categories"
        )
        
        if response:
            log("✅ Admin stats endpoint working", Colors.GREEN)
            
            # Check expected fields
            expected_fields = ["total_users", "total_stories", "total_posts", "total_donations", "total_contacts", "categories"]
            for field in expected_fields:
                if field in response:
                    if field == "categories":
                        categories = response[field]
                        log(f"   ✅ {field}: {len(categories)} categories", Colors.GREEN)
                        if len(categories) > 0:
                            log(f"      Sample categories: {[c.get('category') for c in categories[:3]]}", Colors.CYAN)
                    else:
                        log(f"   ✅ {field}: {response[field]}", Colors.GREEN)
                else:
                    log(f"   ❌ Missing field: {field}", Colors.RED)
        else:
            log("❌ Admin stats failed", Colors.RED)
    
    # ==================== TEST 5: Admin Contacts API ====================
    if admin_token:
        log("\n📧 Test 5: GET /api/admin/contacts", Colors.BOLD)
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        response = test_endpoint(
            "GET",
            f"{BACKEND_URL}/admin/contacts",
            headers=headers,
            description="Admin contact messages"
        )
        
        if response:
            log("✅ Admin contacts endpoint working", Colors.GREEN)
            
            # Check expected structure
            if "contacts" in response:
                contacts = response["contacts"]
                log(f"   ✅ Found {len(contacts)} contact messages", Colors.GREEN)
                
                if len(contacts) > 0:
                    contact = contacts[0]
                    expected_fields = ["name", "email", "message", "created_at"]
                    for field in expected_fields:
                        if field in contact:
                            log(f"      ✅ Contact has {field}", Colors.CYAN)
                        else:
                            log(f"      ❌ Contact missing {field}", Colors.YELLOW)
                else:
                    log("   ℹ️ No contact messages found", Colors.CYAN)
            else:
                log("   ❌ Missing 'contacts' field in response", Colors.RED)
        else:
            log("❌ Admin contacts failed", Colors.RED)
    
    # ==================== TEST 6: Donations List API (No Auth) ====================
    log("\n💰 Test 6: GET /api/donations/list", Colors.BOLD)
    
    response = test_endpoint(
        "GET",
        f"{BACKEND_URL}/donations/list",
        description="Donations list (no auth required)"
    )
    
    if response:
        log("✅ Donations list endpoint working", Colors.GREEN)
        
        # Check expected structure
        if "donations" in response:
            donations = response["donations"]
            log(f"   ✅ Found {len(donations)} donations", Colors.GREEN)
            
            if len(donations) > 0:
                donation = donations[0]
                expected_fields = ["id", "title", "description", "author_name", "created_at", "active"]
                for field in expected_fields:
                    if field in donation:
                        log(f"      ✅ Donation has {field}: {donation[field] if field != 'description' else '...'}", Colors.CYAN)
                    else:
                        log(f"      ❌ Donation missing {field}", Colors.YELLOW)
            else:
                log("   ℹ️ No donations found", Colors.CYAN)
        else:
            log("   ❌ Missing 'donations' field in response", Colors.RED)
    else:
        log("❌ Donations list failed", Colors.RED)
    
    # ==================== SUMMARY ====================
    log("\n" + "="*80, Colors.BLUE)
    log("🏁 VOICE SEARCH & ADMIN TESTING COMPLETE", Colors.BOLD)
    log("="*80, Colors.BLUE)
    
    log(f"\n📊 Test Summary:", Colors.BOLD)
    
    # Summarize each test
    if user_token:
        log(f"   ✅ User authentication working", Colors.GREEN)
        log(f"   🎤 POST /api/stories/voice-search tested", Colors.CYAN)
    else:
        log(f"   ❌ User authentication failed", Colors.RED)
        log(f"   ❌ POST /api/stories/voice-search not tested", Colors.RED)
    
    if admin_token:
        log(f"   ✅ Admin authentication working", Colors.GREEN)
        log(f"   📊 GET /api/admin/stats tested", Colors.CYAN)
        log(f"   📧 GET /api/admin/contacts tested", Colors.CYAN)
    else:
        log(f"   ❌ Admin authentication failed", Colors.RED)
        log(f"   ❌ GET /api/admin/stats not tested", Colors.RED)
        log(f"   ❌ GET /api/admin/contacts not tested", Colors.RED)
    
    log(f"   💰 GET /api/donations/list tested (no auth)", Colors.CYAN)
    
    log(f"\n🎯 All 4 new endpoints tested!", Colors.GREEN)

if __name__ == "__main__":
    main()