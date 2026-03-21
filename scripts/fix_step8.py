"""Fix Step 8 - Second Sujud with safety-filter-friendly prompt"""
import asyncio, os, io
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
load_dotenv("/app/backend/.env")
from emergentintegrations.llm.openai.image_generation import OpenAIImageGeneration

API_KEY = os.environ.get("EMERGENT_LLM_KEY")
OUTPUT_DIR = Path("/app/frontend/public/assets/kids_zone/prayer_v2")

async def main():
    image_gen = OpenAIImageGeneration(api_key=API_KEY)
    
    prompt = (
        "A cute 7-year-old Muslim boy with warm brown skin, gentle dark brown eyes, "
        "soft round face, wearing a pristine white Thobe and white Kufi prayer cap. "
        "He is inside a beautiful grand mosque with golden warm lighting and arched windows with sunlight rays. "
        "Green prayer mat with golden Islamic pattern. "
        "3D render in Pixar animation style, ultra high quality, cinematic warm lighting. "
        "POSITION: The boy is performing Islamic prayer prostration (sujud) on the prayer mat. "
        "He is kneeling with his forehead and nose gently touching the prayer mat. "
        "His open palms are placed flat on the mat beside his head at shoulder level. "
        "His upper arms are lifted away from the floor. "
        "His knees are on the mat and his body is in a bowing prostration position. "
        "His toes are curled touching the ground. "
        "CAMERA: Side view showing the full prostration from a respectful angle. "
        "Beautiful golden volumetric light rays from mosque windows illuminate the scene."
    )
    
    print("🎨 Generating Step 8 (Second Sujud)...")
    try:
        images = await image_gen.generate_images(prompt=prompt, model="gpt-image-1", number_of_images=1)
        if images and len(images) > 0:
            output_path = OUTPUT_DIR / "prayer_step_8.webp"
            img = Image.open(io.BytesIO(images[0]))
            img.save(str(output_path), "WEBP", quality=92)
            print(f"✅ Saved: prayer_step_8.webp ({output_path.stat().st_size:,} bytes, {img.size[0]}x{img.size[1]})")
        else:
            print("❌ No image returned")
    except Exception as e:
        print(f"❌ Error: {e}")

asyncio.run(main())
