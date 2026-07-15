import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="防災クイズ", page_icon="⛑️", layout="centered")

# ============================
# 初期化
# ============================

if "score" not in st.session_state:
    st.session_state.score = 0

if "used" not in st.session_state:
    st.session_state.used = []

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

if "choices" not in st.session_state:
    st.session_state.choices = None

if "answered" not in st.session_state:
    st.session_state.answered = False

# ============================
# 防災クイズ
# ============================

quiz_list = [
    {"q": "地震が起きたとき、まず最初にするべき行動は？",
     "choices": ["身を守る", "外に走る", "窓を開ける", "スマホを見る"],
     "a": "身を守る"},
    {"q": "津波から避難するとき、まず向かうべき場所は？",
     "choices": ["高い場所", "海の様子を見る", "家に戻る", "車で海沿いへ行く"],
     "a": "高い場所"},
    {"q": "火災のとき煙を吸わないための姿勢は？",
     "choices": ["低い姿勢", "背伸びする", "走る", "ジャンプする"],
     "a": "低い姿勢"},
    {"q": "台風のとき危険な場所は？",
     "choices": ["川の近く", "家の中", "高台", "避難所"],
     "a": "川の近く"},
    {"q": "非常用持ち出し袋に入れるべきものは？",
     "choices": ["水・食料", "ゲーム機", "大きい家具", "観葉植物"],
     "a": "水・食料"},
    {"q": "地震のときエレベーターに乗っていたらどうする？",
     "choices": ["全階のボタンを押す", "飛び降りる", "叫ぶ", "スマホで動画を撮る"],
     "a": "全階のボタンを押す"},
    {"q": "避難所でまず確認するべきことは？",
     "choices": ["受付で登録する", "スマホの充電場所", "友達を探す", "ゲームできる場所"],
     "a": "受付で登録する"}
]

# ============================
# ポイント表示
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
        st.session_state.used = []
        remaining = quiz_list
    quiz = random.choice(remaining)
    st.session_state.used.append(quiz["q"])
    return quiz

if st.session_state.current_quiz is None:
    st.session_state.current_quiz = pick_new_quiz()
    st.session_state.choices = None
    st.session_state.answered = False

quiz = st.session_state.current_quiz

# ============================
# 選択肢シャッフル（固定）
# ============================

if st.session_state.choices is None:
    choices = quiz["choices"].copy()
    random.shuffle(choices)
    st.session_state.choices = choices
else:
    choices = st.session_state.choices

st.subheader("問題")
st.write("### " + quiz["q"])

choice = st.radio("選択肢を選んでね", choices)

# ============================
# ◯演出（HTML全部入り）
# ============================

circle_effect = """<!DOCTYPE html><html><head><style>
body{margin:0;background:white;overflow:hidden;}
.scene{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center;perspective:900px;transform:translateY(-140px);}
.totem{position:relative;width:160px;height:160px;transform-style:preserve-3d;animation:spinIn 3.2s ease-out,float 4s ease-in-out infinite 3.2s,vanish 1.6s ease-in-out 7.0s forwards;}
.core{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:100px;height:100px;border-radius:50%;border:12px solid #00ff88;background:transparent;box-shadow:0 0 25px #00ff88,0 0 55px #ffee55,0 0 90px rgba(255,255,120,.9);animation:pulse 2.4s ease-in-out infinite;}
.particle{position:absolute;width:14px;height:14px;border-radius:50%;animation:spread 2.2s ease-out infinite;}
.green{background:#00ff88;box-shadow:0 0 25px #00ff88;}
.yellow{background:#ffee55;box-shadow:0 0 25px #ffee55;}
.p1,.p2,.p3,.p4,.p5,.p6{left:50%;top:50%;}
@keyframes spinIn{0%{transform:scale(0) rotateY(0deg);opacity:0;}40%{transform:scale(0.7) rotateY(180deg);opacity:1;}100%{transform:scale(1) rotateY(720deg);opacity:1;}}
@keyframes float{0%{transform:translateY(0);}50%{transform:translateY(-16px);}100%{transform:translateY(0);}}
@keyframes pulse{0%{transform:translate(-50%,-50%) scale(1);}50%{transform:translate(-50%,-50%) scale(1.35);}100%{transform:translate(-50%,-50%) scale(1);}}
@keyframes spread{0%{transform:translate(-50%,-50%) scale(0.3);opacity:1;}100%{transform:translate(var(--x), var(--y)) scale(1.8);opacity:0;}}
@keyframes vanish{0%{transform:scale(1) translateY(0);opacity:1;filter:blur(0px);}100%{transform:scale(0.2) translateY(160px);opacity:0;filter:blur(6px);}}
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

# ============================
# ✖演出（170px巨大バツ）
# ============================

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
@keyframes vanish{0%{transform:scale(1) translateY(0);opacity:1;filter:blur(0px);}100%{transform:scale(0.2) translateY(160px);opacity:0;filter:blur(6px);}}
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
# 判定ボタン
# ============================

if st.button("送信") and not st.session_state.answered:
    st.session_state.answered = True

    if choice == quiz["a"]:
        st.success("正解！ +1pt")
        st.session_state.score += 1
        components.html(circle_effect, height=700, scrolling=False)
    else:
        st.error("不正解… -1pt")
        st.session_state.score -= 1
        components.html(cross_effect, height=700, scrolling=False)

#============================
#スコア環境
#===========================

if st.session_state.score < 0:
    st.session_state.score = 0

# ============================
# 次の問題へ（演出後も必ず表示）
# ============================

if st.session_state.answered:
    if st.button("次の問題へ"):
        st.session_state.current_quiz = pick_new_quiz()
        st.session_state.choices = None
        st.session_state.answered = False
        st.rerun()
