import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="防災クイズ", page_icon="⛑️", layout="centered")

st.title("防災クイズ：正解すると◯、間違えると✖が出るよ")

# 防災クイズ（例）
question = "地震が起きたとき、まず最初にするべき行動は？"
answer = "身を守る"

user_answer = st.text_input("答えを入力してね")

# ============================
# ◯ 演出（侃の緑の輪っか）
# ============================

circle_effect = """
<!DOCTYPE html>
<html>
<head>
<style>
body{margin:0;background:white;overflow:hidden;}
.scene{
    width:100vw;height:100vh;
    display:flex;justify-content:center;align-items:center;
    perspective:900px;
    transform:translateY(-140px);
}
.totem{
    position:relative;width:160px;height:160px;
    transform-style:preserve-3d;
    animation:spinIn 3.2s ease-out,float 4s ease-in-out infinite 3.2s,vanish 1.6s ease-in-out 7.0s forwards;
}
.core{
    position:absolute;left:50%;top:50%;
    transform:translate(-50%,-50%);
    width:100px;height:100px;border-radius:50%;
    border:12px solid #00ff88;background:transparent;
    box-shadow:0 0 25px #00ff88,0 0 55px #ffee55,0 0 90px rgba(255,255,120,.9);
    animation:pulse 2.4s ease-in-out infinite;
}
.particle{
    position:absolute;width:14px;height:14px;border-radius:50%;
    animation:spread 2.2s ease-out infinite;
}
.green{background:#00ff88;box-shadow:0 0 25px #00ff88;}
.yellow{background:#ffee55;box-shadow:0 0 25px #ffee55;}
.p1,.p2,.p3,.p4,.p5,.p6{left:50%;top:50%;}
@keyframes spinIn{
    0%{transform:scale(0) rotateY(0deg);opacity:0;}
    40%{transform:scale(0.7) rotateY(180deg);opacity:1;}
    100%{transform:scale(1) rotateY(720deg);opacity:1;}
}
@keyframes float{
    0%{transform:translateY(0);}
    50%{transform:translateY(-16px);}
    100%{transform:translateY(0);}
}
@keyframes pulse{
    0%{transform:translate(-50%,-50%) scale(1);}
    50%{transform:translate(-50%,-50%) scale(1.35);}
    100%{transform:translate(-50%,-50%) scale(1);}
}
@keyframes spread{
    0%{transform:translate(-50%,-50%) scale(0.3);opacity:1;}
    100%{transform:translate(var(--x), var(--y)) scale(1.8);opacity:0;}
}
@keyframes vanish{
    0%{transform:scale(1) translateY(0);opacity:1;filter:blur(0px);}
    100%{transform:scale(0.2) translateY(160px);opacity:0;filter:blur(6px);}
}
</style>

<div class="scene">
<div class="totem">

<div class="particle green p1" style="--x:-200px; --y:-300px;"></div>
<div class="particle yellow p2" style="--x:240px; --y:-320px;"></div>
<div class="particle green p3" style="--x:-260px; --y:120px;"></div>
<div class="particle yellow p4" style="--x:280px; --y:140px;"></div>
<div class="particle green p5" style="--x:-140px; --y:260px;"></div>
<div class="particle yellow p6" style="--x:160px; --y:240px;"></div>

<div class="core"></div>

</div>
</div>
</html>
"""

# ============================
# ✖ 演出（侃の170px巨大バツ）
# ============================

cross_effect = """
<!DOCTYPE html>
<html>
<head>
<style>
body{margin:0;background:white;overflow:hidden;}
.scene{
    width:100vw;height:100vh;
    display:flex;justify-content:center;align-items:center;
    perspective:900px;
    transform:translateY(-140px);
}
.totem{
    position:relative;width:160px;height:160px;
    transform-style:preserve-3d;
    animation:spinIn 3.2s ease-out,float 4s ease-in-out infinite 3.2s,vanish 1.6s ease-in-out 7.0s forwards;
}

/* ✖ 本体（170px） */
.core{
    position:absolute;left:50%;top:50%;
    transform:translate(-50%,-50%);
    width:170px;height:170px;
}

/* ✖ の線（太く・長く） */
.core::before,
.core::after{
    content:"";
    position:absolute;left:50%;top:50%;
    width:170px;     /* ← 長さ */
    height:28px;     /* ← 太さ */
    background:#ff2b2b;
    box-shadow:
        0 0 25px #ff2b2b,
        0 0 45px #ff7b00,
        0 0 75px rgba(255,120,0,.9);
    transform-origin:center;
}

.core::before{transform:translate(-50%,-50%) rotate(45deg);}
.core::after{transform:translate(-50%,-50%) rotate(-45deg);}

/* 粒子 */
.particle{
    position:absolute;width:14px;height:14px;border-radius:50%;
    animation:spread 2.2s ease-out infinite;
}
.orange{background:#ff7b00;box-shadow:0 0 25px #ff7b00;}
.red{background:#ff2b2b;box-shadow:0 0 25px #ff2b2b;}
.yellow{background:#ffee55;box-shadow:0 0 25px #ffee55;}
.p1,.p2,.p3,.p4,.p5,.p6{left:50%;top:50%;}

@keyframes spinIn{
    0%{transform:scale(0) rotateY(0deg);opacity:0;}
    40%{transform:scale(0.7) rotateY(180deg);opacity:1;}
    100%{transform:scale(1) rotateY(720deg);opacity:1;}
}
@keyframes float{
    0%{transform:translateY(0);}
    50%{transform:translateY(-16px);}
    100%{transform:translateY(0);}
}
@keyframes spread{
    0%{transform:translate(-50%,-50%) scale(0.3);opacity:1;}
    100%{transform:translate(var(--x), var(--y)) scale(1.8);opacity:0;}
}
@keyframes vanish{
    0%{transform:scale(1) translateY(0);opacity:1;filter:blur(0px);}
    100%{transform:scale(0.2) translateY(160px);opacity:0;filter:blur(6px);}
}
</style>

<div class="scene">
<div class="totem">

<div class="particle orange p1" style="--x:-200px; --y:-300px;"></div>
<div class="particle red p2" style="--x:240px; --y:-320px;"></div>
<div class="particle yellow p3" style="--x:-260px; --y:120px;"></div>
<div class="particle orange p4" style="--x:280px; --y:140px;"></div>
<div class="particle red p5" style="--x:-140px; --y:260px;"></div>
<div class="particle yellow p6" style="--x:160px; --y:240px;"></div>

<div class="core"></div>

</div>
</div>
</html>
"""

# ============================
# 判定
# ============================

if st.button("判定"):
    if user_answer == answer:
        st.success("正解！")
        components.html(circle_effect, height=700, scrolling=False)
    else:
        st.error("不正解…")
        components.html(cross_effect, height=700, scrolling=False)
