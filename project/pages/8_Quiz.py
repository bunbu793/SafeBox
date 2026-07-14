import streamlit as st
import random

st.set_page_config(page_title="防災クイズ", page_icon="📝")

# -------------------------
# セッション初期化
# -------------------------
if "rank" not in st.session_state:
    st.session_state.rank = 1
if "points" not in st.session_state:
    st.session_state.points = 0
if "mode" not in st.session_state:
    st.session_state.mode = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "results" not in st.session_state:
    st.session_state.results = []
if "wrong_questions" not in st.session_state:
    st.session_state.wrong_questions = []
if "test_passed" not in st.session_state:
    st.session_state.test_passed = False
if "answered" not in st.session_state:
    st.session_state.answered = False
if "last_answer_correct" not in st.session_state:
    st.session_state.last_answer_correct = None

# -------------------------
# ○ × アニメーション CSS
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

.mark {
    position: absolute;
    top: -20px;
    right: -20px;
    font-size: 70px;
    font-weight: bold;
    animation: pop 0.4s ease-out forwards;
}

.correct {
    color: #2ecc71;
}

.wrong {
    color: #e74c3c;
}

@keyframes pop {
    0% { transform: scale(0.2); opacity: 0; }
    70% { transform: scale(1.3); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
}

/* トロフィー演出（回転＋光） */
.trophy {
    font-size: 120px;
    text-align: center;
    animation: pop 0.6s ease-out forwards, rotate 2s linear infinite, shine 2s ease-in-out infinite;
    display: block;
    margin-top: 20px;
}

@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes shine {
    0% { filter: drop-shadow(0px 0px 0px gold); }
    50% { filter: drop-shadow(0px 0px 25px gold); }
    100% { filter: drop-shadow(0px 0px 0px gold); }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 問題データ（仮）
# -------------------------
def get_questions_for_rank(rank):
    return [
        {
            "q": "地震が起きたとき、まず最初にすべき行動は？",
            "choices": ["頭を守る", "外に走って出る", "スマホを見る", "窓を開ける"],
            "answer": "頭を守る"
        },
        {
            "q": "避難所で最も大切なことは？",
            "choices": ["静かにする", "情報を共有する", "荷物を広げる", "好きな場所を占領する"],
            "answer": "情報を共有する"
        }
    ]

# -------------------------
# ボタン群
# -------------------------
st.title("📝 防災クイズ")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎯 練習問題を解く"):
        st.session_state.mode = "practice"
        st.session_state.questions = get_questions_for_rank(st.session_state.rank)
        st.session_state.current_index = 0
        st.session_state.results = []
        st.session_state.wrong_questions = []
        st.session_state.answered = False

with col2:
    if st.button("🔥 テスト問題を解く"):
        st.session_state.mode = "test"
        all_qs = get_questions_for_rank(st.session_state.rank)
        st.session_state.questions = random.sample(all_qs, min(10, len(all_qs)))
        st.session_state.current_index = 0
        st.session_state.results = []
        st.session_state.wrong_questions = []
        st.session_state.answered = False

with col3:
    if st.button("📘 間違えた問題を解く"):
        if len(st.session_state.wrong_questions) == 0:
            st.warning("まだ間違えた問題がありません")
        else:
            st.session_state.mode = "review"
            st.session_state.questions = st.session_state.wrong_questions
            st.session_state.current_index = 0
            st.session_state.results = []
            st.session_state.answered = False

# -------------------------
# 問題カード表示
# -------------------------
if st.session_state.mode in ["practice", "test", "review"]:
    idx = st.session_state.current_index
    qs = st.session_state.questions

    if idx < len(qs):
        q = qs[idx]

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.write(f"### {idx+1}. {q['q']}")

        user_answer = st.radio(
            "回答を選択してください",
            q["choices"],
            key=f"ans_{idx}"
        )

        # 回答する（○×だけ表示）
        if st.button("回答する"):
            correct = (user_answer == q["answer"])
            st.session_state.results.append(correct)
            st.session_state.last_answer_correct = correct
            st.session_state.answered = True

            if not correct and st.session_state.mode == "practice":
                st.session_state.wrong_questions.append(q)

        # ○×表示（回答後のみ）
        if st.session_state.answered:
            if st.session_state.last_answer_correct:
                st.markdown("<div class='mark correct'>○</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='mark wrong'>×</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # 次の問題へ
        if st.button("次の問題へ"):
            st.session_state.current_index += 1
            st.session_state.answered = False

    else:
        # -------------------------
        # 最後だけ結果発表
        # -------------------------
        correct_count = sum(st.session_state.results)

        if st.session_state.mode == "practice":
            st.success(f"🎉 +{correct_count} pt 獲得！")
            st.session_state.points += correct_count

        if st.session_state.mode == "test":
            if correct_count >= 9:
                st.success("🎉 合格！次のランクへ進めます")
                st.session_state.test_passed = True
            else:
                st.error("不合格… また挑戦しよう！")
                st.session_state.test_passed = False

        if st.session_state.mode == "review":
            st.info("復習お疲れさま！")

        # -------------------------
        # ランクアップボタン
        # -------------------------
        if st.session_state.test_passed:
            if st.button("次のランクへ進む"):
                st.session_state.rank += 1
                st.session_state.points += 900 if correct_count == 9 else 1200

                st.success("ランクアップしました！")

                # トロフィーアニメーション（回転＋光）
                st.markdown("<div class='trophy'>🏆</div>", unsafe_allow_html=True)

                st.session_state.mode = None
