from google import genai
from google.genai import types
import sys
import os
from PIL import Image
from io import BytesIO

# read prompt from first command line argument (if provided)
# or use default prompt
prompt = sys.argv[1] if len(sys.argv) > 1 else "A beautiful mountain landscape at sunset"
count = int(sys.argv[2]) if len(sys.argv) > 2 else 1

print(f"Prompt: {prompt}")
print(f"Count: {count}")

def generate_image(prompt):
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    
    print("Sending request to Google Imagen...")
    response = client.models.generate_images(
        model='imagen-3.0-generate-002',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            width=1024,
            height=1024
        )
    )

    if response and response.generated_images:
        return response.generated_images[0].image.image_bytes
    return None

# Generate and display images
for i in range(count):
    try:
        image_bytes = generate_image(prompt)
        if image_bytes:
            # Save image to temporary file
            temp_path = f"temp_image_{i}.png"
            image = Image.open(BytesIO(image_bytes))
            image.save(temp_path)
            
            # Open image with system viewer
            if sys.platform == "darwin":  # macOS
                os.system(f"open {temp_path}")
            elif sys.platform == "linux":  # Linux
                os.system(f"xdg-open {temp_path}")
            elif sys.platform == "win32":  # Windows
                os.system(f"start {temp_path}")
                
            print(f"Generated image saved to {temp_path}")
    except Exception as e:
        print(f"Error generating image {i+1}: {e}")
