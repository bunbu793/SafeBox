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

# 後方互換用
KOBITO_IMAGE_URL = KOBITO_IMAGES["login"]

# =========================================================
# ページごとのテーマカラー（ヘッダーのグラデーション & 背景の淡い色）
# =========================================================

PAGE_THEMES = {
    "login":       {"header": ("#e53935", "#ff7043"), "bg": ("#fff5f2", "#ffeceb")},
    "home":        {"header": ("#fb8c00", "#ffb74d"), "bg": ("#fff8f0", "#fff3e0")},
    "family":      {"header": ("#f9a825", "#ffe082"), "bg": ("#fffdf0", "#fff9db")},
    "checklist":   {"header": ("#43a047", "#81c784"), "bg": ("#f3fbf3", "#e8f5e9")},
    "family_code": {"header": ("#00897b", "#4db6ac"), "bg": ("#f0fbfa", "#e0f2f1")},
    "shopping":    {"header": ("#1e88e5", "#64b5f6"), "bg": ("#f0f8ff", "#e3f2fd")},
    "items":       {"header": ("#8e24aa", "#ba68c8"), "bg": ("#faf0fb", "#f3e5f5")},
    "chat":        {"header": ("#ff6f91", "#ff9a76"), "bg": ("#fff8f0", "#fef1f1")},
    "safety":      {"header": ("#6d4c41", "#a1887f"), "bg": ("#f8f4f2", "#efebe9")},
    "quiz":        {"header": ("#616161", "#9e9e9e"), "bg": ("#f7f7f7", "#eeeeee")},
    "brochure":    {"header": ("#1a237e", "#3949ab"), "bg": ("#f0f1fb", "#e8eaf6")},
    "settings":    {"header": ("#7e57c2", "#b39ddb"), "bg": ("#f6f3fb", "#ede7f6")},
}

def apply_page_theme(page_key, title, subtitle=""):
    """背景グラデーション・ヘッダーバナー・カード風ボタンを一括適用する"""

    # 小人のスライドインアニメーション用CSSも一緒に注入する
    inject_kobito_css()

    theme = PAGE_THEMES.get(page_key, PAGE_THEMES["home"])
    h1, h2 = theme["header"]
    b1, b2 = theme["bg"]

    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(180deg, {b1} 0%, {b2} 100%);
    }}

    .page-header {{
        background: linear-gradient(135deg, {h1}, {h2});
        border-radius: 20px;
        padding: 22px 28px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }}
    .page-header h1 {{
        margin: 0;
        font-size: 26px;
    }}
    .page-header p {{
        margin: 6px 0 0 0;
        opacity: 0.9;
        font-size: 14px;
    }}

    .stButton>button{{
        width:100%;
        border-radius:16px;
        font-weight:700;
        font-size:15px;
        border: none;
        background: white;
        color: #444;
        box-shadow: 0 3px 8px rgba(0,0,0,0.08);
        transition: 0.15s;
        padding: 10px;
    }}
    .stButton>button:hover{{
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(0,0,0,0.12);
    }}

    div[data-testid="stForm"] {{
        background: white;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    }}

    div[data-testid="stMetric"] {{
        background: white;
        border-radius: 14px;
        padding: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }}

    div[data-testid="stContainer"] > div[style*="border"] {{
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    </style>

    <div class="page-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

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