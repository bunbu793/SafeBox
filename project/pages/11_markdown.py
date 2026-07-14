import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Totem Effect",
    page_icon="✨",
    layout="centered"
)

html = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>Totem Effect</title>

<style>

/* 背景は白 */
body{
    margin:0;
    background:white;
    overflow:hidden;
}

.scene{
    width:100vw;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}

/* ===========================
   トーテム ○
=========================== */

.totem{
    position:relative;
    width:140px;
    height:140px;
    animation:
        spinIn 0.9s cubic-bezier(.18,1.15,.3,1),
        float 3s ease-in-out infinite 1s,
        vanish 1.2s ease-in-out 3.2s forwards;
}

/* 中央の丸 */
.core{
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    width:80px;
    height:80px;
    background:white;
    border-radius:50%;

    box-shadow:
        0 0 20px #00ff88,
        0 0 40px #ffee55,
        0 0 70px rgba(255,255,120,.9);

    animation:
        pulse 1.8s ease-in-out infinite;
}

/* ===========================
   粒子（緑・黄色）
=========================== */

.particle{
    position:absolute;
    width:10px;
    height:10px;
    border-radius:50%;
    animation:explode 1.2s ease-out forwards;
}

.green{ background:#00ff88; box-shadow:0 0 20px #00ff88; }
.yellow{ background:#ffee55; box-shadow:0 0 20px #ffee55; }

/* 粒子の初期位置 */
.p1{ left:50%; top:50%; }
.p2{ left:50%; top:50%; }
.p3{ left:50%; top:50%; }
.p4{ left:50%; top:50%; }
.p5{ left:50%; top:50%; }
.p6{ left:50%; top:50%; }

/* ===========================
   アニメーション
=========================== */

/* くるくる召喚 */
@keyframes spinIn{
    0%{transform:scale(0) rotate(0deg); opacity:0;}
    60%{transform:scale(1.3) rotate(720deg); opacity:1;}
    100%{transform:scale(1) rotate(1080deg); opacity:1;}
}

/* 浮遊 */
@keyframes float{
    0%{transform:translateY(0);}
    50%{transform:translateY(-12px);}
    100%{transform:translateY(0);}
}

/* ○の脈動 */
@keyframes pulse{
    0%{transform:translate(-50%,-50%) scale(1);}
    50%{transform:translate(-50%,-50%) scale(1.25);}
    100%{transform:translate(-50%,-50%) scale(1);}
}

/* 粒子爆発 */
@keyframes explode{
    0%{transform:translate(-50%,-50%) scale(0); opacity:1;}
    100%{transform:translate(var(--x), var(--y)) scale(1.4); opacity:0;}
}

/* 後ろに下がって消える */
@keyframes vanish{
    0%{transform:scale(1) translateY(0); opacity:1;}
    100%{transform:scale(0.2) translateY(120px); opacity:0;}
}

</style>

<div class="scene">

    <div class="totem">

        <!-- 粒子（方向をCSS変数で指定） -->
        <div class="particle green p1" style="--x:-80px; --y:-120px;"></div>
        <div class="particle yellow p2" style="--x:90px; --y:-140px;"></div>
        <div class="particle green p3" style="--x:-120px; --y:40px;"></div>
        <div class="particle yellow p4" style="--x:130px; --y:60px;"></div>
        <div class="particle green p5" style="--x:-40px; --y:140px;"></div>
        <div class="particle yellow p6" style="--x:60px; --y:130px;"></div>

        <!-- 中央の○ -->
        <div class="core"></div>

    </div>

</div>

</html>
"""

components.html(html, height=700, scrolling=False)
