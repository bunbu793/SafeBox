import os
import random
import json
import streamlit as st
import streamlit.components.v1 as components
from uuid import uuid4
from supabase import create_client

# ============================
# Supabase 接続
# ============================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# family_settings を読み込む
settings_res = supabase.table("family_settings").select("*").eq("family_code", st.session_state["family_code"]).execute()

if len(settings_res.data) > 0:
    settings = settings_res.data[0]

    # 言語設定
    st.session_state["language"] = settings.get("language", "日本語")

    # テーマ設定
    st.session_state["theme"] = settings.get("theme", "Light")

    # テーマCSSを適用
    theme = st.session_state["theme"]

    if theme == "Dark":
        st.markdown("""
        <style>
        body { background-color: #111 !important; color: #eee !important; }
        </style>
        """, unsafe_allow_html=True)

    elif theme == "Cyber":
        st.markdown("""
        <style>
        body {
            background-color: #000 !important;
            color: #0affff !important;
            font-family: 'Consolas', monospace !important;
        }
        </style>
        """, unsafe_allow_html=True)

# ============================
# 演出 HTML（そのまま）
# ============================
circle_effect = """<html><head><style>
body{margin:0;background:white;overflow:hidden;}
.scene{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center;perspective:900px;transform:translateY(-140px);}
.totem{position:relative;width:160px;height:160px;transform-style:preserve-3d;animation:spinIn 3.2s ease-out,float 4s ease-in-out infinite 3.2s,vanish 1.6s ease-in-out 7.0s forwards;}
.core{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:100px;height:100px;border-radius:50%;border:12px solid #00ff88;box-shadow:0 0 25px #00ff88,0 0 55px #ffee55;}
.particle{position:absolute;width:14px;height:14px;border-radius:50%;animation:spread 2.2s ease-out infinite;}
.green{background:#00ff88;} .yellow{background:#ffee55;}
.p1,.p2,.p3,.p4,.p5,.p6{left:50%;top:50%;}
@keyframes spinIn{0%{transform:scale(0);opacity:0;}40%{transform:scale(0.7);}100%{transform:scale(1);}}
@keyframes float{0%{transform:translateY(0);}50%{transform:translateY(-16px);}100%{transform:translateY(0);}}
@keyframes spread{0%{transform:translate(-50%,-50%) scale(0.3);}100%{transform:translate(var(--x), var(--y)) scale(1.8);opacity:0;}}
@keyframes vanish{0%{opacity:1;}100%{opacity:0;}}
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

cross_effect = """<html><head><style>
body{margin:0;background:white;overflow:hidden;}
.scene{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center;perspective:900px;transform:translateY(-140px);}
.totem{position:relative;width:160px;height:160px;transform-style:preserve-3d;animation:spinIn 3.2s ease-out,float 4s ease-in-out infinite 3.2s,vanish 1.6s ease-in-out 7.0s forwards;}
.core{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:170px;height:170px;}
.core::before,.core::after{content:"";position:absolute;left:50%;top:50%;width:170px;height:28px;background:#ff2b2b;}
.core::before{transform:translate(-50%,-50%) rotate(45deg);}
.core::after{transform:translate(-50%,-50%) rotate(-45deg);}
.particle{position:absolute;width:14px;height:14px;border-radius:50%;animation:spread 2.2s ease-out infinite;}
.orange{background:#ff7b00;} .red{background:#ff2b2b;} .yellow{background:#ffee55;}
.p1,.p2,.p3,.p4,.p5,.p6{left:50%;top:50%;}
@keyframes spinIn{0%{transform:scale(0);}40%{transform:scale(0.7);}100%{transform:scale(1);}}
@keyframes float{0%{transform:translateY(0);}50%{transform:translateY(-16px);}100%{transform:translateY(0);}}
@keyframes spread{0%{transform:translate(-50%,-50%) scale(0.3);}100%{transform:translate(var(--x), var(--y)) scale(1.8);opacity:0;}}
@keyframes vanish{0%{opacity:1;}100%{opacity:0;}}
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
# ログイン画面（8_Quiz.py 内で完結）
# ============================
if "user_id" not in st.session_state:
    st.title("防災クイズRPG - ログイン")

    mode = st.radio("選択してください", ["ゲストとしてプレイ", "アカウント登録", "ログイン"])

    if mode == "ゲストとしてプレイ":
        if st.button("ゲストで開始"):
            st.session_state["user_id"] = "guest_" + uuid4().hex[:8]
            st.session_state["is_guest"] = True
            st.rerun()

    elif mode == "アカウント登録":
        new_code = st.text_input("新しい個人コード（ID）")
        new_pass = st.text_input("パスワード", type="password")

        if st.button("登録"):
            if not new_code or not new_pass:
                st.error("ID とパスワードを入力してね")
                st.stop()

            res = supabase.table("profiles").select("*").eq("user_id", new_code).execute()
            if res.data:
                st.error("このIDは既に使われています")
                st.stop()

            profile = {
                "user_id": new_code,
                "password": new_pass,
                "score": st.session_state.get("score", 0),
                "max_combo": st.session_state.get("max_combo", 0),
                "rank": st.session_state.get("rank", "F"),
                "title": st.session_state.get("title", None),
                "legend_flag": st.session_state.get("legend_flag", False)
            }

            supabase.table("profiles").insert(profile).execute()

            st.session_state["user_id"] = new_code
            st.session_state["is_guest"] = False
            st.success("登録完了！")
            st.rerun()

    elif mode == "ログイン":
        code = st.text_input("個人コード（ID）")
        pw = st.text_input("パスワード", type="password")

        if st.button("ログイン"):
            res = supabase.table("profiles").select("*").eq("user_id", code).execute()
            if not res.data:
                st.error("ID が存在しません")
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
# ログイン後
# ============================
user_id = st.session_state["user_id"]
is_guest = st.session_state.get("is_guest", False)

st.info(f"ログイン中：{user_id}")

# ============================
# ランク定義
# ============================
RANK_ORDER = ["F","E","D","C","B","A","A+","AA","S","SS","SSS","LEGEND"]
TEST_COUNTS = {"F":5,"E":15,"D":25,"C":35,"B":45,"A":55,"A+":65,"AA":75,"S":85,"SS":95,"SSS":105,"LEGEND":100}
RANK_COLORS = {"F":"blue","E":"blue","D":"blue","C":"blue","B":"green","A":"green","A+":"green","AA":"red","S":"red","SS":"red","SSS":"red","LEGEND":"gold"}

def next_rank(current):
    idx = RANK_ORDER.index(current)
    return RANK_ORDER[min(idx+1, len(RANK_ORDER)-1)]

# ============================
# JSON → 配列変換（選択肢シャッフル）
# ============================
def fix_choices(q):
    # choices が文字列なら JSON に変換
    if isinstance(q.get("choices"), str):
        try:
            q["choices"] = json.loads(q["choices"])
        except:
            pass

    # 正解を記録（例： "a"）
    correct = q["answer"]

    # シャッフル
    if isinstance(q.get("choices"), list):
        random.shuffle(q["choices"])

    # 正解は文字列のままで OK（Supabase の answer は "a" のまま）
    q["answer"] = correct

    return q

#=============================
# プロフィール読み込み
# ============================
def load_profile(uid):
    if is_guest:
        return {
            "user_id": uid,
            "password": "",
            "score": st.session_state.get("score", 0),
            "max_combo": st.session_state.get("max_combo", 0),
            "rank": st.session_state.get("rank", "F"),
            "title": st.session_state.get("title", None),
            "legend_flag": st.session_state.get("legend_flag", False)
        }

    res = supabase.table("profiles").select("*").eq("user_id", uid).execute()
    if res.data:
        return res.data[0]

    profile = {
        "user_id": uid,
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

def load_mistakes(uid):
    if is_guest:
        return []
    res = supabase.table("mistakes").select("*").eq("user_id", uid).execute()
    ids = [m["question_id"] for m in res.data]
    if not ids:
        return []
    q = supabase.table("questions").select("*").in_("id", ids).execute()
    return [fix_choices(item) for item in q.data]

def load_solved(uid):
    if is_guest:
        return []
    res = supabase.table("solved").select("*").eq("user_id", uid).execute()
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
st.title("防災クイズRPG")

mode = st.selectbox("モードを選んでください", ["ホーム", "練習", "復習", "テスト", "ステータス"])

current_rank = st.session_state.rank
rank_color = RANK_COLORS[current_rank]
test_count = TEST_COUNTS[current_rank]

# ============================
# ステータス画面（サイバー風）
# ============================
if mode == "ステータス":
    title = st.session_state.title or ("最高権力者" if st.session_state.legend_flag else "なし")
    rank_color = RANK_COLORS[current_rank]

    html = f"""
    <div style="
        padding: 30px;
        border-radius: 18px;
        background: radial-gradient(circle at top left, #0f0f0f, #000000 60%);
        border: 2px solid {rank_color};
        box-shadow: 0 0 25px {rank_color}, inset 0 0 25px #111;
        font-family: 'Consolas', 'Roboto Mono', monospace;
        color: #0affff;
        position: relative;
        overflow: hidden;
        width: 100%;
    ">

        <div style="
            position:absolute;
            top:0; left:0;
            width:100%; height:100%;
            background-image: linear-gradient(#0a0a0a 1px, transparent 1px),
                              linear-gradient(90deg, #0a0a0a 1px, transparent 1px);
            background-size: 22px 22px;
            opacity:0.25;
            z-index:0;
        "></div>

        <h2 style="
            color:{rank_color};
            text-shadow: 0 0 12px {rank_color};
            margin-bottom: 20px;
            position:relative;
            z-index:2;
        ">
            ⚡ CYBER STATUS MODULE ⚡
        </h2>

        <div style="font-size:18px; line-height:1.9; position:relative; z-index:2;">
            <b style="color:#00eaff;">▶ RANK :</b>
            <span style="color:{rank_color}; font-size:24px; text-shadow:0 0 10px {rank_color};">
                <b>{current_rank}</b>
            </span><br>

            <b style="color:#00eaff;">▶ SCORE :</b> {st.session_state.score} pt<br>
            <b style="color:#00eaff;">▶ MAX COMBO :</b> {st.session_state.max_combo} 回<br>
            <b style="color:#00eaff;">▶ TEST SIZE :</b> {test_count} 問<br>

            <b style="color:#00eaff;">▶ TITLE :</b>
            <span style="color:#ff00ff; text-shadow:0 0 10px #ff00ff;">
                {title}
            </span>
        </div>

        <div style="
            position:absolute;
            bottom:10px; left:10px;
            width:90%;
            height:2px;
            background:linear-gradient(90deg, transparent, {rank_color}, transparent);
            opacity:0.7;
            z-index:2;
        "></div>

    </div>
    """

    components.html(html, height=400, scrolling=False)

    # ランク進行バー
    rank_index = RANK_ORDER.index(current_rank)
    progress = rank_index / (len(RANK_ORDER) - 1)

    st.markdown("""
    <h4 style="color:#00eaff; font-family:Consolas;">▶ RANK PROGRESS</h4>
    """, unsafe_allow_html=True)

    st.progress(progress)

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
                    supabase.table("solved").upsert({"user_id": user_id, "question_id": q["id"]}).execute()

        if choice == q["answer"]:
            st.success("正解！ +1pt")

            # コンボ処理
            st.session_state.combo = st.session_state.get("combo", 0) + 1
            st.session_state.max_combo = max(st.session_state.max_combo, st.session_state.combo)

            st.session_state.score += 1
            components.html(circle_effect, height=700, scrolling=False)

        else:
            st.error("不正解…")

            # コンボリセット
            st.session_state.combo = 0

            if not is_guest:
                supabase.table("mistakes").upsert({
                    "user_id": user_id,
                    "question_id": q["id"]
                }).execute()

            components.html(cross_effect, height=700, scrolling=False)

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
                    components.html(circle_effect, height=700, scrolling=False)
                else:
                    st.error("不正解…また復習しよう")
                    components.html(cross_effect, height=700, scrolling=False)

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
                components.html(circle_effect, height=700, scrolling=False)
            else:
                st.error("不正解…")
                components.html(cross_effect, height=700, scrolling=False)

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

    # ============================
    # ログアウトボタン
    # ============================
    if st.button("ログアウト"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("ログアウトしました")
        st.rerun()