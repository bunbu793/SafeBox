import streamlit as st

st.set_page_config(page_title="2D Trophy", page_icon="🏆")

# 2Dトロフィー（Lottie）
lottie_html = """
<div style="width:260px;margin:auto;">
    <lottie-player 
        src="https://lottie.host/8c3f5c4b-0f3a-4b8e-9e8c-1e8f4b5a2f2f/2d_trophy.json"
        background="transparent"
        speed="1"
        style="width: 260px; height: 260px;"
        loop
        autoplay>
    </lottie-player>
</div>

<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
"""

st.title("🏆 2Dトロフィー表示テスト")

st.components.v1.html(lottie_html, height=350)
