import streamlit as st
import random

# -------------------------
# 初期化
# -------------------------
if "rank" not in st.session_state:
    st.session_state.rank = 1

if "points" not in st.session_state:
    st.session_state.points = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "wrong_questions" not in st.session_state:
    st.session_state.wrong_questions = []

if "play_animation" not in st.session_state:
    st.session_state.play_animation = False

if "mode" not in st.session_state:
    st.session_state.mode = None

# -------------------------
# UI
# -------------------------
st.title("📝 防災クイズ")

st.info(f"現在のランク：Lv.{st.session_state.rank}")
st.success(f"累計ポイント：{st.session_state.points} pt")

st.divider()

# -------------------------
# 練習問題開始
# -------------------------
if st.button("🎯 練習問題を始める"):
    st.session_state.mode = "practice"
    st.session_state.wrong_questions = []
    st.session_state.streak = 0
    st.session_state.play_animation = False

# -------------------------
# テスト開始
# -------------------------
if st.button("🔥 テストを受ける（9問正解で合格）"):
    st.session_state.mode = "test"
    st.session_state.wrong_questions = []
    st.session_state.streak = 0
    st.session_state.play_animation = False

# -------------------------
# 問題数の設定
# -------------------------
def get_question_count():
    if st.session_state.mode == "practice":
        return 10 if st.session_state.rank == 1 else 25
    if st.session_state.mode == "test":
        return 10

# -------------------------
# ダミー問題生成（後で generate_quiz に置き換え）
# -------------------------
def generate_questions(n):
    questions = []
    for i in range(n):
        questions.append({
            "q": f"問題 {i+1}：防災に関する質問（仮）",
            "choices": ["A", "B", "C", "D"],
            "answer": random.choice(["A", "B", "C", "D"])
        })
    return questions

# -------------------------
# クイズ実行
# -------------------------
if st.session_state.mode in ["practice", "test"]:
    num_q = get_question_count()
    questions = generate_questions(num_q)

    score = 0

    for idx, q in enumerate(questions):
        st.write(f"### {q['q']}")
        user_answer = st.radio(
            f"回答を選択してください（{idx+1}/{num_q}）",
            q["choices"],
            key=f"q_{idx}"
        )

        if st.button(f"回答する {idx+1}", key=f"btn_{idx}"):
            if user_answer == q["answer"]:
                # 正解
                st.success("正解！ +1pt")
                st.session_state.points += 1
                st.session_state.streak += 1
                st.session_state.play_animation = True  # ← アニメーション用フラグ

                # 連勝ボーナス
                if st.session_state.streak == 5:
                    st.session_state.points += 3
                    st.info("🔥 5連勝ボーナス +3pt")
                if st.session_state.streak == 10:
                    st.session_state.points += 10
                    st.info("🔥 10連勝ボーナス +10pt")
                if st.session_state.streak == 20:
                    st.session_state.points += 30
                    st.info("🔥 20連勝ボーナス +30pt")

            else:
                # 不正解
                st.error("不正解… -1pt")
                st.session_state.points -= 1
                st.session_state.streak = 0
                st.session_state.wrong_questions.append(q)

    # -------------------------
    # 間違い直し（練習問題のみ）
    # -------------------------
    if st.session_state.mode == "practice" and len(st.session_state.wrong_questions) > 0:
        st.divider()
        st.subheader("📘 間違い直し")

        for idx, q in enumerate(st.session_state.wrong_questions):
            st.write(f"### {q['q']}")
            user_answer = st.radio(
                f"復習問題（{idx+1}/{len(st.session_state.wrong_questions)}）",
                q["choices"],
                key=f"fix_{idx}"
            )

            if st.button(f"回答する（復習） {idx+1}", key=f"fix_btn_{idx}"):
                if user_answer == q["answer"]:
                    st.success("正解！")
                else:
                    st.error("まだ違う…")

    # -------------------------
    # テスト合格判定
    # -------------------------
    if st.session_state.mode == "test":
        correct_count = sum(
            1 for idx, q in enumerate(questions)
            if st.session_state.get(f"q_{idx}") == q["answer"]
        )

        st.write(f"### テスト結果：{correct_count} / 10")

        if correct_count >= 9:
            st.success("🎉 合格！ランクアップ！")
            st.session_state.rank += 1
            st.session_state.points += 900 if correct_count == 9 else 1200
        else:
            st.error("不合格… また挑戦しよう！")
