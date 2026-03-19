#!/usr/bin/env python3
"""
Social Media Platform (Sohba) API Testing for أذان وحكاية
Tests all NEW social media endpoints as specified in the review request.
"""

import asyncio
import httpx
import json
import sys
import time
from datetime import datetime

# Load frontend .env to get the backend URL
BACKEND_URL = None
try:
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                BACKEND_URL = line.split('=', 1)[1].strip().rstrip('/') + '/api'
                break
except FileNotFoundError:
    BACKEND_URL = "http://localhost:8001/api"

if not BACKEND_URL:
    BACKEND_URL = "http://localhost:8001/api"

print(f"Using backend URL: {BACKEND_URL}")

class TestResults:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.critical_issues = []
    
    def add_pass(self, endpoint, details=""):
        self.passed.append(f"✅ {endpoint}: {details}")
    
    def add_fail(self, endpoint, error, critical=False):
        failure_msg = f"❌ {endpoint}: {error}"
        self.failed.append(failure_msg)
        if critical:
            self.critical_issues.append(failure_msg)
    
    def print_summary(self):
        print("\n" + "="*80)
        print("🔍 SOCIAL MEDIA PLATFORM (SOHBA) API TEST RESULTS")
        print("="*80)
        
        if self.passed:
            print(f"\n✅ PASSED ({len(self.passed)}/13 endpoints):")
            for result in self.passed:
                print(f"   {result}")
        
        if self.failed:
            print(f"\n❌ FAILED ({len(self.failed)}/13 endpoints):")
            for result in self.failed:
                print(f"   {result}")
        
        if self.critical_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.critical_issues)} found):")
            for issue in self.critical_issues:
                print(f"   {issue}")
        
        print(f"\n📊 OVERALL RESULT: {len(self.passed)}/13 endpoints working ({len(self.passed)/13*100:.1f}% success rate)")
        
        if len(self.failed) == 0:
            print("🎉 ALL SOCIAL MEDIA ENDPOINTS PASSING! Platform is fully functional.")
        else:
            print(f"⚠️  {len(self.failed)} endpoints need attention.")
        
        print("="*80)

async def test_endpoint(client, endpoint, method="GET", data=None, headers=None, expected_status=200, validation_func=None):
    """Generic endpoint testing function"""
    url = f"{BACKEND_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = await client.get(url, headers=headers or {})
        elif method == "POST":
            response = await client.post(url, json=data, headers=headers or {})
        elif method == "DELETE":
            response = await client.delete(url, headers=headers or {})
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        # Check status code
        if response.status_code != expected_status:
            return False, f"Expected status {expected_status}, got {response.status_code}. Response: {response.text[:200]}"
        
        # Parse JSON response
        try:
            json_data = response.json()
        except Exception as e:
            if expected_status == 200:
                return False, f"Invalid JSON response: {str(e)}. Response text: {response.text[:100]}"
            else:
                # For non-200 responses, return the raw text
                return True, response.text
        
        # Custom validation
        if validation_func:
            is_valid, error = validation_func(json_data)
            if not is_valid:
                return False, error
        
        return True, json_data
    
    except Exception as e:
        return False, f"Request failed: {str(e)}"

async def main():
    results = TestResults()
    
    print("🚀 Starting social media platform (Sohba) API testing...")
    print(f"📡 Testing against: {BACKEND_URL}")
    
    # Store variables for use across tests
    auth_token = None
    post_id = None
    comment_id = None
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # 1. Register a test user
        print("\n1. Testing user registration...")
        unique_email = f"test_social_{int(time.time())}@test.com"
        register_data = {
            "email": unique_email,
            "password": "test123456",
            "name": "مستخدم تجربة"
        }
        success, data = await test_endpoint(
            client, "/auth/register", method="POST", data=register_data,
            validation_func=lambda d: (
                (True, "") if "access_token" in d and "user" in d
                else (False, "Missing access_token or user in response")
            )
        )
        if success:
            results.add_pass("POST /api/auth/register", f"User registered successfully: {register_data['name']}")
            auth_token = data.get("access_token")
        else:
            results.add_fail("POST /api/auth/register", data, critical=True)
        
        # 2. Login with JSON format (as per existing API)
        print("\n2. Testing user login...")
        login_data = {
            "email": unique_email,
            "password": "test123456"
        }
        success, data = await test_endpoint(
            client, "/auth/login", method="POST", data=login_data,
            validation_func=lambda d: (
                (True, "") if "access_token" in d
                else (False, "Missing access_token in response")
            )
        )
        if success:
            results.add_pass("POST /api/auth/login", "Login successful, returns access_token")
            auth_token = data.get("access_token")  # Update token
        else:
            results.add_fail("POST /api/auth/login", data, critical=True)
        
        # Set up auth headers for subsequent requests
        auth_headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
        
        # 3. Get recommended users
        print("\n3. Testing recommended users...")
        success, data = await test_endpoint(
            client, "/sohba/recommended-users?limit=5",
            validation_func=lambda d: (
                (True, f"Found {len(d.get('users', []))} recommended users")
                if "users" in d and isinstance(d["users"], list)
                else (False, "Missing or invalid users list")
            )
        )
        if success:
            users_count = len(data.get("users", []))
            results.add_pass("GET /api/sohba/recommended-users", f"Returns {users_count} recommended users")
        else:
            results.add_fail("GET /api/sohba/recommended-users", data)
        
        # 4. Create a post
        print("\n4. Testing post creation...")
        post_data = {
            "content": "بسم الله الرحمن الرحيم - منشور تجربة",
            "category": "general",
            "content_type": "text"
        }
        success, data = await test_endpoint(
            client, "/sohba/posts", method="POST", data=post_data, headers=auth_headers,
            validation_func=lambda d: (
                (True, "") if "post" in d and "id" in d["post"]
                else (False, "Missing post or post.id in response")
            )
        )
        if success:
            post_id = data.get("post", {}).get("id")
            results.add_pass("POST /api/sohba/posts", f"Created post with ID: {post_id}")
        else:
            results.add_fail("POST /api/sohba/posts", data, critical=True)
        
        # 5. Get video feed
        print("\n5. Testing video feed...")
        success, data = await test_endpoint(
            client, "/sohba/feed/videos",
            validation_func=lambda d: (
                (True, f"Found {len(d.get('videos', d.get('posts', [])))} videos")
                if ("videos" in d or "posts" in d) and isinstance(d.get("videos", d.get("posts", [])), list)
                else (False, "Missing or invalid videos/posts list")
            )
        )
        if success:
            videos_count = len(data.get("videos", data.get("posts", [])))
            results.add_pass("GET /api/sohba/feed/videos", f"Returns {videos_count} video posts")
        else:
            results.add_fail("GET /api/sohba/feed/videos", data)
        
        # 6. Get following feed (requires auth)
        print("\n6. Testing following feed...")
        success, data = await test_endpoint(
            client, "/sohba/feed/following", headers=auth_headers,
            validation_func=lambda d: (
                (True, f"Found {len(d.get('posts', []))} posts from following")
                if "posts" in d and isinstance(d["posts"], list)
                else (False, "Missing or invalid posts list")
            )
        )
        if success:
            following_posts = len(data.get("posts", []))
            results.add_pass("GET /api/sohba/feed/following", f"Returns {following_posts} posts from followed users")
        else:
            results.add_fail("GET /api/sohba/feed/following", data)
        
        # 7. Like the created post
        print("\n7. Testing post like...")
        if post_id:
            success, data = await test_endpoint(
                client, f"/sohba/posts/{post_id}/like", method="POST", headers=auth_headers,
                validation_func=lambda d: (
                    (True, f"Like status: {d.get('liked', 'unknown')}")
                    if "liked" in d or "success" in d
                    else (False, "Missing like status in response")
                )
            )
            if success:
                like_status = data.get("liked", data.get("success", "liked"))
                results.add_pass("POST /api/sohba/posts/{id}/like", f"Post liked successfully: {like_status}")
            else:
                results.add_fail("POST /api/sohba/posts/{id}/like", data)
        else:
            results.add_fail("POST /api/sohba/posts/{id}/like", "No post_id available (previous test failed)")
        
        # 8. Add comment to the post
        print("\n8. Testing comment creation...")
        if post_id:
            comment_data = {
                "content": "تعليق تجربة"
            }
            success, data = await test_endpoint(
                client, f"/sohba/posts/{post_id}/comments", method="POST", 
                data=comment_data, headers=auth_headers,
                validation_func=lambda d: (
                    (True, "") if "comment" in d and "id" in d["comment"]
                    else (False, "Missing comment or comment.id in response")
                )
            )
            if success:
                comment_id = data.get("comment", {}).get("id")
                results.add_pass("POST /api/sohba/posts/{id}/comments", f"Created comment with ID: {comment_id}")
            else:
                results.add_fail("POST /api/sohba/posts/{id}/comments", data)
        else:
            results.add_fail("POST /api/sohba/posts/{id}/comments", "No post_id available (previous test failed)")
        
        # 9. Add reply to comment
        print("\n9. Testing comment reply...")
        if post_id and comment_id:
            reply_data = {
                "content": "رد على التعليق",
                "reply_to": comment_id
            }
            success, data = await test_endpoint(
                client, f"/sohba/posts/{post_id}/comments", method="POST", 
                data=reply_data, headers=auth_headers,
                validation_func=lambda d: (
                    (True, "") if "comment" in d and "id" in d["comment"]
                    else (False, "Missing comment or comment.id in reply response")
                )
            )
            if success:
                reply_id = data.get("comment", {}).get("id")
                results.add_pass("POST /api/sohba/posts/{id}/comments (reply)", f"Created reply with ID: {reply_id}")
            else:
                results.add_fail("POST /api/sohba/posts/{id}/comments (reply)", data)
        else:
            results.add_fail("POST /api/sohba/posts/{id}/comments (reply)", "No post_id or comment_id available")
        
        # 10. Delete a comment
        print("\n10. Testing comment deletion...")
        if comment_id:
            success, data = await test_endpoint(
                client, f"/sohba/comments/{comment_id}", method="DELETE", headers=auth_headers,
                validation_func=lambda d: (
                    (True, "Comment deleted") if "deleted" in d or "success" in d
                    else (False, "Missing delete confirmation")
                )
            )
            if success:
                results.add_pass("DELETE /api/sohba/comments/{id}", "Comment deleted successfully")
            else:
                results.add_fail("DELETE /api/sohba/comments/{id}", data)
        else:
            results.add_fail("DELETE /api/sohba/comments/{id}", "No comment_id available (previous test failed)")
        
        # 11. Share a post
        print("\n11. Testing post sharing...")
        if post_id:
            success, data = await test_endpoint(
                client, f"/sohba/posts/{post_id}/share", method="POST", headers=auth_headers,
                validation_func=lambda d: (
                    (True, "Post shared") if "shared" in d or "success" in d
                    else (False, "Missing share confirmation")
                )
            )
            if success:
                results.add_pass("POST /api/sohba/posts/{id}/share", "Post shared successfully")
            else:
                results.add_fail("POST /api/sohba/posts/{id}/share", data)
        else:
            results.add_fail("POST /api/sohba/posts/{id}/share", "No post_id available (previous test failed)")
        
        # 12. Get trending posts (explore)
        print("\n12. Testing explore/trending posts...")
        success, data = await test_endpoint(
            client, "/sohba/explore",
            validation_func=lambda d: (
                (True, f"Found {len(d.get('posts', []))} trending posts")
                if "posts" in d and isinstance(d["posts"], list)
                else (False, "Missing or invalid posts list in explore")
            )
        )
        if success:
            trending_count = len(data.get("posts", []))
            results.add_pass("GET /api/sohba/explore", f"Returns {trending_count} trending posts")
        else:
            results.add_fail("GET /api/sohba/explore", data)
        
        # 13. Test admin social stats (may require admin user)
        print("\n13. Testing admin social stats...")
        success, data = await test_endpoint(
            client, "/admin/social/stats", headers=auth_headers, expected_status=200,
            validation_func=lambda d: (
                (True, "Admin stats returned") if "stats" in d or "users" in d or "posts" in d
                else (False, "Missing stats data")
            )
        )
        if not success and "401" in str(data) or "403" in str(data):
            # This is expected for non-admin users
            results.add_pass("GET /api/admin/social/stats", "Admin endpoint properly protected (401/403 for non-admin)")
        elif success:
            results.add_pass("GET /api/admin/social/stats", "Admin stats accessible")
        else:
            results.add_fail("GET /api/admin/social/stats", data)
    
    # Print comprehensive results
    results.print_summary()
    
    # Return exit code
    return 0 if len(results.failed) == 0 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)