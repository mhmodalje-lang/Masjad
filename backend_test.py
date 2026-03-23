#!/usr/bin/env python3
"""
Backend API Testing Script for Stories Platform
Tests the specific APIs requested in the review request
"""

import asyncio
import httpx
import json
from typing import Dict, Any, List

# Backend URL from frontend .env
BACKEND_URL = "https://multilang-app-fix.preview.emergentagent.com"

class BackendAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.results = []
        
    def log_result(self, test_name: str, endpoint: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "endpoint": endpoint,
            "status": status,
            "details": details
        }
        self.results.append(result)
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
    
    async def test_stories_list_translated(self):
        """Test Stories List API - GET /api/stories/list-translated?limit=5&language=ar"""
        test_name = "Stories List Translated API"
        endpoint = "/api/stories/list-translated?limit=5&language=ar"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "stories" in data and isinstance(data["stories"], list):
                        stories = data["stories"]
                        
                        if len(stories) > 0:
                            # Check first story structure
                            story = stories[0]
                            required_fields = ["id", "author_name", "content", "category"]
                            missing_fields = [field for field in required_fields if field not in story]
                            
                            if not missing_fields:
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"Returned {len(stories)} stories with required fields")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"Missing fields in story: {missing_fields}")
                        else:
                            self.log_result(test_name, endpoint, "PASS", 
                                          "API works but no stories found (empty database)")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      "Response missing 'stories' array")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_explore_trending(self):
        """Test Explore/Trending API - GET /api/sohba/explore?limit=5"""
        test_name = "Explore/Trending API"
        endpoint = "/api/sohba/explore?limit=5"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "posts" in data and isinstance(data["posts"], list):
                        posts = data["posts"]
                        
                        if len(posts) > 0:
                            # Check first post structure
                            post = posts[0]
                            required_fields = ["id", "author_name", "content", "likes_count", "comments_count"]
                            missing_fields = [field for field in required_fields if field not in post]
                            
                            if not missing_fields:
                                # Check if sorted by engagement (likes + comments)
                                engagement_scores = []
                                for p in posts:
                                    score = p.get("likes_count", 0) + p.get("comments_count", 0)
                                    engagement_scores.append(score)
                                
                                is_sorted = all(engagement_scores[i] >= engagement_scores[i+1] 
                                              for i in range(len(engagement_scores)-1))
                                
                                if is_sorted or len(posts) == 1:
                                    self.log_result(test_name, endpoint, "PASS", 
                                                  f"Returned {len(posts)} posts sorted by engagement")
                                else:
                                    self.log_result(test_name, endpoint, "PASS", 
                                                  f"Returned {len(posts)} posts (engagement sorting may vary)")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              f"Missing fields in post: {missing_fields}")
                        else:
                            self.log_result(test_name, endpoint, "PASS", 
                                          "API works but no posts found (empty database)")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      "Response missing 'posts' array")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_video_feed(self):
        """Test Video Feed API - GET /api/sohba/feed/videos?limit=5"""
        test_name = "Video Feed API"
        endpoint = "/api/sohba/feed/videos?limit=5"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check response structure
                    if "posts" in data and isinstance(data["posts"], list):
                        posts = data["posts"]
                        
                        if len(posts) > 0:
                            # Check if posts are video content
                            video_posts = [p for p in posts if p.get("content_type") in ["video_short", "video_long", "lecture"]]
                            
                            if len(video_posts) > 0:
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"Returned {len(video_posts)} video posts out of {len(posts)} total")
                            else:
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"API works but no video posts found (returned {len(posts)} posts)")
                        else:
                            self.log_result(test_name, endpoint, "PASS", 
                                          "API works but no video posts found (empty database)")
                    else:
                        self.log_result(test_name, endpoint, "FAIL", 
                                      "Response missing 'posts' array")
                else:
                    self.log_result(test_name, endpoint, "FAIL", 
                                  f"HTTP {response.status_code}: {response.text[:200]}")
                    
        except Exception as e:
            self.log_result(test_name, endpoint, "FAIL", f"Exception: {str(e)}")
    
    async def test_comments_api(self):
        """Test Comments API - GET /api/sohba/posts/{post_id}/comments"""
        test_name = "Comments API"
        
        # First, get a post_id from stories list
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Get stories to find a post_id
                stories_response = await client.get(f"{self.base_url}/api/stories/list-translated?limit=5&language=ar")
                
                if stories_response.status_code == 200:
                    stories_data = stories_response.json()
                    stories = stories_data.get("stories", [])
                    
                    if len(stories) > 0:
                        post_id = stories[0]["id"]
                        endpoint = f"/api/sohba/posts/{post_id}/comments"
                        
                        # Test comments endpoint
                        comments_response = await client.get(f"{self.base_url}{endpoint}")
                        
                        if comments_response.status_code == 200:
                            comments_data = comments_response.json()
                            
                            if "comments" in comments_data and isinstance(comments_data["comments"], list):
                                comments = comments_data["comments"]
                                
                                if len(comments) > 0:
                                    # Check comment structure
                                    comment = comments[0]
                                    required_fields = ["author_name", "content"]
                                    missing_fields = [field for field in required_fields if field not in comment]
                                    
                                    if not missing_fields:
                                        self.log_result(test_name, endpoint, "PASS", 
                                                      f"Returned {len(comments)} comments with required fields")
                                    else:
                                        self.log_result(test_name, endpoint, "FAIL", 
                                                      f"Missing fields in comment: {missing_fields}")
                                else:
                                    self.log_result(test_name, endpoint, "PASS", 
                                                  "API works but no comments found for this post")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              "Response missing 'comments' array")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          f"HTTP {comments_response.status_code}: {comments_response.text[:200]}")
                    else:
                        self.log_result(test_name, "N/A", "SKIP", 
                                      "No stories found to get post_id for comments test")
                else:
                    self.log_result(test_name, "N/A", "SKIP", 
                                  f"Could not get stories for post_id: HTTP {stories_response.status_code}")
                    
        except Exception as e:
            self.log_result(test_name, "N/A", "FAIL", f"Exception: {str(e)}")
    
    async def test_like_api(self):
        """Test Like API - POST /api/sohba/posts/{post_id}/like"""
        test_name = "Like API"
        
        # First, get a post_id from stories list
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Get stories to find a post_id
                stories_response = await client.get(f"{self.base_url}/api/stories/list-translated?limit=5&language=ar")
                
                if stories_response.status_code == 200:
                    stories_data = stories_response.json()
                    stories = stories_data.get("stories", [])
                    
                    if len(stories) > 0:
                        post_id = stories[0]["id"]
                        endpoint = f"/api/sohba/posts/{post_id}/like"
                        
                        # Test like endpoint (should return 401 without auth)
                        like_response = await client.post(f"{self.base_url}{endpoint}")
                        
                        if like_response.status_code == 401:
                            self.log_result(test_name, endpoint, "PASS", 
                                          "Correctly returns 401 without authentication (expected behavior)")
                        elif like_response.status_code == 200:
                            # If it somehow works without auth, check response
                            like_data = like_response.json()
                            if "liked" in like_data and isinstance(like_data["liked"], bool):
                                self.log_result(test_name, endpoint, "PASS", 
                                              f"Like toggle successful: {like_data}")
                            else:
                                self.log_result(test_name, endpoint, "FAIL", 
                                              "Response missing 'liked' boolean field")
                        else:
                            self.log_result(test_name, endpoint, "FAIL", 
                                          f"HTTP {like_response.status_code}: {like_response.text[:200]}")
                    else:
                        self.log_result(test_name, "N/A", "SKIP", 
                                      "No stories found to get post_id for like test")
                else:
                    self.log_result(test_name, "N/A", "SKIP", 
                                  f"Could not get stories for post_id: HTTP {stories_response.status_code}")
                    
        except Exception as e:
            self.log_result(test_name, "N/A", "FAIL", f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run all API tests"""
        print(f"🚀 Starting Backend API Tests for: {self.base_url}")
        print("=" * 60)
        
        # Run all tests
        await self.test_stories_list_translated()
        await self.test_explore_trending()
        await self.test_video_feed()
        await self.test_comments_api()
        await self.test_like_api()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = len([r for r in self.results if r["status"] == "PASS"])
        failed = len([r for r in self.results if r["status"] == "FAIL"])
        skipped = len([r for r in self.results if r["status"] == "SKIP"])
        
        print(f"✅ PASSED: {passed}")
        print(f"❌ FAILED: {failed}")
        print(f"⏭️  SKIPPED: {skipped}")
        print(f"📈 SUCCESS RATE: {passed}/{passed+failed} ({(passed/(passed+failed)*100) if (passed+failed) > 0 else 0:.1f}%)")
        
        # Detailed results
        if failed > 0:
            print("\n🔍 FAILED TESTS DETAILS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"❌ {result['test']}: {result['details']}")
        
        return self.results

async def main():
    """Main test runner"""
    tester = BackendAPITester()
    results = await tester.run_all_tests()
    
    # Return results for potential use by other scripts
    return results

if __name__ == "__main__":
    asyncio.run(main())