import streamlit as st

st.set_page_config(page_title="2D Trophy", page_icon="🏆")

# 侃のCSS（そのまま使える）
st.markdown("""
<style>
.trophy{
    width:220px;
    margin:auto;
    position:relative;
}

/* カップ本体 */
.cup{
    width:140px;
    height:120px;
    margin:auto;
    background:#FFD46A;
    border-radius:0 0 60px 60px;
    position:relative;
}

/* 左取っ手 */
.cup::before{
    content:"";
    position:absolute;
    left:-35px;
    top:18px;

    width:42px;
    height:42px;

    border:12px solid #FFD46A;
    border-right:none;
    border-radius:50%;
}

/* 右取っ手 */
.cup::after{
    content:"";
    position:absolute;
    right:-35px;
    top:18px;

    width:42px;
    height:42px;

    border:12px solid #FFD46A;
    border-left:none;
    border-radius:50%;
}

/* ★ */
.star{
    position:absolute;
    left:50%;
    top:42%;

    transform:translate(-50%,-50%);

    font-size:42px;
    color:white;

    text-shadow:0 0 8px gold;
}

/* 柱 */
.stem{
    width:34px;
    height:55px;
    background:#FFD46A;

    margin:auto;
}

/* 台 */
.base-top{
    width:80px;
    height:28px;

    background:#8B4A00;

    margin:auto;

    border-radius:6px 6px 0 0;
}

/* 土台 */
.base{
    width:130px;
    height:22px;

    background:#6E3900;

    margin:auto;

    border-radius:5px;
}
</style>
""", unsafe_allow_html=True)

# HTML構造（これがないと表示されない）
st.markdown("""
<div class="trophy">
    <div class="cup"></div>
    <div class="star">★</div>
    <div class="stem"></div>
    <div class="base-top"></div>
    <div class="base"></div>
</div>
""", unsafe_allow_html=True)

st.title("🏆 2Dトロフィー（右の画像風）")
