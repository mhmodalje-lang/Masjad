"""
SALAH PRAYER GUIDE - 4K 3D Image Generation
Generates 10 high-definition 3D renders of "Noor" performing prayer steps
Using OpenAI gpt-image-1 via Emergent LLM Key
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv("/app/backend/.env")

from emergentintegrations.llm.openai.image_generation import OpenAIImageGeneration

API_KEY = os.environ.get("EMERGENT_LLM_KEY", "sk-emergent-eD2Be7d77B883287a7")
OUTPUT_DIR = Path("/app/frontend/public/assets/kids_zone/prayer_v2")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# CHARACTER LOCK - Consistent visual identity for "Noor"
# ═══════════════════════════════════════════════════════════════
CHARACTER_SEED = (
    "A respectful 7-year-old Muslim boy named Noor, "
    "with warm brown skin, gentle dark brown eyes, soft round face with rosy cheeks, "
    "wearing a pristine white Thobe (جلابية) that reaches his ankles, "
    "and a white prayer cap (طاقية) on his head. "
    "He is inside a beautiful mosque with warm golden lighting, "
    "ornate Islamic geometric patterns on the walls, "
    "arched windows with soft sunlight streaming through, "
    "a green prayer mat with intricate Islamic design beneath him. "
)

STYLE_DIRECTIVE = (
    "3D render in Pixar/Unreal Engine 5 style, "
    "photorealistic lighting with spiritual warm golden ambient light, "
    "volumetric light rays from mosque windows, "
    "ultra high detail, cinematic composition, "
    "4K resolution quality, depth of field, "
    "respectful and educational Islamic illustration. "
    "The character must look exactly the same in every image - same face, same clothing, same proportions."
)

# ═══════════════════════════════════════════════════════════════
# 10 PRAYER STEPS - Detailed position prompts
# ═══════════════════════════════════════════════════════════════
PRAYER_STEPS = [
    {
        "step": 1,
        "filename": "prayer_step_1.webp",
        "title": "النية والقيام - Standing & Intention",
        "prompt": (
            f"{CHARACTER_SEED}"
            "Noor is standing perfectly upright on his green prayer mat, facing forward (toward the Qibla). "
            "His feet are shoulder-width apart, his arms are relaxed at his sides, "
            "and his eyes are looking downward at the spot where he will prostrate. "
            "He has a calm, focused, and reverent expression. "
            "The mosque interior is visible behind him with beautiful arched doorways. "
            "Camera angle: front-facing, slightly low angle to show his full body. "
            f"{STYLE_DIRECTIVE}"
        ),
    },
    {
        "step": 2,
        "filename": "prayer_step_2.webp",
        "title": "تكبيرة الإحرام - Takbiratul Ihram",
        "prompt": (
            f"{CHARACTER_SEED}"
            "Noor is raising both hands up to his ear level with his palms open and facing forward (toward the Qibla), "
            "fingers are slightly spread and naturally relaxed. "
            "His mouth is slightly open as he says 'Allahu Akbar'. "
            "His eyes are looking down respectfully. "
            "Camera angle: front view, upper body emphasis, showing hands clearly raised to ears. "
            f"{STYLE_DIRECTIVE}"
        ),
    },
    {
        "step": 3,
        "filename": "prayer_step_3.webp",
        "title": "القيام والقراءة - Standing & Recitation",
        "prompt": (
            f"{CHARACTER_SEED}"
            "Noor is standing upright with his right hand placed over his left hand on his chest, "
            "holding them together at chest level. "
            "His eyes are looking down at the prayer mat where he will prostrate. "
            "He has a peaceful, contemplative expression as he recites Surah Al-Fatiha. "
            "A subtle golden glow around him suggests spiritual recitation. "
            "Camera angle: three-quarter front view showing the hand placement on chest clearly. "
            f"{STYLE_DIRECTIVE}"
        ),
    },
    {
        "step": 4,
        "filename": "prayer_step_4.webp",
        "title": "الركوع - Bowing (Ruku')",
        "prompt": (
            f"{CHARACTER_SEED}"
            "Noor is bowing at the waist with his back perfectly straight and flat like a table (90-degree angle). "
            "His hands are placed firmly on his knees with fingers spread. "
            "His head is aligned with his back (not looking up or hanging down). "
            "His legs are straight and firm. "
            "Camera angle: side profile view clearly showing the flat back position and hand placement on knees. "
            f"{STYLE_DIRECTIVE}"
        ),
    },
    {
        "step": 5,
        "filename": "prayer_step_5.webp",
        "title": "الاعتدال من الركوع - Rising from Ruku'",
        "prompt": (
            f"{CHARACTER_SEED}"
            "Noor is rising from the bowing position, standing upright with his arms relaxed at his sides. "
            "He is in the brief standing position between bowing and prostration. "
            "His body is completely straight and upright. "
            "His eyes are looking down humbly. "
            "Camera angle: front-facing view showing full standing posture. "
            f"{STYLE_DIRECTIVE}"
        ),
    },
    {
        "step": 6,
        "filename": "prayer_step_6.webp",
        "title": "السجود - Prostration (Sujud)",
        "prompt": (
            f"{CHARACTER_SEED}"
            "Noor is in the prostration (sujud) position on his prayer mat. "
            "His forehead and nose are touching the ground, "
            "both palms are flat on the ground beside his head with fingers together pointing toward Qibla, "
            "both knees are on the ground, and the toes of both feet are curled and touching the ground. "
            "His arms are slightly raised off the ground (not flat like a dog). "
            "His back is slightly elevated. "
            "Camera angle: side view clearly showing all 7 body parts touching the ground. "
            f"{STYLE_DIRECTIVE}"
        ),
    },
    {
        "step": 7,
        "filename": "prayer_step_7.webp",
        "title": "الجلسة بين السجدتين - Sitting Between Prostrations",
        "prompt": (
            f"{CHARACTER_SEED}"
            "Noor is sitting on his left foot (which is spread beneath him), "
            "with his right foot upright (toes pointing toward Qibla). "
            "His hands are placed on his thighs near his knees with palms down. "
            "His back is straight and upright while sitting. "
            "His expression is humble and focused. "
            "Camera angle: front three-quarter view showing the sitting position clearly. "
            f"{STYLE_DIRECTIVE}"
        ),
    },
    {
        "step": 8,
        "filename": "prayer_step_8.webp",
        "title": "السجدة الثانية - Second Prostration",
        "prompt": (
            f"{CHARACTER_SEED}"
            "Noor is performing the second prostration (sujud) on his prayer mat, identical to the first. "
            "His forehead and nose are touching the ground, "
            "palms flat on the ground beside his head, knees on the ground, toes curled and touching the ground. "
            "The golden mosque light creates a spiritual atmosphere. "
            "A subtle '2' indicator or second-time feeling. "
            "Camera angle: slightly elevated angle from the side, showing the full prostration. "
            f"{STYLE_DIRECTIVE}"
        ),
    },
    {
        "step": 9,
        "filename": "prayer_step_9.webp",
        "title": "التشهد - Tashahhud",
        "prompt": (
            f"{CHARACTER_SEED}"
            "Noor is sitting for the Tashahhud (testimony of faith). "
            "He is sitting on his left foot with his right foot upright. "
            "His left hand is placed flat on his left thigh. "
            "His right hand is on his right thigh with his index finger raised and pointing forward, "
            "while the other fingers are curled into a loose fist. "
            "The raised index finger is clearly visible and prominent. "
            "His lips are moving as he recites the Tashahhud. "
            "Camera angle: front view slightly from the right to clearly show the raised index finger. "
            f"{STYLE_DIRECTIVE}"
        ),
    },
    {
        "step": 10,
        "filename": "prayer_step_10.webp",
        "title": "التسليم - Tasleem (Ending the Prayer)",
        "prompt": (
            f"{CHARACTER_SEED}"
            "Noor is performing the Tasleem to end the prayer. "
            "He is sitting and turning his head to the right side, "
            "with a gentle, peaceful smile on his face. "
            "His hands are on his thighs. "
            "Golden light creates a beautiful spiritual atmosphere. "
            "An arrow or visual indicator showing the head turning to the right. "
            "Camera angle: front view showing Noor turning his head to his right. "
            f"{STYLE_DIRECTIVE}"
        ),
    },
]


async def generate_single_image(image_gen, step_data, retry=0):
    """Generate a single prayer step image with retries."""
    step_num = step_data["step"]
    filename = step_data["filename"]
    output_path = OUTPUT_DIR / filename
    
    # Skip if already generated
    if output_path.exists() and output_path.stat().st_size > 10000:
        print(f"  ✅ Step {step_num} already exists ({output_path.stat().st_size} bytes), skipping...")
        return True
    
    print(f"  🎨 Generating Step {step_num}: {step_data['title']}...")
    
    try:
        images = await image_gen.generate_images(
            prompt=step_data["prompt"],
            model="gpt-image-1",
            number_of_images=1
        )
        
        if images and len(images) > 0:
            image_bytes = images[0]
            
            # Save as webp
            try:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(image_bytes))
                img.save(str(output_path), "WEBP", quality=90)
                file_size = output_path.stat().st_size
                print(f"  ✅ Step {step_num} saved: {filename} ({file_size:,} bytes, {img.size[0]}x{img.size[1]})")
                return True
            except ImportError:
                # Fallback: save as PNG then note for conversion
                png_path = output_path.with_suffix('.png')
                with open(png_path, "wb") as f:
                    f.write(image_bytes)
                print(f"  ⚠️ Step {step_num} saved as PNG (PIL not available for WEBP conversion)")
                return True
        else:
            print(f"  ❌ Step {step_num}: No image returned")
            if retry < 2:
                print(f"  🔄 Retrying step {step_num} (attempt {retry + 2})...")
                return await generate_single_image(image_gen, step_data, retry + 1)
            return False
            
    except Exception as e:
        print(f"  ❌ Step {step_num} error: {str(e)}")
        if retry < 2:
            print(f"  🔄 Retrying step {step_num} (attempt {retry + 2})...")
            await asyncio.sleep(3)
            return await generate_single_image(image_gen, step_data, retry + 1)
        return False


async def main():
    print("=" * 60)
    print("🕌 SALAH PRAYER GUIDE - 4K 3D Image Generation")
    print(f"   Output: {OUTPUT_DIR}")
    print(f"   Model: gpt-image-1")
    print(f"   Steps: {len(PRAYER_STEPS)}")
    print("=" * 60)
    
    image_gen = OpenAIImageGeneration(api_key=API_KEY)
    
    results = {"success": [], "failed": []}
    
    for step_data in PRAYER_STEPS:
        success = await generate_single_image(image_gen, step_data)
        if success:
            results["success"].append(step_data["step"])
        else:
            results["failed"].append(step_data["step"])
        
        # Brief delay between generations
        if step_data["step"] < len(PRAYER_STEPS):
            await asyncio.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"✅ Success: {len(results['success'])}/{len(PRAYER_STEPS)}")
    if results["failed"]:
        print(f"❌ Failed: Steps {results['failed']}")
    else:
        print("🎉 ALL 10 IMAGES GENERATED SUCCESSFULLY!")
    print("=" * 60)
    
    # List generated files
    print("\n📁 Generated files:")
    for f in sorted(OUTPUT_DIR.iterdir()):
        if f.is_file():
            print(f"   {f.name} ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    asyncio.run(main())
