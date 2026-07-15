import streamlit as st
import random

st.set_page_config(page_title="防災クイズ", page_icon="📝")

# -------------------------
# ラジオボタン横並びCSS
# -------------------------
st.markdown("""
<style>
div.stRadio > div {
    display: flex;
    flex-direction: row;
    gap: 20px;
}
</style>
""", unsafe_allow_html=True)

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
# CSS（○×＋新トロフィー＋右側配置）
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

/* ○ × を右側へ移動 */
.mark {
    position: absolute;
    top: 20px;
    right: -150px;   /* ← 右側へ移動 */
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

/* トロフィーを右側へ移動 */
.trophy {
    width: 120px;
    height: 160px;
    position: absolute;
    top: 100px;
    right: -180px;   /* ← 右側へ移動 */

    animation: zoomIn 0.8s ease-out forwards,
               explode 0.8s ease-out 0.8s forwards,
               rise 1.2s ease-out 1.6s forwards,
               shine 2s ease-in-out infinite 2.8s;
}

/* カップ部分 */
.trophy .cup {
    width: 100px;
    height: 70px;
    background: gold;
    border-radius: 50px 50px 20px 20px;
    margin: auto;
    position: relative;
    box-shadow: 0 0 20px rgba(255,215,0,0.7);
}

/* ハンドル */
.trophy .handle-left,
.trophy .handle-right {
    width: 30px;
    height: 50px;
    border: 8px solid gold;
    border-radius: 50%;
    position: absolute;
    top: 10px;
}

.trophy .handle-left { left: -25px; }
.trophy .handle-right { right: -25px; }

/* 台座 */
.trophy .base {
    width: 80px;
    height: 40px;
    background: #8b5a2b;
    margin: auto;
    border-radius: 5px;
    margin-top: 10px;
}

/* アニメーション */
@keyframes zoomIn {
    0% { transform: scale(0.1) translateY(-200px); opacity: 0; }
    60% { transform: scale(1.3) translateY(20px); opacity: 1; }
    100% { transform: scale(1) translateY(0px); opacity: 1; }
}

@keyframes explode {
    0% { filter: drop-shadow(0px 0px 0px gold); }
    50% { filter: drop-shadow(0px 0px 40px gold); }
    100% { filter: drop-shadow(0px 0px 10px gold); }
}

@keyframes rise {
    0% { transform: translateY(0px); }
    100% { transform: translateY(-20px); }
}

@keyframes shine {
    0% { filter: drop-shadow(0px 0px 5px gold); }
    50% { filter: drop-shadow(0px 0px 25px gold); }
    100% { filter: drop-shadow(0px 0px 5px gold); }
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# 問題データ
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
st.title("📝 防災クイズ（Ultimate Trophy Edition）")

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

        # ○×＋トロフィー（右側表示）
        if st.session_state.answered:
            if st.session_state.last_correct:
                st.markdown("<div class='mark correct'>○</div>", unsafe_allow_html=True)
                st.markdown("""
                <div class="trophy">
                    <div class="cup"></div>
                    <div class="handle-left"></div>
                    <div class="handle-right"></div>
                    <div class="base"></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<div class='mark wrong'>×</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # 次の問題へ
        if st.session_state.answered and st.button("次の問題へ"):
            st.session_state.index += 1
            st.session_state.answered = False
