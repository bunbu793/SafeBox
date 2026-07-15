import streamlit as st
from logic.profile import load_profile
from screens.practice import practice_screen
from screens.review import review_screen
from screens.test import test_screen
from screens.status import status_screen

st.set_page_config(page_title="防災クイズRPG", page_icon="⛑️", layout="centered")

if "user_id" not in st.session_state:
    st.session_state.user_id = "player_1"

profile = load_profile(st.session_state.user_id)

st.title("防災クイズRPG")

mode = st.selectbox("モードを選んでください", ["ホーム", "練習", "復習", "テスト", "ステータス"])

if mode == "練習":
    practice_screen(profile)

elif mode == "復習":
    review_screen(profile)

elif mode == "テスト":
    test_screen(profile)

elif mode == "ステータス":
    status_screen(profile)

else:
    st.write("モードを選んでね")