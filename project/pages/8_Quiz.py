import streamlit as st
import random

st.set_page_config(page_title="防災クイズ", page_icon="📝")

# -------------------------
# セッション初期化
# -------------------------
if "questions" not in st.session_state:
    st.session_state.questions = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "last_correct" not in st.session_state:
    st.session_state.last_correct = None

# -------------------------
# ○ × ＋ トロフィー CSS（perfect）
# -------------------------
st.markdown("""
<style>
.card {
    width: 70%;
    margin: auto;
    padding: 25px;
    border-radius: 12px;
    background: #ffffff;
    border: 2px solid #ddd;
    margin-bottom: 20px;
    position: relative;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}

/* ○ × */
.mark {
    position: absolute;
    top: -20px;
    right: -20px;
    font-size: 70px;
    font-weight: bold;
    animation: pop 0.4s ease-out forwards;
}
.correct { color: #2ecc71; }
.wrong { color: #e74c3c; }

@keyframes pop {
    0% { transform: scale(0.2); opacity: 0; }
    70% { transform: scale(1.3); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
}

/* トロフィー（遠→近＋横回転＋光） */
.trophy {
    font-size: 120px;
    text-align: center;
    display: block;
    margin-top: 10px;
    animation: flyin 1.2s ease-out forwards, shine 2s ease-in-out infinite;
}

/* 遠くから近くへ＋横回転 */
@keyframes flyin {
    0% {
        transform: translateY(-200px) scale(0.1) rotateY(0deg);
        opacity: 0;
    }
    40% {
        transform: translateY(-80px) scale(0.5) rotateY(180deg);
        opacity: 0.7;
    }
    70% {
        transform: translateY(-20px) scale(1.2) rotateY(360deg);
        opacity: 1;
    }
    100% {
        transform: translateY(0px) scale(1) rotateY(360deg);
        opacity: 1;
    }
}

/* 光る */
@keyframes shine {
    0% { filter: drop-shadow(0px 0px 0px gold); }
    50% { filter: drop-shadow(0px 0px 25px gold); }
    100% { filter: drop-shadow(0px 0px 0px gold); }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 問題データ（簡易版）
# -------------------------
QUESTIONS = [
    {
        "q": "地震が起きたとき、まず最初にすべき行動は？",
        "choices": ["頭を守る", "外に走って出る", "スマホを見る", "窓を開ける"],
        "answer": "頭を守る"
    },
    {
        "q": "避難所で最も大切なことは？",
        "choices": ["静かにする", "情報を共有する", "荷物を広げる", "好きな場所を占領する"],
        "answer": "情報を共有する"
    },
    {
        "q": "非常食として正しいものは？",
        "choices": ["缶詰", "生肉", "アイスクリーム", "ケーキ"],
        "answer": "缶詰"
    }
]

# -------------------------
# スタートボタン
# -------------------------
st.title("📝 防災クイズ（Perfect Trophy Edition）")

if st.button("クイズを始める"):
    st.session_state.questions = QUESTIONS
    st.session_state.index = 0
    st.session_state.answered = False

# -------------------------
# 問題カード表示
# -------------------------
if st.session_state.questions:
    idx = st.session_state.index

    if idx < len(st.session_state.questions):
        q = st.session_state.questions[idx]

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write(f"### {idx+1}. {q['q']}")

        user_answer = st.radio(
            "回答を選択してください",
            q["choices"],
            key=f"ans_{idx}"
        )

        # 回答する
        if st.button("回答する"):
            correct = (user_answer == q["answer"])
            st.session_state.last_correct = correct
            st.session_state.answered = True

        # ○×表示＋正解ならトロフィー
        if st.session_state.answered:
            if st.session_state.last_correct:
                st.markdown("<div class='mark correct'>○</div>", unsafe_allow_html=True)
                st.markdown("<div class='trophy'>🏆</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='mark wrong'>×</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # 次の問題へ
        if st.session_state.answered and st.button("次の問題へ"):
            st.session_state.index += 1
            st.session_state.answered = False
