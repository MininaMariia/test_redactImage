import os
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def test_api_connection():
    key = os.getenv("STAB_API_KEY")
    if not key: return False, "Не нашел ключ"
    return True, "все хорошо!"

@st.cache_data(show_spinner=False)
def edit_image_via_api(image_bytes: bytes, prompt: str):
    api_key = os.getenv("STAB_API_KEY")
    if not api_key:
        raise ValueError("не нашел API ключ")
    
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img.thumbnail((1024, 1024))
    
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=90)
    optimized_bytes = buffer.getvalue()

    try:
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers={
                "authorization": f"Bearer {api_key}",
                "accept": "image/*"
            },
            files={
                "image": ("image.jpg", optimized_bytes, "image/jpeg")
            },
            data={
                "prompt": prompt,
                "mode": "image-to-image",
                "strength": 0.6, 
                "output_format": "jpeg"
            },
            timeout=60
        )

        if response.status_code == 200:
            return response.content, "Stable Diffusion 3"
        else:
            error_msg = response.json().get("errors", response.text)
            raise Exception(f"Ошибка сервера Stability: {error_msg}")
            
    except Exception as e:
        raise Exception(f"Техническая ошибка: {str(e)}")
