import asyncio
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from nanoid import generate
from .imagesize import get_closest_image_size

def random_img_fname():
    """Generate a random filename for saving images.

    Returns:
        str: Random filename with .png extension
    """
    return generate() + ".png"

async def generate_image(prompt, w=1024, h=1024, steps=30, cfg=7.5):
    """Generate an image using Google's Imagen API.

    Args:
        prompt (str): The text description of the image to generate
        w (int): Desired width in pixels
        h (int): Desired height in pixels
        steps (int): Number of inference steps
        cfg (float): Guidance scale for image generation

    Returns:
        bytes: The generated image data
    """
    try:
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        # Get the closest supported image size
        width, height = get_closest_image_size(w, h)
        print(f"Using image size: {width}x{height}")

        client = genai.Client(api_key=api_key)
        # can't specify w,h, ignoring
        response = await asyncio.to_thread(
            client.models.generate_images,
            model= 'imagen-4.0-ultra-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1
            )
        )

        if response and response.generated_images:
            return response.generated_images[0].image.image_bytes
        else:
            print("No images generated")
            return None

    except Exception as e:
        print(f"Error in generate_image: {e}")
        return None

async def save_image(image_bytes, save_path):
    """Save image bytes to a file.

    Args:
        image_bytes (bytes): The image data to save
        save_path (str): Path where to save the image

    Returns:
        str: Path to the saved image file, or None if failed
    """
    try:
        image = Image.open(BytesIO(image_bytes))
        image.save(save_path)
        print(f"Image saved to {save_path}")
        return save_path
    except Exception as e:
        print(f"Error saving image: {e}")
        return None
