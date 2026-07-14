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
if "test_passed" not in st.session_state:
    st.session_state.test_passed = False

# -------------------------
# ○ × アニメーション CSS
# -------------------------
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 12px;
    background: #f8f9fa;
    border: 2px solid #ddd;
    margin-bottom: 20px;
    position: relative;
}

.mark {
    position: absolute;
    top: -10px;
    right: -10px;
    font-size: 60px;
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
</style>
""", unsafe_allow_html=True)

# -------------------------
# 問題データ（例：Lv1）
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
# 練習問題開始
# -------------------------
if st.button("🎯 練習問題を始める"):
    st.session_state.mode = "practice"
    st.session_state.questions = get_questions_for_rank(st.session_state.rank)
    st.session_state.current_index = 0
    st.session_state.results = []

# -------------------------
# テスト開始
# -------------------------
if st.button("🔥 テストを受ける（9問正解で合格）"):
    st.session_state.mode = "test"
    all_qs = get_questions_for_rank(st.session_state.rank)
    st.session_state.questions = random.sample(all_qs, 10)
    st.session_state.current_index = 0
    st.session_state.results = []

# -------------------------
# 問題カード表示
# -------------------------
if st.session_state.mode in ["practice", "test"]:
    idx = st.session_state.current_index
    qs = st.session_state.questions

    if idx < len(qs):
        q = qs[idx]

        st.markdown(f"<div class='card'>", unsafe_allow_html=True)

        st.write(f"### {idx+1}. {q['q']}")

        user_answer = st.radio(
            "回答を選択してください",
            q["choices"],
            key=f"ans_{idx}"
        )

        if st.button("回答する"):
            correct = (user_answer == q["answer"])
            st.session_state.results.append(correct)

            # ○ × アニメーション表示
            if correct:
                st.markdown("<div class='mark correct'>○</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='mark wrong'>×</div>", unsafe_allow_html=True)

            st.session_state.current_index += 1

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # -------------------------
        # 全問終了 → 結果発表
        # -------------------------
        correct_count = sum(st.session_state.results)
        total = len(st.session_state.results)

        st.write(f"### 結果：{correct_count} / {total}")

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

        # -------------------------
        # ランクアップボタン
        # -------------------------
        if st.session_state.test_passed:
            if st.button("次のランクへ進む"):
                st.session_state.rank += 1
                st.session_state.points += 900 if correct_count == 9 else 1200
                st.success("ランクアップしました！")
                st.session_state.mode = None
