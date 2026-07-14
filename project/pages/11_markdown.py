import streamlit as st

st.set_page_config(page_title="2D Trophy", page_icon="🏆")

# CSSで描く2Dトロフィー
st.markdown("""
<style>
.trophy-2d {
    width: 150px;
    margin: 40px auto;
    position: relative;
}

/* カップ部分（2Dイラスト風） */
.trophy-2d .cup {
    width: 120px;
    height: 80px;
    background: #FFD84D;
    border-radius: 60px 60px 20px 20px;
    margin: auto;
    border: 4px solid #E0B63F;
}

/* ハンドル（2Dの丸い形） */
.trophy-2d .handle-left,
.trophy-2d .handle-right {
    width: 35px;
    height: 55px;
    border: 4px solid #E0B63F;
    border-radius: 50%;
    position: absolute;
    top: 10px;
    background: #FFD84D;
}

.trophy-2d .handle-left { left: -25px; }
.trophy-2d .handle-right { right: -25px; }

/* 台座（2Dのシンプルな木色） */
.trophy-2d .base {
    width: 90px;
    height: 40px;
    background: #C48A4A;
    margin: auto;
    border-radius: 6px;
    margin-top: 10px;
    border: 4px solid #A06A36;
}
</style>
""", unsafe_allow_html=True)

# HTMLでトロフィーを表示
st.markdown("""
<div class="trophy-2d">
    <div class="cup"></div>
    <div class="handle-left"></div>
    <div class="handle-right"></div>
    <div class="base"></div>
</div>
""", unsafe_allow_html=True)

st.title("🏆 2Dトロフィー表示テスト")
