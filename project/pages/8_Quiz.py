import os
import random
import json
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client, Client

# ============================
# Supabase 接続
# ============================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================
# ランク定義（テスト合格でランクアップ）
# ============================
RANK_ORDER = ["F","E","D","C","B","A","A+","AA","S","SS","SSS","LEGEND"]

TEST_COUNTS = {
    "F": 5,
    "E": 15,
    "D": 25,
    "C": 35,
    "B": 45,
    "A": 55,
    "A+": 65,
    "AA": 75,
    "S": 85,
    "SS": 95,
    "SSS": 105,
    "LEGEND": 100
}

RANK_COLORS = {
    "F": "blue",
    "E": "blue",
    "D": "blue",
    "C": "blue",
    "B": "green",
    "A": "green",
    "A+": "green",
    "AA": "red",
    "S": "red",
    "SS": "red",
    "SSS": "red",
    "LEGEND": "gold"
}

def next_rank(current):
    idx = RANK_ORDER.index(current)
    if idx < len(RANK_ORDER) - 1:
        return RANK_ORDER[idx + 1]
    return current

# ============================
# JSON → 配列変換（choices用）
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
    res = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
    if res.data:
        return res.data[0]

    profile = {
        "user_id": user_id,
        "score": 0,              # スコアは演出用に残す
        "max_combo": 0,
        "rank": "F",
        "title": None,
        "legend_flag": False
    }
    supabase.table("profiles").insert(profile).execute()
    return profile

def save_profile(profile):
    supabase.table("profiles").update(profile).eq("user_id", profile["user_id"]).execute()

# ============================
# 問題読み込み系
# ============================
def load_questions_by_rank(rank):
    res = supabase.table("questions").select("*").execute()
    all_q = [fix_choices(q) for q in res.data]

    # rank_required が自分のランク以下のものだけ出題
    order = RANK_ORDER
    return [q for q in all_q if order.index(q["rank_required"]) <= order.index(rank)]

def load_mistakes(user_id):
    res = supabase.table("mistakes").select("*").eq("user_id", user_id).execute()
    ids = [m["question_id"] for m in res.data]
    if not ids:
        return []
    q = supabase.table("questions").select("*").in_("id", ids).execute()
    return [fix_choices(item) for item in q.data]

def load_solved(user_id):
    res = supabase.table("solved").select("*").eq("user_id", user_id).execute()
    ids = [s["question_id"] for s in res.data]
    if not ids:
        return []
    q = supabase.table("questions").select("*").in_("id", ids).execute()
    return [fix_choices(item) for item in q.data]

# ============================
# トーテム演出（HTML）
# ============================
circle_effect = """<!DOCTYPE html><html><head><style>
body{margin:0;background:white;overflow:hidden;}
.scene{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center;perspective:900px;transform:translateY(-140px);}
.totem{position:relative;width:160px;height:160px;transform-style:preserve-3d;animation:spinIn 3.2s ease-out,float 4s ease-in-out infinite 3.2s,vanish 1.6s ease-in-out 7.0s forwards;}
.core{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:100px;height:100px;border-radius:50%;border:12px solid #00ff88;background:transparent;box-shadow:0 0 25px #00ff88,0 0 55px #ffee55,0 0 90px rgba(255,255,120,.9);animation:pulse 2.4s ease-in-out infinite;}
.particle{position:absolute;width:14px;height:14px;border-radius:50%;animation:spread 2.2s ease-out infinite;}
.green{background:#00ff88;}
.yellow{background:#ffee55;}
.p1,.p2,.p3,.p4,.p5,.p6{left:50%;top:50%;}
@keyframes spinIn{0%{transform:scale(0) rotateY(0deg);opacity:0;}40%{transform:scale(0.7) rotateY(180deg);opacity:1;}100%{transform:scale(1) rotateY(720deg);opacity:1;}}
@keyframes float{0%{transform:translateY(0);}50%{transform:translateY(-16px);}100%{transform:translateY(0);}}
@keyframes pulse{0%{transform:translate(-50%,-50%) scale(1);}50%{transform:translate(-50%,-50%) scale(1.35);}100%{transform:translate(-50%,-50%) scale(1);}}
@keyframes spread{0%{transform:translate(-50%,-50%) scale(0.3);opacity:1;}100%{transform:translate(var(--x), var(--y)) scale(1.8);opacity:0;}}
@keyframes vanish{0%{transform:scale(1) translateY(0);opacity:1;}100%{transform:scale(0.2) translateY(160px);opacity:0;}}
</style>
<div class="scene"><div class="totem">
<div class="particle green p1" style="--x:-200px; --y:-300px;"></div>
<div class="particle yellow p2" style="--x:240px; --y:-320px;"></div>
<div class="particle green p3" style="--x:-260px; --y:120px;"></div>
<div class="particle yellow p4" style="--x:280px; --y:140px;"></div>
<div class="particle green p5" style="--x:-140px; --y:260px;"></div>
<div class="particle yellow p6" style="--x:160px; --y:240px;"></div>
<div class="core"></div></div></div></html>
"""

cross_effect = """<!DOCTYPE html><html><head><style>
body{margin:0;background:white;overflow:hidden;}
.scene{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center;perspective:900px;transform:translateY(-140px);}
.totem{position:relative;width:160px;height:160px;transform-style:preserve-3d;animation:spinIn 3.2s ease-out,float 4s ease-in-out infinite 3.2s,vanish 1.6s ease-in-out 7.0s forwards;}
.core{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:170px;height:170px;}
.core::before,.core::after{content:"";position:absolute;left:50%;top:50%;width:170px;height:28px;background:#ff2b2b;box-shadow:0 0 25px #ff2b2b,0 0 45px #ff7b00,0 0 75px rgba(255,120,0,.9);transform-origin:center;}
.core::before{transform:translate(-50%,-50%) rotate(45deg);}
.core::after{transform:translate(-50%,-50%) rotate(-45deg);}
.particle{position:absolute;width:14px;height:14px;border-radius:50%;animation:spread 2.2s ease-out infinite;}
.orange{background:#ff7b00;}
.red{background:#ff2b2b;}
.yellow{background:#ffee55;}
.p1,.p2,.p3,.p4,.p5,.p6{left:50%;top:50%;}
@keyframes spinIn{0%{transform:scale(0) rotateY(0deg);opacity:0;}40%{transform:scale(0.7) rotateY(180deg);opacity:1;}100%{transform:scale(1) rotateY(720deg);opacity:1;}}
@keyframes float{0%{transform:translateY(0);}50%{transform:translateY(-16px);}100%{transform:translateY(0);}}
@keyframes spread{0%{transform:translate(-50%,-50%) scale(0.3);opacity:1;}100%{transform:translate(var(--x), var(--y)) scale(1.8);opacity:0;}}
@keyframes vanish{0%{transform:scale(1) translateY(0);opacity:1;}100%{transform:scale(0.2) translateY(160px);opacity:0;}}
</style>
<div class="scene"><div class="totem">
<div class="particle orange p1" style="--x:-200px; --y:-300px;"></div>
<div class="particle red p2" style="--x:240px; --y:-320px;"></div>
<div class="particle yellow p3" style="--x:-260px; --y:120px;"></div>
<div class="particle orange p4" style="--x:280px; --y:140px;"></div>
<div class="particle red p5" style="--x:-140px; --y:260px;"></div>
<div class="particle yellow p6" style="--x:160px; --y:240px;"></div>
<div class="core"></div></div></div></html>
"""

# ============================
# Streamlit UI 基本設定
# ============================
st.set_page_config(page_title="防災クイズRPG", page_icon="⛑️", layout="centered")

st.markdown("""
<style>
div.stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
</style>
""", unsafe_allow_html=True)

# ============================
# セッション初期化
# ============================
if "user_id" not in st.session_state:
    st.session_state.user_id = "player_1"

profile = load_profile(st.session_state.user_id)

if "score" not in st.session_state:
    st.session_state.score = profile["score"]
if "combo" not in st.session_state:
    st.session_state.combo = 0
if "max_combo" not in st.session_state:
    st.session_state.max_combo = profile["max_combo"]
if "answered" not in st.session_state:
    st.session_state.answered = False
if "current_questions" not in st.session_state:
    st.session_state.current_questions = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "test_correct" not in st.session_state:
    st.session_state.test_correct = 0

# ============================
# ホーム
# ============================
st.title("防災クイズRPG")

mode = st.selectbox("モードを選んでください", ["ホーム", "練習", "復習", "テスト", "ステータス"])

current_rank = profile["rank"]
rank_color = RANK_COLORS[current_rank]
test_count = TEST_COUNTS[current_rank]

# ============================
# ステータス画面
# ============================
if mode == "ステータス":
    title = profile["title"] or ("最高権力者" if profile["legend_flag"] else "なし")

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

    # 管理者用：即レジェンド化ボタン
if st.button("レジェンドになる（管理者用）"):
    profile["rank"] = "LEGEND"
    profile["title"] = "最高権力者"
    profile["legend_flag"] = True
    save_profile(profile)

    st.balloons()
    st.success("レジェンド達成！称号：最高権力者")

# ============================
# 練習モード
# ============================
elif mode == "練習":
    questions = load_questions_by_rank(current_rank)

    if not questions:
        st.info("まだ問題が登録されていません。Supabaseのquestionsテーブルに問題を追加してね。")
    else:
        if not st.session_state.current_questions:
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
            if st.button("送信", key=f"practice_send_{st.session_state.index}"):
                st.session_state.answered = True

                supabase.table("solved").upsert({
                    "user_id": st.session_state.user_id,
                    "question_id": q["id"]
                }).execute()

                if choice == q["answer"]:
                    st.success("正解！ +1pt")
                    st.session_state.score += 1
                    st.session_state.combo += 1

                    if st.session_state.combo > st.session_state.max_combo:
                        st.session_state.max_combo = st.session_state.combo

                    components.html(circle_effect, height=700, scrolling=False)

                else:
                    st.error("不正解…")
                    st.session_state.combo = 0

                    supabase.table("mistakes").upsert({
                        "user_id": st.session_state.user_id,
                        "question_id": q["id"]
                    }).execute()

                    components.html(cross_effect, height=700, scrolling=False)

        if st.session_state.answered:
            if st.button("次の問題へ", key=f"practice_next_{st.session_state.index}"):
                st.session_state.index += 1
                st.session_state.answered = False

                profile["score"] = st.session_state.score
                profile["max_combo"] = st.session_state.max_combo
                save_profile(profile)

                st.rerun()

# ============================
# 復習モード
# ============================
elif mode == "復習":
    mistakes = load_mistakes(st.session_state.user_id)

    if not mistakes:
        st.info("復習する問題はありません！")
    else:
        q = random.choice(mistakes)
        st.subheader("復習問題")
        st.write("### " + q["question"])
        choice = st.radio("選択肢を選んでね", q["choices"], key=f"review_{q['id']}")

        if st.button("送信", key=f"review_send_{q['id']}"):
            if choice == q["answer"]:
                st.success("正解！復習クリア！")
                supabase.table("mistakes").delete().eq("user_id", st.session_state.user_id).eq("question_id", q["id"]).execute()
                components.html(circle_effect, height=700, scrolling=False)
            else:
                st.error("不正解…また復習しよう")
                components.html(cross_effect, height=700, scrolling=False)

# ============================
# テストモード（合格でランクアップ）
# ============================
elif mode == "テスト":
    if current_rank == "LEGEND":
        solved = load_solved(st.session_state.user_id)
        if len(solved) < 100:
            st.warning("LEGENDテストには100問必要です。まず練習モードで問題を解いてください。")
            st.stop()
        questions = random.sample(solved, 100)
    else:
        questions_all = load_questions_by_rank(current_rank)
        if not questions_all:
            st.info("まだ問題が登録されていません。Supabaseのquestionsテーブルに問題を追加してね。")
            st.stop()
        questions = random.sample(questions_all, min(test_count, len(questions_all)))

    if not st.session_state.current_questions:
        st.session_state.current_questions = questions
        st.session_state.index = 0
        st.session_state.answered = False
        st.session_state.test_correct = 0

    if st.session_state.index >= len(st.session_state.current_questions):
        total = len(st.session_state.current_questions)
        correct = st.session_state.test_correct
        rate = correct / total if total > 0 else 0.0
        rounded = round(rate, 1)

        st.write(f"正解数：{correct}/{total}（正答率 {rounded*100:.1f}%）")

        if rounded >= 0.9:
            st.success("合格！ランクアップ！")
            new_rank = next_rank(current_rank)
            profile["rank"] = new_rank

            if new_rank == "LEGEND":
                profile["title"] = "最高権力者"
                profile["legend_flag"] = True
                st.balloons()
                st.success("LEGEND達成！称号：最高権力者")

            save_profile(profile)
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
        if st.button("送信", key=f"test_send_{st.session_state.index}"):
            st.session_state.answered = True

            if choice == q["answer"]:
                st.success("正解！")
                st.session_state.test_correct += 1
                components.html(circle_effect, height=700, scrolling=False)
            else:
                st.error("不正解…")
                components.html(cross_effect, height=700, scrolling=False)

    if st.session_state.answered:
        if st.button("次の問題へ", key=f"test_next_{st.session_state.index}"):
            st.session_state.index += 1
            st.session_state.answered = False
            st.rerun()

# ============================
# ホーム表示
# ============================
else:
    st.write("モードを選んでね")
