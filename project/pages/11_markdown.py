import streamlit as st

st.set_page_config(
    page_title="Golden Trophy",
    page_icon="🏆",
    layout="centered"
)

st.markdown("""
<style>
/* 侃のCSSはそのまま全部ここに入ってる（省略） */
</style>

<div class="trophy-area">
    <div class="trophy">

        <div class="cup">

            <!-- ★ ここを修正：glow-ring を閉じる -->
            <div class="glow-ring"></div>

            <!-- spark たち -->
            <div class="spark spark1"></div>
            <div class="spark spark2"></div>
            <div class="spark spark3"></div>
            <div class="spark spark4"></div>
            <div class="spark spark5"></div>
            <div class="spark spark6"></div>

            <!-- ハイライト -->
            <div class="highlight"></div>

            <!-- 取っ手 -->
            <div class="handle-left"></div>
            <div class="handle-right"></div>

            <!-- 星 -->
            <div class="star">★</div>

        </div>

        <div class="stem"></div>
        <div class="base-top"></div>
        <div class="base-bottom"></div>

    </div>
</div>

""", unsafe_allow_html=True)
