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
   トーテム ○（輪っか）
=========================== */

.totem{
    position:relative;
    width:160px;
    height:160px;
    animation:
        spinIn 2.2s cubic-bezier(.18,1.15,.3,1),
        float 4s ease-in-out infinite 2.2s,
        vanish 2.4s ease-in-out 6.4s forwards;
}

/* 真ん中の◯（穴あき輪っか） */
.core{
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    width:100px;
    height:100px;
    border-radius:50%;
    border:12px solid #00ff88;   /* 線は濃いまま */
    background:transparent;

    box-shadow:
        0 0 25px #00ff88,
        0 0 55px #ffee55,
        0 0 90px rgba(255,255,120,.9);

    animation:
        pulse 2.4s ease-in-out infinite;
}

/* ===========================
   粒子（緑・黄色）
=========================== */

.particle{
    position:absolute;
    width:14px;
    height:14px;
    border-radius:50%;
    animation:explode 1.8s ease-out forwards;
}

.green{ background:#00ff88; box-shadow:0 0 25px #00ff88; }
.yellow{ background:#ffee55; box-shadow:0 0 25px #ffee55; }

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

/* ゆっくり回転して出てくる */
@keyframes spinIn{
    0%{transform:scale(0) rotate(0deg); opacity:0;}
    40%{transform:scale(0.8) rotate(360deg); opacity:1;}
    100%{transform:scale(1) rotate(720deg); opacity:1;}
}

/* 浮遊 */
@keyframes float{
    0%{transform:translateY(0);}
    50%{transform:translateY(-16px);}
    100%{transform:translateY(0);}
}

/* 脈動 */
@keyframes pulse{
    0%{transform:translate(-50%,-50%) scale(1);}
    50%{transform:translate(-50%,-50%) scale(1.35);}
    100%{transform:translate(-50%,-50%) scale(1);}
}

/* 粒子爆発（飛距離を大幅アップ） */
@keyframes explode{
    0%{transform:translate(-50%,-50%) scale(0); opacity:1;}
    100%{transform:translate(var(--x), var(--y)) scale(1.8); opacity:0;}
}

/* 後ろに下がって消える（演出長め） */
@keyframes vanish{
    0%{
        transform:scale(1) translateY(0) translateZ(0);
        opacity:1;
        filter:blur(0px);
    }
    50%{
        transform:scale(0.6) translateY(60px) translateZ(-120px);
        opacity:.6;
        filter:blur(4px);
    }
    100%{
        transform:scale(0.2) translateY(180px) translateZ(-260px);
        opacity:0;
        filter:blur(8px);
    }
}

</style>

<div class="scene">

    <div class="totem">

        <!-- 粒子（飛距離を大幅に伸ばした） -->
        <div class="particle green p1" style="--x:-160px; --y:-240px;"></div>
        <div class="particle yellow p2" style="--x:180px; --y:-260px;"></div>
        <div class="particle green p3" style="--x:-220px; --y:80px;"></div>
        <div class="particle yellow p4" style="--x:240px; --y:100px;"></div>
        <div class="particle green p5" style="--x:-100px; --y:220px;"></div>
        <div class="particle yellow p6" style="--x:120px; --y:210px;"></div>

        <!-- 真ん中の◯（穴あき輪っか） -->
        <div class="core"></div>

    </div>

</div>

</html>
"""

components.html(html, height=700, scrolling=False)
