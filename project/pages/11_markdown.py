import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="防災クイズ", page_icon="⛑️", layout="centered")

# ============================
# 初期化（ポイント・出題済み管理）
# ============================

if "score" not in st.session_state:
    st.session_state.score = 0

if "used" not in st.session_state:
    st.session_state.used = []

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

# ============================
# 防災クイズ（好きなだけ増やせる）
# ============================

quiz_list = [
    {
        "q": "地震が起きたとき、まず最初にするべき行動は？",
        "choices": ["身を守る", "外に走る", "窓を開ける", "スマホを見る"],
        "a": "身を守る"
    },
    {
        "q": "津波から避難するとき、まず向かうべき場所は？",
        "choices": ["高い場所", "海の様子を見る", "家に戻る", "車で海沿いへ行く"],
        "a": "高い場所"
    },
    {
        "q": "火災のとき煙を吸わないための姿勢は？",
        "choices": ["低い姿勢", "背伸びする", "走る", "ジャンプする"],
        "a": "低い姿勢"
    },
    {
        "q": "台風のとき危険な場所は？",
        "choices": ["川の近く", "家の中", "高台", "避難所"],
        "a": "川の近く"
    },
    {
        "q": "非常用持ち出し袋に入れるべきものは？",
        "choices": ["水・食料", "ゲーム機", "大きい家具", "観葉植物"],
        "a": "水・食料"
    },
    {
        "q": "地震のときエレベーターに乗っていたらどうする？",
        "choices": ["全階のボタンを押す", "飛び降りる", "叫ぶ", "スマホで動画を撮る"],
        "a": "全階のボタンを押す"
    },
    {
        "q": "避難所でまず確認するべきことは？",
        "choices": ["受付で登録する", "スマホの充電場所", "友達を探す", "ゲームできる場所"],
        "a": "受付で登録する"
    }
]

# ============================
# 右上にポイント表示
# ============================

st.markdown(
    f"<div style='position:absolute; top:10px; right:20px; font-size:24px;'>"
    f"ポイント：{st.session_state.score} pt</div>",
    unsafe_allow_html=True
)

st.title("防災クイズ（mikan風カード形式）")

# ============================
# 新しい問題を選ぶ（重複なし）
# ============================

def pick_new_quiz():
    remaining = [q for q in quiz_list if q["q"] not in st.session_state.used]
    if not remaining:
        st.session_state.used = []  # 全部出たらリセット
        remaining = quiz_list
    quiz = random.choice(remaining)
    st.session_state.used.append(quiz["q"])
    return quiz

if st.session_state.current_quiz is None:
    st.session_state.current_quiz = pick_new_quiz()

quiz = st.session_state.current_quiz

# ============================
# 選択肢をランダムにシャッフル
# ============================

choices = quiz["choices"].copy()
random.shuffle(choices)

st.subheader("問題")
st.write("### " + quiz["q"])

choice = st.radio("選択肢を選んでね", choices)

# ============================
# ◯演出（侃のやつ）
# ============================

circle_effect = """<html>…ここに侃の◯演出HTML…</html>"""

# ============================
# ✖演出（170px巨大バツ）
# ============================

cross_effect = """<html>…ここに侃の✖演出HTML…</html>"""

# ============================
# 判定ボタン
# ============================

if st.button("送信"):
    if choice == quiz["a"]:
        st.success("正解！ +1pt")
        st.session_state.score += 1
        components.html(circle_effect, height=700, scrolling=False)
    else:
        st.error("不正解… -1pt")
        st.session_state.score -= 1
        components.html(cross_effect, height=700, scrolling=False)

    st.session_state.current_quiz = None  # 次の問題へ切り替え

    st.stop()

# ============================
# 次の問題へボタン
# ============================

if st.button("次の問題へ"):
    st.session_state.current_quiz = pick_new_quiz()
    st.rerun()
