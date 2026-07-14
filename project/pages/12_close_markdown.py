import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Totem X Effect",
    page_icon="❌",
    layout="centered"
)

html = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>Totem X Effect</title>

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

    /* ✖ が奥に消えないようにする */
    perspective: 900px;
}

/* ===========================
   トーテム ✖（赤）
=========================== */

.totem{
    position:relative;
    width:160px;
    height:160px;

    /* ✖ を3Dのまま回転させるために必須 */
    transform-style: preserve-3d;

    animation:
        spinIn 3.2s ease-out,
        float 4s ease-in-out infinite 3.2s,
        vanish 1.6s ease-in-out 7.0s forwards;
}

/* 真ん中の✖（赤） */
.core{
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    width:100px;
    height:100px;

    display:flex;
    justify-content:center;
    align-items:center;

    font-size:90px;
    font-weight:900;
    color:#ff2b2b;
    text-shadow:
        0 0 20px #ff2b2b,
        0 0 40px #ff7b00,
        0 0 70px rgba(255,120,0,.9);

    animation:pulse 2.4s ease-in-out infinite;
}

/* ===========================
   粒子（オレンジ＋赤＋黄色）
=========================== */

.particle{
    position:absolute;
    width:14px;
    height:14px;
    border-radius:50%;

    animation:spread 2.2s ease-out infinite;
}

.orange{ background:#ff7b00; box-shadow:0 0 25px #ff7b00; }
.red{ background:#ff2b2b; box-shadow:0 0 25px #ff2b2b; }
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

/* Y軸でゆっくり回転して出てくる */
@keyframes spinIn{
    0%{
        transform:scale(0) rotateY(0deg);
        opacity:0;
    }
    40%{
        transform:scale(0.7) rotateY(180deg);
        opacity:1;
    }
    100%{
        transform:scale(1) rotateY(720deg);
        opacity:1;
    }
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

/* 粒子がずっと発散し続ける */
@keyframes spread{
    0%{
        transform:translate(-50%,-50%) scale(0.3);
        opacity:1;
    }
    100%{
        transform:translate(var(--x), var(--y)) scale(1.8);
        opacity:0;
    }
}

/* 後ろに下がって消える */
@keyframes vanish{
    0%{
        transform:scale(1) translateY(0);
        opacity:1;
        filter:blur(0px);
    }
    100%{
        transform:scale(0.2) translateY(160px);
        opacity:0;
        filter:blur(6px);
    }
}

</style>

<div class="scene">

    <div class="totem">

        <!-- 粒子 -->
        <div class="particle orange p1" style="--x:-200px; --y:-300px;"></div>
        <div class="particle red p2" style="--x:240px; --y:-320px;"></div>
        <div class="particle yellow p3" style="--x:-260px; --y:120px;"></div>
        <div class="particle orange p4" style="--x:280px; --y:140px;"></div>
        <div class="particle red p5" style="--x:-140px; --y:260px;"></div>
        <div class="particle yellow p6" style="--x:160px; --y:240px;"></div>

        <!-- ✖ 本体 -->
        <div class="core">✖</div>

    </div>

</div>

</html>
"""

components.html(html, height=700, scrolling=False)
