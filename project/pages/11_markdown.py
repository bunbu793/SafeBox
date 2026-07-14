import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="2D Trophy Totem",
    page_icon="🏆",
    layout="centered"
)

html = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>2D Trophy Totem</title>

<style>

/* 背景を白に */
body{
    margin:0;
    background:#ffffff;
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
   2Dトロフィー（↑の画像風）
=========================== */

.trophy{
    position:relative;
    width:180px;
    height:250px;
    animation:
        summon 1.6s cubic-bezier(.18,1.15,.3,1),
        float 3s ease-in-out infinite 1.6s,
        glow 2.5s ease-in-out infinite;
}

/* カップ（2Dイラスト風） */
.cup{
    position:relative;
    width:150px;
    height:110px;
    margin:auto;
    background:#FFD54A;
    border-radius:0 0 70px 70px;
    border-top:8px solid #FFE9A0;
}

/* 左右の取っ手（2D） */
.left, .right{
    position:absolute;
    top:18px;
    width:42px;
    height:42px;
    border-radius:50%;
    border:10px solid #FFD54A;
    background:none;
}

.left{ left:-30px; border-right:none; }
.right{ right:-30px; border-left:none; }

/* 星（2D） */
.star{
    position:absolute;
    left:50%;
    top:25%;
    transform:translate(-50%,-50%);
    font-size:52px;
    color:white;
    text-shadow:
        0 0 8px gold,
        0 0 18px orange;
    animation:
        starPulse 1.8s ease-in-out infinite,
        starFloat 2.8s ease-in-out infinite;
}

/* 柱（2D） */
.stem{
    width:34px;
    height:60px;
    margin:auto;
    background:#FFD54A;
}

/* 台座（2D） */
.base1{
    width:82px;
    height:24px;
    margin:auto;
    background:#8B5200;
    border-radius:6px 6px 0 0;
}

.base2{
    width:130px;
    height:18px;
    margin:auto;
    background:#5A3100;
    border-radius:0 0 8px 8px;
}

/* ===========================
   トーテム演出（そのまま）
=========================== */

/* 光のリング */
.ring{
    position:absolute;
    left:50%;
    top:42%;
    width:230px;
    height:230px;
    transform:translate(-50%,-50%);
    border-radius:50%;
    border:3px solid rgba(255,235,120,.7);
    box-shadow:0 0 25px gold, inset 0 0 18px white;
    animation:ring 2.2s infinite;
}

/* パーティクル */
.particle{
    position:absolute;
    width:8px;
    height:8px;
    border-radius:50%;
    background:white;
    box-shadow:0 0 12px gold, 0 0 25px orange;
}

.p1{left:20px;top:40px;animation:fly1 2.2s infinite;}
.p2{right:30px;top:60px;animation:fly2 2.5s infinite;}
.p3{left:55px;bottom:30px;animation:fly3 2.8s infinite;}
.p4{right:40px;bottom:20px;animation:fly4 2.3s infinite;}
.p5{left:50%;top:-10px;animation:fly5 2.6s infinite;}
.p6{left:50%;bottom:-5px;animation:fly6 2.1s infinite;}
.p7{left:-5px;top:120px;animation:fly7 2.4s infinite;}
.p8{right:-5px;top:120px;animation:fly8 2.7s infinite;}

/* 光のオーラ */
.trophy::before{
    content:"";
    position:absolute;
    left:50%;
    top:45%;
    transform:translate(-50%,-50%);
    width:240px;
    height:240px;
    border-radius:50%;
    background:radial-gradient(circle,
        rgba(255,240,160,.55),
        rgba(255,215,0,.15),
        transparent 72%);
    filter:blur(12px);
    animation:aura 2.2s ease-in-out infinite;
    z-index:-5;
}

/* 光の柱 */
.trophy::after{
    content:"";
    position:absolute;
    left:50%;
    top:-170px;
    transform:translateX(-50%);
    width:110px;
    height:520px;
    background:linear-gradient(
        transparent,
        rgba(255,255,255,.85),
        rgba(255,230,80,.9),
        rgba(255,255,255,.85),
        transparent
    );
    filter:blur(22px);
    animation:beam 2s ease-in-out infinite;
    z-index:-6;
}

/* ===========================
   アニメーション
=========================== */

@keyframes summon{
    0%{opacity:0;transform:translateY(180px) scale(.2) rotate(-80deg);filter:blur(10px);}
    40%{opacity:1;transform:translateY(-25px) scale(1.15) rotate(12deg);}
    70%{transform:translateY(8px) scale(.95) rotate(-4deg);}
    100%{opacity:1;transform:translateY(0) scale(1) rotate(0);filter:none;}
}

@keyframes float{
    0%{transform:translateY(0);}
    50%{transform:translateY(-10px);}
    100%{transform:translateY(0);}
}

@keyframes starPulse{
    0%{transform:translate(-50%,-50%) scale(1);}
    50%{transform:translate(-50%,-50%) scale(1.18);}
    100%{transform:translate(-50%,-50%) scale(1);}
}

@keyframes starFloat{
    0%{margin-top:0;}
    50%{margin-top:-6px;}
    100%{margin-top:0;}
}

@keyframes ring{
    0%{transform:translate(-50%,-50%) scale(.5);opacity:1;}
    100%{transform:translate(-50%,-50%) scale(1.7);opacity:0;}
}

@keyframes fly1{0%{transform:translate(0,0) scale(.4);}100%{transform:translate(-40px,-80px) scale(1.8);opacity:0;}}
@keyframes fly2{0%{transform:translate(0,0);}100%{transform:translate(45px,-90px);opacity:0;}}
@keyframes fly3{0%{transform:translate(0,0);}100%{transform:translate(-35px,70px);opacity:0;}}
@keyframes fly4{0%{transform:translate(0,0);}100%{transform:translate(40px,80px);opacity:0;}}
@keyframes fly5{0%{transform:translate(-50%,0);}100%{transform:translate(-50%,-120px);opacity:0;}}
@keyframes fly6{0%{transform:translate(-50%,0);}100%{transform:translate(-50%,100px);opacity:0;}}
@keyframes fly7{0%{transform:translate(0,0);}100%{transform:translate(-80px,-20px);opacity:0;}}
@keyframes fly8{0%{transform:translate(0,0);}100%{transform:translate(80px,-20px);opacity:0;}}

@keyframes aura{
    0%{transform:translate(-50%,-50%) scale(.8);opacity:.35;}
    50%{transform:translate(-50%,-50%) scale(1.05);opacity:.9;}
    100%{transform:translate(-50%,-50%) scale(.8);opacity:.35;}
}

@keyframes beam{
    0%{opacity:.25;transform:translateX(-50%) scaleY(.6);}
    50%{opacity:1;transform:translateX(-50%) scaleY(1.2);}
    100%{opacity:.25;transform:translateX(-50%) scaleY(.6);}
}

@keyframes glow{
    0%{filter:drop-shadow(0 0 8px rgba(255,215,0,.25));}
    50%{filter:drop-shadow(0 0 22px gold) drop-shadow(0 0 45px orange);}
    100%{filter:drop-shadow(0 0 8px rgba(255,215,0,.25));}
}

</style>
</head>

<body>

<div class="scene">

    <div class="trophy">

        <div class="ring"></div>

        <div class="particle p1"></div>
        <div class="particle p2"></div>
        <div class="particle p3"></div>
        <div class="particle p4"></div>
        <div class="particle p5"></div>
        <div class="particle p6"></div>
        <div class="particle p7"></div>
        <div class="particle p8"></div>

        <div class="cup">
            <div class="left"></div>
            <div class="right"></div>
            <div class="star">★</div>
        </div>

        <div class="stem"></div>
        <div class="base1"></div>
        <div class="base2"></div>

    </div>

</div>

</body>
</html>
"""

components.html(html, height=700, scrolling=False)
