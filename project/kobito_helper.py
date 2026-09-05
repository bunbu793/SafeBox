import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

BASE_URL = "https://raw.githubusercontent.com/bunbu793/SafeBox/main/project/assets"

# ページごとの小人画像
KOBITO_IMAGES = {
    "login":       f"{BASE_URL}/kobito_red.png",
    "home":        f"{BASE_URL}/kobito_orange.png",
    "family":      f"{BASE_URL}/kobito_yellow.png",
    "checklist":   f"{BASE_URL}/kobito_green.png",
    "family_code": f"{BASE_URL}/kobito_teal.png",
    "shopping":    f"{BASE_URL}/kobito_blue.png",
    "items":       f"{BASE_URL}/kobito_purple.png",
    "chat":        f"{BASE_URL}/kobito_pink.png",
    "safety":      f"{BASE_URL}/kobito_brown.png",
    "quiz":        f"{BASE_URL}/kobito_gray.png",
    "brochure":    f"{BASE_URL}/kobito_navy.png",
    "settings":    f"{BASE_URL}/kobito_violet.png",
}

# 後方互換用（今まで KOBITO_IMAGE_URL を直接importしていた箇所のため）
KOBITO_IMAGE_URL = KOBITO_IMAGES["login"]

KOBITO_CSS = """
<style>
@keyframes kobito-move {
    0%   { right: -200px; opacity: 0; }
    20%  { right: 80px; opacity: 1; }
    70%  { right: 80px; opacity: 1; }
    100% { right: -200px; opacity: 0; }
}
.kobito-box {
    position: fixed;
    top: 300px;
    right: -200px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: center;
    animation: kobito-move 6s ease-in-out forwards;
}
.kobito-balloon {
    background:#fff;
    border:2px solid #333;
    padding:10px;
    border-radius:10px;
    margin-bottom:10px;
}
</style>
"""

def inject_kobito_css():
    st.markdown(KOBITO_CSS, unsafe_allow_html=True)

def get_base64_image_from_url(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode()

def show_kobito_popup(image_url, message, session_key):
    if session_key not in st.session_state:
        st.session_state[session_key] = False

    if not st.session_state[session_key]:
        img_b64 = get_base64_image_from_url(image_url)
        st.markdown(f"""
        <div class="kobito-box">
            <div class="kobito-balloon">{message}</div>
            <img src="data:image/png;base64,{img_b64}" width="150">
        </div>
        """, unsafe_allow_html=True)
        st.session_state[session_key] = True

@st.cache_data
def load_kobito_avatar(image_url):
    """chat_message の avatar 用に PIL Image として読み込む"""
    response = requests.get(image_url)
    return Image.open(BytesIO(response.content))
