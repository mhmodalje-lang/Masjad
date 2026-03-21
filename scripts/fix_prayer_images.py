"""
SALAH PRAYER GUIDE V2 - CORRECTED Images Regeneration
Fixing 6 images with incorrect prayer positions
Using extremely specific prompts for accurate Islamic prayer positions
"""

import asyncio
import os
import io
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image

load_dotenv("/app/backend/.env")

from emergentintegrations.llm.openai.image_generation import OpenAIImageGeneration

API_KEY = os.environ.get("EMERGENT_LLM_KEY", "sk-emergent-eD2Be7d77B883287a7")
OUTPUT_DIR = Path("/app/frontend/public/assets/kids_zone/prayer_v2")

# ═══════════════════════════════════════════════════════════════
# CHARACTER LOCK V2 - More specific to ensure consistency
# ═══════════════════════════════════════════════════════════════
CHARACTER = (
    "A cute 7-year-old Muslim boy with warm brown skin, gentle dark brown eyes, "
    "soft round face with rosy cheeks, short black hair. "
    "He is wearing a pristine white Thobe (Islamic garment) that reaches his ankles "
    "and a white Kufi/prayer cap on his head. "
    "He is inside a beautiful grand mosque with golden warm ambient lighting, "
    "ornate Islamic geometric patterns and calligraphy on the walls, "
    "tall arched windows with soft sunlight streaming through creating volumetric light rays. "
    "Green prayer mat with golden Islamic geometric pattern on the floor. "
    "3D render in Pixar animation style, ultra high quality, photorealistic lighting, "
    "cinematic composition, warm spiritual atmosphere. "
)

# ═══════════════════════════════════════════════════════════════
# IMAGES TO REGENERATE - With EXTREMELY specific position prompts
# ═══════════════════════════════════════════════════════════════
IMAGES_TO_FIX = [
    {
        "filename": "prayer_step_2.webp",
        "title": "Step 2: Takbiratul Ihram (تكبيرة الإحرام)",
        "prompt": (
            f"{CHARACTER}"
            "CRITICAL POSITION REQUIREMENT: The boy is STANDING UPRIGHT on his feet (NOT sitting, NOT kneeling). "
            "His full body is visible from head to feet. He is standing tall and straight. "
            "His legs are straight and he is on his feet on the prayer mat. "
            "HAND POSITION: Both of his hands are raised UP to his EAR level. "
            "His palms are OPEN and facing FORWARD. His fingers are slightly spread apart. "
            "His elbows are bent as his hands reach ear height. "
            "His eyes are gently closed and his mouth is slightly open saying 'Allahu Akbar'. "
            "CAMERA: Full body shot from the front, showing him standing on the prayer mat with hands raised to ears. "
            "The image must clearly show: standing position, feet on ground, full height visible, hands at ear level."
        ),
    },
    {
        "filename": "prayer_step_3.webp",
        "title": "Step 3: Standing Qiyam (القيام والقراءة)",
        "prompt": (
            f"{CHARACTER}"
            "CRITICAL POSITION REQUIREMENT: The boy is STANDING UPRIGHT on his feet (NOT sitting, NOT kneeling). "
            "His full body is visible from head to feet. He is standing tall and straight on the prayer mat. "
            "His legs are straight, feet together on the prayer mat. "
            "HAND POSITION: His RIGHT hand is placed flat OVER his LEFT hand, both resting on his CHEST/upper stomach area. "
            "The right hand grips the left wrist gently. Both hands are clearly visible on his chest area. "
            "His eyes are gently closed, looking DOWN toward the prayer mat. "
            "He has a serene, contemplative expression as he recites the Quran. "
            "CAMERA: Full body shot from a three-quarter front angle, clearly showing him STANDING with hands folded on chest. "
            "The image must clearly show: standing upright on feet, hands clasped on chest, full body visible."
        ),
    },
    {
        "filename": "prayer_step_4.webp",
        "title": "Step 4: Ruku - Bowing (الركوع)",
        "prompt": (
            f"{CHARACTER}"
            "CRITICAL POSITION REQUIREMENT: The boy is performing RUKU (bowing) - this is NOT sujud/prostration. "
            "He is bending forward at the WAIST only. His legs remain STRAIGHT and VERTICAL. "
            "His back is perfectly FLAT and HORIZONTAL like a TABLE or a board - parallel to the ground. "
            "His head is aligned with his back (not hanging down, not looking up). "
            "HAND POSITION: Both of his hands are placed firmly on his KNEES (not on the floor, not on his shins). "
            "His fingers are spread and gripping his kneecaps. His palms are on his knees. "
            "His arms are straight from shoulders to knees. "
            "CAMERA: Clear SIDE PROFILE view showing: straight vertical legs, horizontal flat back at 90 degrees, hands on knees. "
            "The image must clearly show: bent at waist, back flat like a table, hands gripping knees, legs straight."
        ),
    },
    {
        "filename": "prayer_step_6.webp",
        "title": "Step 6: Sujud - Prostration (السجود)",
        "prompt": (
            f"{CHARACTER}"
            "CRITICAL POSITION: The boy is in SUJUD (prostration) on the prayer mat. "
            "His FOREHEAD and NOSE are touching the ground/prayer mat. "
            "HAND POSITION: Both PALMS are flat on the ground BESIDE his head (not under his face). "
            "His palms are at the level of his ears/shoulders on the mat, fingers together pointing toward Qibla. "
            "ARMS: His upper arms and elbows are RAISED OFF THE GROUND - NOT resting on the floor. "
            "There is visible space between his elbows and the ground. His arms form a triangle shape. "
            "HIPS: His hips/bottom are RAISED UP HIGH in the air, higher than his head. "
            "KNEES: Both knees are on the ground on the prayer mat. "
            "FEET: The toes of both feet are CURLED and pressing against the ground, pointing toward Qibla. "
            "CAMERA: Side view clearly showing: forehead on ground, hips raised high, arms off ground, palms flat beside head. "
            "The image must clearly show all 7 body parts: forehead+nose, 2 palms, 2 knees, 2 sets of toes on ground."
        ),
    },
    {
        "filename": "prayer_step_7.webp",
        "title": "Step 7: Sitting Between Prostrations (الجلسة بين السجدتين)",
        "prompt": (
            f"{CHARACTER}"
            "CRITICAL POSITION: The boy is SITTING on the prayer mat between two prostrations. "
            "SITTING POSITION (Iftirash): He is sitting on his LEFT foot which is flat/spread beneath him. "
            "His RIGHT foot is UPRIGHT with toes curled and touching the ground, pointing toward Qibla. "
            "His back and torso are STRAIGHT and UPRIGHT while sitting. "
            "HAND POSITION: Both hands are placed flat on his THIGHS near his knees, palms facing DOWN. "
            "His fingers are spread naturally on his thighs. "
            "EYES: His eyes are gently CLOSED or looking DOWN at his hands/lap. NOT looking at the camera. "
            "He has a peaceful, humble expression. "
            "CAMERA: Front three-quarter view showing him sitting upright, hands on thighs, eyes down. "
            "The image must clearly show: sitting upright, hands flat on thighs, eyes looking down, feet position."
        ),
    },
    {
        "filename": "prayer_step_8.webp",
        "title": "Step 8: Second Sujud (السجدة الثانية)",
        "prompt": (
            f"{CHARACTER}"
            "CRITICAL POSITION: The boy is in SUJUD (prostration) - this is the SECOND prostration. "
            "His FOREHEAD and NOSE are firmly touching the prayer mat/ground. "
            "HAND POSITION: Both PALMS are flat on the ground beside his head at ear/shoulder level. "
            "His fingers are together pointing toward Qibla direction. "
            "ARMS: His upper arms and elbows are clearly LIFTED OFF the ground. "
            "There is visible daylight/space between his elbows and the mat. "
            "HIPS: His hips/bottom are raised HIGH up in the air. "
            "KNEES: Both knees are on the prayer mat. "
            "FEET: Toes are curled and pressing the ground. "
            "CAMERA: Slightly elevated three-quarter view from above and to the side. "
            "Beautiful golden mosque light rays streaming from the window behind him. "
            "The image must clearly show: raised elbows off ground, raised hips, forehead on mat, palms beside head."
        ),
    },
]


async def regenerate_images():
    print("=" * 60)
    print("🕌 SALAH PRAYER GUIDE V2 - CORRECTING 6 IMAGES")
    print(f"   Output: {OUTPUT_DIR}")
    print(f"   Images to fix: {len(IMAGES_TO_FIX)}")
    print("=" * 60)
    
    image_gen = OpenAIImageGeneration(api_key=API_KEY)
    
    results = {"success": [], "failed": []}
    
    for i, img_data in enumerate(IMAGES_TO_FIX):
        filename = img_data["filename"]
        output_path = OUTPUT_DIR / filename
        
        # Backup old image
        if output_path.exists():
            backup_path = output_path.with_suffix('.old.webp')
            os.rename(str(output_path), str(backup_path))
            print(f"\n  📦 Backed up old {filename}")
        
        print(f"\n  🎨 [{i+1}/{len(IMAGES_TO_FIX)}] Generating: {img_data['title']}...")
        
        try:
            images = await image_gen.generate_images(
                prompt=img_data["prompt"],
                model="gpt-image-1",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                image_bytes = images[0]
                img = Image.open(io.BytesIO(image_bytes))
                img.save(str(output_path), "WEBP", quality=92)
                file_size = output_path.stat().st_size
                print(f"  ✅ Saved: {filename} ({file_size:,} bytes, {img.size[0]}x{img.size[1]})")
                results["success"].append(filename)
                
                # Remove backup
                backup_path = output_path.with_suffix('.old.webp')
                if backup_path.exists():
                    os.remove(str(backup_path))
            else:
                print(f"  ❌ No image returned for {filename}")
                results["failed"].append(filename)
                # Restore backup
                backup_path = output_path.with_suffix('.old.webp')
                if backup_path.exists():
                    os.rename(str(backup_path), str(output_path))
                    
        except Exception as e:
            print(f"  ❌ Error for {filename}: {str(e)}")
            results["failed"].append(filename)
            # Restore backup
            backup_path = output_path.with_suffix('.old.webp')
            if backup_path.exists():
                os.rename(str(backup_path), str(output_path))
        
        # Delay between generations
        if i < len(IMAGES_TO_FIX) - 1:
            await asyncio.sleep(3)
    
    print("\n" + "=" * 60)
    print(f"✅ Fixed: {len(results['success'])}/{len(IMAGES_TO_FIX)}")
    if results["failed"]:
        print(f"❌ Failed: {results['failed']}")
    else:
        print("🎉 ALL 6 CORRECTED IMAGES GENERATED SUCCESSFULLY!")
    print("=" * 60)
    
    # List all files
    print("\n📁 All prayer images:")
    for f in sorted(OUTPUT_DIR.iterdir()):
        if f.is_file() and f.suffix == '.webp' and '.old' not in f.name:
            print(f"   {f.name} ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    asyncio.run(regenerate_images())
