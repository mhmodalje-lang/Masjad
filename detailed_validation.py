#!/usr/bin/env python3
"""
Detailed Salah API Validation - Verify all requirements from review request
"""

import requests
import json

BACKEND_URL = "https://quran-authentic-1.preview.emergentagent.com"

def detailed_validation():
    print("=" * 70)
    print("DETAILED SALAH API VALIDATION")
    print("=" * 70)
    
    # Test Arabic endpoint
    print("\n1. Testing Arabic endpoint...")
    ar_response = requests.get(f"{BACKEND_URL}/api/kids-learn/salah?locale=ar")
    ar_data = ar_response.json()
    
    print(f"   Status Code: {ar_response.status_code}")
    print(f"   Steps Count: {len(ar_data['steps'])}")
    
    # Test English endpoint
    print("\n2. Testing English endpoint...")
    en_response = requests.get(f"{BACKEND_URL}/api/kids-learn/salah?locale=en")
    en_data = en_response.json()
    
    print(f"   Status Code: {en_response.status_code}")
    print(f"   Steps Count: {len(en_data['steps'])}")
    
    # Validate field structure for both
    print("\n3. Validating field structure...")
    required_fields = ['step', 'position', 'title', 'description', 'dhikr_ar', 'dhikr_transliteration', 'body_position']
    
    for locale, data in [('Arabic', ar_data), ('English', en_data)]:
        print(f"\n   {locale} endpoint:")
        for i, step in enumerate(data['steps'], 1):
            missing_fields = [field for field in required_fields if field not in step]
            if missing_fields:
                print(f"     Step {i}: Missing fields: {missing_fields}")
            else:
                print(f"     Step {i}: ✅ All required fields present")
    
    # Validate position values
    print("\n4. Validating position values...")
    expected_positions = [
        'qiyam_niyyah', 'takbir', 'qiyam_qiraa', 'qiyam_fatiha', 
        'ruku', 'itidal', 'sujud_1', 'juloos', 'sujud_2', 'tashahhud', 'tasleem'
    ]
    
    ar_positions = [step['position'] for step in ar_data['steps']]
    en_positions = [step['position'] for step in en_data['steps']]
    
    print(f"   Arabic positions: {ar_positions}")
    print(f"   English positions: {en_positions}")
    print(f"   Expected positions: {expected_positions}")
    
    if ar_positions == expected_positions and en_positions == expected_positions:
        print("   ✅ Position values match expected sequence")
    else:
        print("   ❌ Position values don't match expected sequence")
    
    # Validate language content
    print("\n5. Validating language-specific content...")
    
    # Check Arabic content
    ar_step_2 = ar_data['steps'][1]  # Takbir step
    has_arabic_title = any('\u0600' <= char <= '\u06FF' for char in ar_step_2['title'])
    has_arabic_desc = any('\u0600' <= char <= '\u06FF' for char in ar_step_2['description'])
    
    print(f"   Arabic endpoint - Title has Arabic: {has_arabic_title}")
    print(f"   Arabic endpoint - Description has Arabic: {has_arabic_desc}")
    
    # Check English content
    en_step_2 = en_data['steps'][1]  # Takbir step
    has_arabic_title_en = any('\u0600' <= char <= '\u06FF' for char in en_step_2['title'])
    has_arabic_desc_en = any('\u0600' <= char <= '\u06FF' for char in en_step_2['description'])
    
    print(f"   English endpoint - Title has Arabic: {has_arabic_title_en}")
    print(f"   English endpoint - Description has Arabic: {has_arabic_desc_en}")
    
    # Sample data display
    print("\n6. Sample step data:")
    print(f"\n   Arabic Step 2 (Takbir):")
    print(f"     Title: {ar_step_2['title']}")
    print(f"     Position: {ar_step_2['position']}")
    print(f"     Dhikr: {ar_step_2['dhikr_ar']}")
    print(f"     Transliteration: {ar_step_2['dhikr_transliteration']}")
    
    print(f"\n   English Step 2 (Takbir):")
    print(f"     Title: {en_step_2['title']}")
    print(f"     Position: {en_step_2['position']}")
    print(f"     Dhikr: {en_step_2['dhikr_ar']}")
    print(f"     Transliteration: {en_step_2['dhikr_transliteration']}")
    
    # Health check
    print("\n7. Testing health endpoint...")
    health_response = requests.get(f"{BACKEND_URL}/api/health")
    health_data = health_response.json()
    
    print(f"   Status Code: {health_response.status_code}")
    print(f"   Health Status: {health_data.get('status', 'unknown')}")
    
    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    detailed_validation()