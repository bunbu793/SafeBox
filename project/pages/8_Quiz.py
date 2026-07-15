import os
import random
import json
import streamlit as st
import streamlit.components.v1 as components
from uuid import uuid4
from supabase import create_client, Client

# ============================
# Supabase 接続
# ============================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================
# ログイン画面（このファイルだけで完結）
# ============================
if "user_id" not in st.session_state:
    st.title("防災クイズ - ログイン")

    mode = st.radio("選択してください", ["ゲストとしてプレイ", "アカウント登録", "ログイン"])

    # --------------------------
    # ゲストとしてプレイ
    # --------------------------
    if mode == "ゲストとしてプレイ":
        if st.button("ゲストで開始"):
            st.session_state["user_id"] = "guest_" + uuid4().hex[:8]
            st.session_state["is_guest"] = True
            st.rerun()

    # --------------------------
    # アカウント登録（ID + パスワード）
    # --------------------------
    elif mode == "アカウント登録":
        new_code = st.text_input("新しい個人コード（ID）を入力してください")
        new_pass = st.text_input("パスワードを入力してください", type="password")

        if st.button("登録"):
            if not new_code or not new_pass:
                st.error("ID とパスワードを入力してください")
                st.stop()

            # ID 重複チェック
            res = supabase.table("profiles").select("*").eq("user_id", new_code).execute()
            if res.data:
                st.error("このIDは既に使われています")
                st.stop()

            # ゲストデータ引き継ぎ
            if st.session_state.get("is_guest", False):
                profile = {
                    "user_id": new_code,
                    "password": new_pass,
                    "score": st.session_state.get("score", 0),
                    "max_combo": st.session_state.get("max_combo", 0),
                    "rank": st.session_state.get("rank", "F"),
                    "title": st.session_state.get("title", None),
                    "legend_flag": st.session_state.get("legend_flag", False)
                }
            else:
                profile = {
                    "user_id": new_code,
                    "password": new_pass,
                    "score": 0,
                    "max_combo": 0,
                    "rank": "F",
                    "title": None,
                    "legend_flag": False
                }

            supabase.table("profiles").insert(profile).execute()

            st.session_state["user_id"] = new_code
            st.session_state["is_guest"] = False
            st.success("登録完了！")
            st.rerun()

    # --------------------------
    # ログイン（ID + パスワード）
    # --------------------------
    elif mode == "ログイン":
        code = st.text_input("個人コード（ID）を入力してください")
        pw = st.text_input("パスワードを入力してください", type="password")

        if st.button("ログイン"):
            res = supabase.table("profiles").select("*").eq("user_id", code).execute()

            if not res.data:
                st.error("このIDは存在しません")
                st.stop()

            user = res.data[0]

            if user["password"] != pw:
                st.error("パスワードが違います")
                st.stop()

            st.session_state["user_id"] = code
            st.session_state["is_guest"] = False
            st.success("ログイン成功！")
            st.rerun()

    st.stop()

# ============================
# ログイン後の処理
# ============================
user_id = st.session_state["user_id"]
is_guest = st.session_state.get("is_guest", False)

st.info(f"ログイン中：{user_id}")

# ============================
# ランク定義
# ============================
RANK_ORDER = ["F","E","D","C","B","A","A+","AA","S","SS","SSS","LEGEND"]

TEST_COUNTS = {
    "F": 5, "E": 15, "D": 25, "C": 35, "B": 45,
    "A": 55, "A+": 65, "AA": 75, "S": 85,
    "SS": 95, "SSS": 105, "LEGEND": 100
}

RANK_COLORS = {
    "F": "blue", "E": "blue", "D": "blue", "C": "blue",
    "B": "green", "A": "green", "A+": "green",
    "AA": "red", "S": "red", "SS": "red", "SSS": "red",
    "LEGEND": "gold"
}

def next_rank(current):
    idx = RANK_ORDER.index(current)
    return RANK_ORDER[min(idx + 1, len(RANK_ORDER) - 1)]

# ============================
# JSON → 配列変換
# ============================
def fix_choices(q):
    if isinstance(q.get("choices"), str):
        try:
            q["choices"] = json.loads(q["choices"])
        except:
            pass
    return q

# ============================
# プロフィール読み込み／保存
# ============================
def load_profile(user_id):
    if is_guest:
        return {
            "user_id": user_id,
            "score": st.session_state.get("score", 0),
            "max_combo": st.session_state.get("max_combo", 0),
            "rank": st.session_state.get("rank", "F"),
            "title": st.session_state.get("title", None),
            "legend_flag": st.session_state.get("legend_flag", False)
        }

    res = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
    if res.data:
        return res.data[0]

    profile = {
        "user_id": user_id,
        "password": "",
        "score": 0,
        "max_combo": 0,
        "rank": "F",
        "title": None,
        "legend_flag": False
    }
    supabase.table("profiles").insert(profile).execute()
    return profile

def save_profile(profile):
    if is_guest:
        return
    supabase.table("profiles").update(profile).eq("user_id", profile["user_id"]).execute()

# ============================
# 問題読み込み
# ============================
def load_questions_by_rank(rank):
    res = supabase.table("questions").select("*").execute()
    all_q = [fix_choices(q) for q in res.data]
    return [q for q in all_q if RANK_ORDER.index(q["rank_required"]) <= RANK_ORDER.index(rank)]

def load_mistakes(user_id):
    if is_guest:
        return []
    res = supabase.table("mistakes").select("*").eq("user_id", user_id).execute()
    ids = [m["question_id"] for m in res.data]
    if not ids:
        return []
    q = supabase.table("questions").select("*").in_("id", ids).execute()
    return [fix_choices(item) for item in q.data]

def load_solved(user_id):
    if is_guest:
        return []
    res = supabase.table("solved").select("*").eq("user_id", user_id).execute()
    ids = [s["question_id"] for s in res.data]
    if not ids:
        return []
    q = supabase.table("questions").select("*").in_("id", ids).execute()
    return [fix_choices(item) for item in q.data]

# ============================
# セッション初期化
# ============================
profile = load_profile(user_id)

st.session_state.score = profile["score"]
st.session_state.max_combo = profile["max_combo"]
st.session_state.rank = profile["rank"]
st.session_state.title = profile["title"]
st.session_state.legend_flag = profile["legend_flag"]

# ============================
# ホーム
# ============================
st.title("防災クイズ")

mode = st.selectbox("モードを選んでください", ["ホーム", "練習", "復習", "テスト", "ステータス"])

current_rank = st.session_state.rank
rank_color = RANK_COLORS[current_rank]
test_count = TEST_COUNTS[current_rank]

# ============================
# ステータス画面
# ============================
if mode == "ステータス":
    title = st.session_state.title or ("最高権力者" if st.session_state.legend_flag else "なし")

    st.markdown(f"""
    <div style='border:3px solid {rank_color}; padding:20px; border-radius:12px;'>
        <h3 style='color:{rank_color};'>ステータス</h3>
        <b>ランク：</b> {current_rank}<br>
        <b>スコア：</b> {st.session_state.score} pt<br>
        <b>最大連続正解：</b> {st.session_state.max_combo} 回<br>
        <b>テスト問題数：</b> {test_count} 問<br>
        <b>称号：</b> {title}
    </div>
    """, unsafe_allow_html=True)

# ============================
# 練習モード
# ============================
elif mode == "練習":
    questions = load_questions_by_rank(current_rank)

    if not questions:
        st.info("まだ問題が登録されていません。")
    else:
        if "current_questions" not in st.session_state or not st.session_state.current_questions:
            st.session_state.current_questions = random.sample(questions, min(10, len(questions)))
            st.session_state.index = 0
            st.session_state.answered = False

        if st.session_state.index >= len(st.session_state.current_questions):
            st.session_state.current_questions = []
            st.session_state.index = 0
            st.session_state.answered = False
            st.rerun()

        q = st.session_state.current_questions[st.session_state.index]

        st.subheader(f"問題 {st.session_state.index+1}/{len(st.session_state.current_questions)}")
        st.write("### " + q["question"])

        choice = st.radio("選択肢を選んでね", q["choices"], key=f"practice_{st.session_state.index}")

        if not st.session_state.answered:
            if st.button("送信"):
                st.session_state.answered = True

                if not is_guest:
                    supabase.table("solved").upsert({
                        "user_id": user_id,
                        "question_id": q["id"]
                    }).execute()

                if choice == q["answer"]:
                    st.success("正解！ +1pt")
                    st.session_state.score += 1
                    st.session_state.max_combo += 1
                else:
                    st.error("不正解…")
                    st.session_state.max_combo = 0
                    if not is_guest:
                        supabase.table("mistakes").upsert({
                            "user_id": user_id,
                            "question_id": q["id"]
                        }).execute()

        if st.session_state.answered:
            if st.button("次の問題へ"):
                st.session_state.index += 1
                st.session_state.answered = False

                save_profile({
                    "user_id": user_id,
                    "password": profile.get("password", ""),
                    "score": st.session_state.score,
                    "max_combo": st.session_state.max_combo,
                    "rank": st.session_state.rank,
                    "title": st.session_state.title,
                    "legend_flag": st.session_state.legend_flag
                })

                st.rerun()

# ============================
# 復習モード
# ============================
elif mode == "復習":
    if is_guest:
        st.info("ゲストは復習機能を使えません。")
    else:
        mistakes = load_mistakes(user_id)

        if not mistakes:
            st.info("復習する問題はありません！")
        else:
            q = random.choice(mistakes)
            st.subheader("復習問題")
            st.write("### " + q["question"])
            choice = st.radio("選択肢を選んでね", q["choices"], key=f"review_{q['id']}")

            if st.button("送信"):
                if choice == q["answer"]:
                    st.success("正解！復習クリア！")
                    supabase.table("mistakes").delete().eq("user_id", user_id).eq("question_id", q["id"]).execute()
                else:
                    st.error("不正解…また復習しよう")

# ============================
# テストモード
# ============================
elif mode == "テスト":
    questions_all = load_questions_by_rank(current_rank)
    questions = random.sample(questions_all, min(test_count, len(questions_all)))

    if "current_questions" not in st.session_state or not st.session_state.current_questions:
        st.session_state.current_questions = questions
        st.session_state.index = 0
        st.session_state.answered = False
        st.session_state.test_correct = 0

    if st.session_state.index >= len(st.session_state.current_questions):
        total = len(st.session_state.current_questions)
        correct = st.session_state.test_correct
        rate = correct / total
        rounded = round(rate, 1)

        st.write(f"正解数：{correct}/{total}（正答率 {rounded*100:.1f}%）")

        if rounded >= 0.9:
            st.success("合格！ランクアップ！")
            st.session_state.rank = next_rank(st.session_state.rank)

            if st.session_state.rank == "LEGEND":
                st.session_state.title = "最高権力者"
                st.session_state.legend_flag = True
                st.balloons()

            save_profile({
                "user_id": user_id,
                "password": profile.get("password", ""),
                "score": st.session_state.score,
                "max_combo": st.session_state.max_combo,
                "rank": st.session_state.rank,
                "title": st.session_state.title,
                "legend_flag": st.session_state.legend_flag
            })
        else:
            st.error("不合格…もう一度挑戦しよう")

        st.session_state.current_questions = []
        st.session_state.index = 0
        st.session_state.answered = False
        st.session_state.test_correct = 0
        st.stop()

    q = st.session_state.current_questions[st.session_state.index]

    st.subheader(f"テスト問題 {st.session_state.index+1}/{len(st.session_state.current_questions)}")
    st.write("### " + q["question"])

    choice = st.radio("選択肢を選んでね", q["choices"], key=f"test_{st.session_state.index}")

    if not st.session_state.answered:
        if st.button("送信"):
            st.session_state.answered = True

            if choice == q["answer"]:
                st.success("正解！")
                st.session_state.test_correct += 1
            else:
                st.error("不正解…")

    if st.session_state.answered:
        if st.button("次の問題へ"):
            st.session_state.index += 1
            st.session_state.answered = False
            st.rerun()

# ============================
# ホーム表示
# ============================
else:
    st.write("モードを選んでね")
