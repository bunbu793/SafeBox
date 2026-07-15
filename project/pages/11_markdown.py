import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="防災クイズ", page_icon="⛑️", layout="centered")

#============================
# ラジオボタン横並び
#============================
st.markdown("""
<style>
div.stRadio > div {
    display: flex;
    flex-direction: row;
    gap: 20px;
}
</style>
""", unsafe_allow_html=True)

# ============================
# 初期化
# ============================

if "score" not in st.session_state:
    st.session_state.score = 0

if "combo" not in st.session_state:
    st.session_state.combo = 0   # 連続正解数

if "used" not in st.session_state:
    st.session_state.used = []

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

if "choices" not in st.session_state:
    st.session_state.choices = None

if "answered" not in st.session_state:
    st.session_state.answered = False

# ============================
# 防災クイズ（問題増やせる）
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
     "a": "受付で登録する"},
]

# ============================
# ランク判定
# ============================

def get_rank(score):
    if score >= 25: return "S"
    if score >= 20: return "A"
    if score >= 15: return "B"
    if score >= 10: return "C"
    if score >= 5:  return "D"
    return "E"

# ============================
# 全国順位（疑似）
# ============================

def get_national_rank(score):
    avg = 12
    if score >= avg + 10: return "全国トップ10%"
    if score >= avg + 5:  return "全国トップ25%"
    if score >= avg:      return "全国トップ50%"
    return "全国平均以下"

# ============================
# スコア表示
# ============================

rank = get_rank(st.session_state.score)
national = get_national_rank(st.session_state.score)

st.markdown(
    f"""
    <div style='position:absolute; top:10px; right:20px; font-size:20px;'>
        スコア：{st.session_state.score} pt<br>
        連続正解：{st.session_state.combo} 回<br>
        ランク：{rank}<br>
        全国順位：{national}
    </div>
    """,
    unsafe_allow_html=True
)

st.title("防災クイズ")

# ============================
# 新しい問題を選ぶ
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
# トーテム演出（◯）
# ============================

circle_effect = """<!DOCTYPE html><html><head><style>
body{margin:0;background:white;overflow:hidden;}
.scene{
    position:absolute;
    top:120px;
    left:75%;
    transform:translateX(-50%);
}
.totem{
    position:relative;width:160px;height:160px;
    transform-style:preserve-3d;
    animation:spinIn 3.2s ease-out,float 4s ease-in-out infinite 3.2s;
}
.core{
    position:absolute;left:50%;top:50%;
    transform:translate(-50%,-50%);
    width:100px;height:100px;border-radius:50%;
    border:12px solid #00ff88;
    box-shadow:0 0 25px #00ff88,0 0 55px #ffee55;
}
</style>
<div class="scene"><div class="totem"><div class="core"></div></div></div>
</html>
"""

# ============================
# トーテム演出（✖）
# ============================

cross_effect = """<!DOCTYPE html><html><head><style>
body{margin:0;background:white;overflow:hidden;}
.scene{
    position:absolute;
    top:120px;
    left:75%;
    transform:translateX(-50%);
}
.totem{
    position:relative;width:160px;height:160px;
    transform-style:preserve-3d;
    animation:spinIn 3.2s ease-out,float 4s ease-in-out infinite 3.2s;
}
.core{
    position:absolute;left:50%;top:50%;
    transform:translate(-50%,-50%);
    width:170px;height:170px;
}
.core::before,.core::after{
    content:"";position:absolute;left:50%;top:50%;
    width:170px;height:28px;background:#ff2b2b;
    transform-origin:center;
}
.core::before{transform:translate(-50%,-50%) rotate(45deg);}
.core::after{transform:translate(-50%,-50%) rotate(-45deg);}
</style>
<div class="scene"><div class="totem"><div class="core"></div></div></div>
</html>
"""

# ============================
# 判定ボタン
# ============================

if not st.session_state.answered:
    send = st.button("送信")

    if send:
        st.session_state.answered = True

        if choice == quiz["a"]:
            st.success("正解！ +1pt")
            st.session_state.score += 1

            # 連続正解ボーナス
            st.session_state.combo += 1
            if st.session_state.combo >= 5:
                st.session_state.score += 5
                st.info("🔥 5連続正解ボーナス +5pt！")
            elif st.session_state.combo >= 3:
                st.session_state.score += 2
                st.info("✨ 3連続正解ボーナス +2pt！")
            elif st.session_state.combo >= 2:
                st.session_state.score += 1
                st.info("⭐ 2連続正解ボーナス +1pt！")

            components.html(circle_effect, height=300, scrolling=False)

        else:
            st.error("不正解… -1pt")
            st.session_state.score -= 1
            st.session_state.combo = 0
            components.html(cross_effect, height=300, scrolling=False)

else:
    st.write("")

# ============================
# スコアがマイナスにならないように
# ============================

if st.session_state.score < 0:
    st.session_state.score = 0

# ============================
# 次の問題へ
# ============================

if st.session_state.answered:
    if st.button("次の問題へ"):
        st.session_state.current_quiz = pick_new_quiz()
        st.session_state.choices = None
        st.session_state.answered = False
        st.rerun()
