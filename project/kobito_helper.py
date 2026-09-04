import streamlit as st
import requests
import base64

KOBITO_IMAGE_URL = "https://raw.githubusercontent.com/bunbu793/SafeBox/main/project/assets/kobito1.png"

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