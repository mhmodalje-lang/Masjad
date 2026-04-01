#!/usr/bin/env python3
"""
Policy Compliance Backend API Testing
Testing all policy compliance endpoints after frontend-only changes
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL from review request
BACKEND_URL = "https://bug-fix-tools.preview.emergentagent.com"

def test_endpoint(method, url, expected_status=200, data=None, headers=None, expected_content_type=None):
    """Test a single endpoint and return results"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return {"success": False, "error": f"Unsupported method: {method}"}
        
        result = {
            "success": response.status_code == expected_status,
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "content_type": response.headers.get('content-type', ''),
            "content_length": len(response.text)
        }
        
        # Check content type if specified
        if expected_content_type and expected_content_type not in result["content_type"]:
            result["success"] = False
            result["error"] = f"Expected content-type {expected_content_type}, got {result['content_type']}"
        
        # Try to parse JSON response
        try:
            result["response_data"] = response.json()
        except:
            result["response_text"] = response.text[:200] + "..." if len(response.text) > 200 else response.text
        
        return result
    
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

def main():
    print("🧪 POLICY COMPLIANCE BACKEND API TESTING")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test cases from review request
    test_cases = [
        {
            "name": "Health Check",
            "method": "GET",
            "url": f"{BACKEND_URL}/api/health",
            "expected_status": 200,
            "description": "Should return 200 with healthy status"
        },
        {
            "name": "Privacy Page",
            "method": "GET", 
            "url": f"{BACKEND_URL}/privacy",
            "expected_status": 200,
            "description": "Frontend route should be accessible"
        },
        {
            "name": "Terms Page",
            "method": "GET",
            "url": f"{BACKEND_URL}/terms", 
            "expected_status": 200,
            "description": "Frontend route should be accessible"
        },
        {
            "name": "About Page",
            "method": "GET",
            "url": f"{BACKEND_URL}/about",
            "expected_status": 200,
            "description": "Frontend route should be accessible"
        },
        {
            "name": "Contact Page", 
            "method": "GET",
            "url": f"{BACKEND_URL}/contact",
            "expected_status": 200,
            "description": "Frontend route should be accessible"
        },
        {
            "name": "Delete Data Page",
            "method": "GET",
            "url": f"{BACKEND_URL}/delete-data",
            "expected_status": 200,
            "description": "Frontend route should be accessible"
        },
        {
            "name": "Content Policy Page",
            "method": "GET", 
            "url": f"{BACKEND_URL}/content-policy",
            "expected_status": 200,
            "description": "Frontend route should be accessible"
        },
        {
            "name": "App Ads TXT",
            "method": "GET",
            "url": f"{BACKEND_URL}/api/app-ads-txt",
            "expected_status": 200,
            "expected_content_type": "text/plain",
            "description": "Should return text/plain response"
        },
        {
            "name": "Delete Account (No Auth)",
            "method": "DELETE",
            "url": f"{BACKEND_URL}/api/auth/delete-account",
            "expected_status": 401,
            "description": "Should return 401 without auth"
        },
        {
            "name": "Report Content (No Auth)",
            "method": "POST",
            "url": f"{BACKEND_URL}/api/report",
            "expected_status": 401,
            "description": "Should return 401 without auth"
        },
        {
            "name": "Block User (No Auth)",
            "method": "POST", 
            "url": f"{BACKEND_URL}/api/block-user",
            "expected_status": 401,
            "description": "Should return 401 without auth"
        },
        {
            "name": "Data Deletion Request",
            "method": "POST",
            "url": f"{BACKEND_URL}/api/data-deletion-request",
            "data": {"email": "test@test.com", "reason": "test"},
            "expected_status": 200,
            "description": "Should return 200 with valid data"
        }
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i:2d}: {test_case['name']}")
        print(f"         {test_case['method']} {test_case['url']}")
        print(f"         {test_case['description']}")
        
        result = test_endpoint(
            method=test_case['method'],
            url=test_case['url'],
            expected_status=test_case['expected_status'],
            data=test_case.get('data'),
            expected_content_type=test_case.get('expected_content_type')
        )
        
        if result['success']:
            print(f"         ✅ PASS - Status: {result['status_code']}, Time: {result['response_time']:.3f}s")
            passed += 1
        else:
            print(f"         ❌ FAIL - Status: {result.get('status_code', 'N/A')}")
            if 'error' in result:
                print(f"         Error: {result['error']}")
            failed += 1
        
        # Add test case info to result
        result.update({
            'test_name': test_case['name'],
            'method': test_case['method'],
            'url': test_case['url'],
            'expected_status': test_case['expected_status'],
            'description': test_case['description']
        })
        
        results.append(result)
        print()
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print(f"Total Tests: {len(test_cases)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
    print()
    
    # Detailed results for failed tests
    failed_tests = [r for r in results if not r['success']]
    if failed_tests:
        print("🔍 FAILED TESTS DETAILS:")
        for test in failed_tests:
            error_msg = test.get('error', f"Expected {test['expected_status']}, got {test.get('status_code', 'N/A')}")
            print(f"- {test['test_name']}: {error_msg}") 
        print()
    
    # Save results to JSON
    with open('/app/policy_compliance_test_results.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'backend_url': BACKEND_URL,
            'total_tests': len(test_cases),
            'passed': passed,
            'failed': failed,
            'success_rate': passed/len(test_cases)*100,
            'results': results
        }, f, indent=2)
    
    print(f"📄 Detailed results saved to: /app/policy_compliance_test_results.json")
    
    # Return exit code based on results
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())