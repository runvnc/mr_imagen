import asyncio
import os
from google import genai
from google.genai import types
from nanoid import generate
from lib.providers.services import service
from lib.providers.commands import command
from PIL import Image
from io import BytesIO
from .core import generate_image, save_image

def random_img_fname():
    return generate() + ".png"

@service()
async def select_image_model(context=None, model_id=None, local=False, uncensored=False):
    # Hardcoded model selection for Imagen
    return {
        'id': 'imagen-3',
        'name': 'Imagen 3.0',
        'provider': 'Google',
        'model_id': 'imagen-3.0-generate-002'
    }

@service()
async def text_to_image(prompt, model_id=None, from_huggingface=None,
                      count=1, context=None, save_to=None, w=1024, h=1024, steps=30, cfg=7.5):
    print("text_to_image: Generating image with Imagen")
    script_location = os.path.dirname(os.path.realpath(__file__))
    
    try:
        model = await select_image_model(context)
        print(f"Using model: {model['name']}")
        
        for n in range(1, count+1):
            image_bytes = await generate_image(prompt, w, h, steps, cfg)
            if image_bytes:
                fname = f"/static/imgs/{random_img_fname()}"
                full_path = f"{script_location}{fname}"
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                if await save_image(image_bytes, full_path):
                    abs_path = os.path.realpath(full_path)
                    print("abs_path", abs_path)
                    return abs_path
            else:
                print("No image generated or error in result")
        return None
    except Exception as e:
        print(f"Error in text_to_image: {e}")
        return None

@command()
async def image(description="", context=None, w=1024, h=1024, steps=30, cfg=7.5):
    """image: Generate an image from a prompt

    # Example:

    [
      { "image": {"description": "A cute tabby cat in the forest"} },
      { "image": {"description": "A happy golden retriever in the park", "w": 1024, "h": 1024} }
    ]

    # Example:

    [
      { "image": {"description": "A christmas gift wrapped in a red bow.", "steps": 30, "cfg": 7.5} }
    ]

    """
    prompt = description
    print(f"Generating image for prompt: {prompt}")
    fname = await text_to_image(prompt, context=context, w=w, h=h, steps=steps, cfg=cfg)
    if fname:
        print(f"Image output to file: {fname}")
        # Strip everything before 'mr_imagen' for relative URL
        rel_url = "/" + fname[fname.rindex('mr_imagen'):]
        print("rel_url", rel_url)
        await context.insert_image(rel_url)
        return f"Image generated at {rel_url} and inserted into chat UI"
    else:
        print("Failed to generate image")

if __name__ == "__main__":
    print("Testing image generation")
    asyncio.run(text_to_image("A beautiful mountain landscape at sunset", count=1))
    print("Done testing image generation")
