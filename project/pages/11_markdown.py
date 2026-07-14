import streamlit as st

st.set_page_config(page_title="2D Trophy", page_icon="🏆")

# CSSで右の画像風トロフィーを描く
st.markdown("""
<style>
.trophy-flat {
    width: 150px;
    margin: 40px auto;
    position: relative;
}

/* カップ部分（右の画像に近い平面デザイン） */
.trophy-flat .cup {
    width: 120px;
    height: 80px;
    background: #FFD84D; /* 明るい黄色 */
    border-radius: 60px 60px 20px 20px;
    margin: auto;
    border: 6px solid #E0B63F; /* 少し濃い黄色の縁 */
}

/* ハンドル（右の画像の丸い形に合わせる） */
.trophy-flat .handle-left,
.trophy-flat .handle-right {
    width: 35px;
    height: 55px;
    border: 6px solid #E0B63F;
    border-radius: 50%;
    position: absolute;
    top: 10px;
    background: #FFD84D;
}

.trophy-flat .handle-left { left: -30px; }
.trophy-flat .handle-right { right: -30px; }

/* 台座（右の画像の茶色） */
.trophy-flat .base {
    width: 90px;
    height: 40px;
    background: #C48A4A;
    margin: auto;
    border-radius: 6px;
    margin-top: 10px;
    border: 6px solid #A06A36;
}
</style>
""", unsafe_allow_html=True)

# HTMLでトロフィーを表示
st.markdown("""
<div class="trophy-flat">
    <div class="cup"></div>
    <div class="handle-left"></div>
    <div class="handle-right"></div>
    <div class="base"></div>
</div>
""", unsafe_allow_html=True)

st.title("🏆 2Dトロフィー（右の画像風）")
