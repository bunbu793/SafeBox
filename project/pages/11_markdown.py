import streamlit as st

st.set_page_config(page_title="Lottie Trophy", page_icon="🏆")

# Lottie埋め込み（外部ライブラリ不要）
lottie_html = """
<div style="width:300px;margin:auto;">
    <lottie-player 
        src="https://assets10.lottiefiles.com/packages/lf20_trophy.json"
        background="transparent"
        speed="1"
        style="width: 300px; height: 300px;"
        loop
        autoplay>
    </lottie-player>
</div>

<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
"""

st.title("🏆 トロフィー表示テスト（Lottie）")

st.components.v1.html(lottie_html, height=350)
