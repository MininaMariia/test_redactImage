import streamlit as st
from PIL import Image
import io
from utils.api import edit_image_via_api, test_api_connection

st.set_page_config(page_title="Редактирование изображения", page_icon="!!!", layout="centered")

def local_css():
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
        <style>
            .stApp { background-color: #FFFFFF !important; }
            
            * {
                font-family: 'Playfair Display', serif !important;
                color: #000000 !important;
            }

            .subtitle {
                letter-spacing: 5px;
                font-size: 14px !important;
                font-weight: bold;
                text-align: center;
                margin-top: 50px;
                text-transform: uppercase;
                margin-bottom: 10px;
            }

            .main-title {
                font-size: 40px !important;
                font-style: italic;
                text-align: center;
                margin-bottom: 40px;
                line-height: 1.2;
                font-weight: 400;
            }

            [data-testid="stFileUploadDropzone"] {
                background-color: #FFFFFF !important;
                border: 1px solid #000000 !important;
                border-radius: 0px !important;
            }

            div.stButton > button {
                background-color: #c99277 !important;
                color: white !important;
                border-radius: 0px !important;
                border: none !important;
                width: 100%; height: 50px;
                text-transform: uppercase; letter-spacing: 2px;
                font-size: 14px; font-weight: bold;
                margin-top: 20px;
            }

            .stSelectbox div[data-baseweb="select"], .stTextInput input {
                border-radius: 0px !important; 
                border: 1px solid #000000 !important;
            }
            
            #MainMenu, footer, header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )

local_css()

st.markdown('<p class="subtitle">Тестовое задание</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Редактирование изображения <br>с использованием генеративной модели</h1>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Загрузите фото", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")

if uploaded_file:
    img = Image.open(uploaded_file)
    
    st.image(img, width=400, caption="Фото до")
    
    st.markdown("<h3 style='text-align: center;'>Что хотите увидеть?</h3>", unsafe_allow_html=True)
    
    PRESETS = {
        "5 лет курения": "person's face after 5 years of heavy smoking, visible skin damage, premature aging, unhealthy complexion, highly detailed",
        "10 лет алкоголя": "person's face after 10 years of chronic alcoholism, facial swelling, broken capillaries, dull eyes, bloated appearance",
        "20 лет обычной жизни": "a realistic aged version of this person, 20 years into the future, natural maturation, subtle wrinkles, realistic skin texture",
        "Свой вариант": ""
    }
    
    selected_option = st.selectbox("How will you change?", list(PRESETS.keys()), label_visibility="collapsed")
    
    prompt = PRESETS[selected_option]
    if selected_option == "Свой вариант":
        prompt = st.text_input("Опишите, что вы хотите увидеть (in English):")

    if st.button("Показать результат"):
        if prompt:
            with st.spinner("Происходит магия"):
                try:
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG')
                    
                    result_bytes, _ = edit_image_via_api(img_byte_arr.getvalue(), prompt)
                    
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(img, caption="До", use_container_width=True)
                    with col2:
                        st.image(result_bytes, caption="После", use_container_width=True)
                        
                    st.download_button("Скачать изображение", result_bytes, "prediction.jpg", "image/jpeg")
                except Exception as e:
                    st.error(f"Ошибка: {e}")