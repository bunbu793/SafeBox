import streamlit as st
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="トロフィー表示", page_icon="🏆")

# Lottie読み込み関数
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# LOTTE風の豪華トロフィー（フリー素材）
trophy_lottie = load_lottie(
    "https://assets10.lottiefiles.com/packages/lf20_trophy.json"
)

st.title("🏆 トロフィー表示テスト")

# トロフィーだけ表示
st_lottie(trophy_lottie, height=300)
