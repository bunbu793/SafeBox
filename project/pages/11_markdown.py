import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Quiz Totem", page_icon="❓", layout="centered")

st.title("クイズ：トーテム演出つき")

# クイズ問題
question = "Minecraftでネザーにいる巨大なスライムの名前は？"
answer = "マグマキューブ"

user_answer = st.text_input("答えを入力してね")

# 正解・不正解で演出を切り替える
if st.button("判定"):
    if user_answer == answer:
        st.success("正解！")
        # ◯演出を読み込む
        with open("circle_effect.html", "r", encoding="utf-8") as f:
            components.html(f.read(), height=700, scrolling=False)
    else:
        st.error("不正解…")
        # ✖演出を読み込む
        with open("cross_effect.html", "r", encoding="utf-8") as f:
            components.html(f.read(), height=700, scrolling=False)
