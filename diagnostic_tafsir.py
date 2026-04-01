#!/usr/bin/env python3
"""
Quick diagnostic test to see what's in the tafsir field
"""

import asyncio
import aiohttp
import json

BACKEND_URL = "https://bug-fix-tools.preview.emergentagent.com"

async def check_tafsir_content():
    async with aiohttp.ClientSession() as session:
        # Check a few failing cases
        test_cases = [
            ("1", "1", "en"),
            ("2", "255", "en"),
            ("1", "1", "de"),
        ]
        
        for surah, ayah, lang in test_cases:
            url = f"{BACKEND_URL}/api/quran/v4/global-verse/{surah}/{ayah}?language={lang}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    tafsir = data.get("tafsir", "")
                    print(f"\n=== {surah}:{ayah} ({lang}) ===")
                    print(f"Tafsir length: {len(tafsir)}")
                    print(f"Tafsir preview: {tafsir[:200]}...")
                    has_arabic = any('\u0600' <= char <= '\u06FF' for char in tafsir)
                    print(f"Has Arabic: {has_arabic}")

if __name__ == "__main__":
    asyncio.run(check_tafsir_content())