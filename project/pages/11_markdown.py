import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Golden Trophy",
    page_icon="🏆",
    layout="centered"
)

html = """
<!DOCTYPE html>
<html>
<head>

<style>

body{

    margin:0;
    background:#111;
    overflow:hidden;

}

.scene{

    width:100vw;
    height:100vh;

    display:flex;
    justify-content:center;
    align-items:center;

}

/* ===== トロフィー ===== */
/* ===========================
   ゴールドカラー
=========================== */

.cup{

    background:
        linear-gradient(
            90deg,
            #8a6500 0%,
            #c99716 18%,
            #ffe07a 45%,
            #fff6cf 50%,
            #ffd55a 60%,
            #c18a0d 82%,
            #7f5a00 100%
        );

    box-shadow:
        inset 0 6px 8px rgba(255,255,255,.45),
        inset -8px -10px 18px rgba(0,0,0,.25),
        0 12px 22px rgba(0,0,0,.35);

    overflow:hidden;

}

/* 光沢 */

.cup::before{

    content:"";

    position:absolute;

    left:18px;

    top:12px;

    width:34px;

    height:80px;

    border-radius:50%;

    background:
        rgba(255,255,255,.35);

    filter:blur(8px);

}

/* 流れる反射 */

.cup::after{

    content:"";

    position:absolute;

    top:-30px;

    left:-80px;

    width:35px;

    height:180px;

    background:
        linear-gradient(
            transparent,
            rgba(255,255,255,.8),
            transparent
        );

    transform:rotate(18deg);

    animation:shine 3.5s linear infinite;

}

/* ===========================
   取っ手
=========================== */

.left,
.right{

    border:10px solid #d6a521;

    box-shadow:
        inset 0 2px 4px rgba(255,255,255,.35);

}

.left{

    border-right:none;

}

.right{

    border-left:none;

}

/* ===========================
   星
=========================== */

.star{

    color:#fff7bc;

    text-shadow:

        0 0 8px white,

        0 0 18px gold,

        0 0 35px orange;

}

/* ===========================
   柱
=========================== */

.stem{

    background:

        linear-gradient(
            90deg,
            #936400,
            #ffd86b,
            #8b5b00
        );

}

/* ===========================
   台座
=========================== */

.base1{

    background:

        linear-gradient(
            #8b5200,
            #5b3100
        );

    border-radius:6px 6px 0 0;

}

.base2{

    background:

        linear-gradient(
            #5a3100,
            #311700
        );

    border-radius:0 0 8px 8px;

}

/* ===========================
   アニメーション
=========================== */

@keyframes shine{

    from{

        left:-90px;

    }

    to{

        left:220px;

    }

}

.trophy{

    position:relative;

    width:180px;
    height:250px;

}

/* カップ */

.cup{

    position:relative;

    width:150px;
    height:110px;

    margin:auto;

    border-radius:0 0 70px 70px;

}

/* 左右の取っ手 */

.left,
.right{

    position:absolute;

    top:18px;

    width:42px;
    height:42px;

    border-radius:50%;

}

.left{

    left:-30px;

}

.right{

    right:-30px;

}

/* 星 */

.star{

    position:absolute;

    left:50%;
    top:25%;

    transform:translate(-50%,-50%);

    font-size:52px;

}

/* 柱 */

.stem{

    width:34px;
    height:60px;

    margin:auto;

}

/* 土台 */

.base1{

    width:82px;
    height:24px;

    margin:auto;

}

.base2{

    width:130px;
    height:18px;

    margin:auto;

}

/*=====================================
    トロフィー出現
=====================================*/

.trophy{

    animation:
        summon 1.6s cubic-bezier(.18,1.15,.3,1),
        float 3s ease-in-out infinite 1.6s;

}


/*=====================================
    星
=====================================*/

.star{

    animation:
        starPulse 1.8s ease-in-out infinite,
        starFloat 2.8s ease-in-out infinite;

}


/*=====================================
    光のオーラ
=====================================*/

.trophy::before{

    content:"";

    position:absolute;

    left:50%;
    top:45%;

    transform:translate(-50%,-50%);

    width:240px;
    height:240px;

    border-radius:50%;

    background:
        radial-gradient(circle,
        rgba(255,240,160,.55),
        rgba(255,215,0,.15),
        transparent 72%);

    filter:blur(12px);

    animation:
        aura 2.2s ease-in-out infinite;

    z-index:-5;

}


/*=====================================
    光の柱
=====================================*/

.trophy::after{

    content:"";

    position:absolute;

    left:50%;
    top:-170px;

    transform:translateX(-50%);

    width:110px;
    height:520px;

    background:
        linear-gradient(
            transparent,
            rgba(255,255,255,.85),
            rgba(255,230,80,.9),
            rgba(255,255,255,.85),
            transparent
        );

    filter:blur(22px);

    animation:
        beam 2s ease-in-out infinite;

    z-index:-6;

}


/*=====================================
    出現
=====================================*/

@keyframes summon{

0%{

opacity:0;

transform:
translateY(180px)
scale(.2)
rotate(-80deg);

filter:blur(10px);

}

40%{

opacity:1;

transform:
translateY(-25px)
scale(1.15)
rotate(12deg);

}

70%{

transform:
translateY(8px)
scale(.95)
rotate(-4deg);

}

100%{

opacity:1;

transform:
translateY(0)
scale(1)
rotate(0);

filter:none;

}

}


/*=====================================
    浮遊
=====================================*/

@keyframes float{

0%{

transform:translateY(0);

}

50%{

transform:translateY(-10px);

}

100%{

transform:translateY(0);

}

}


/*=====================================
    星
=====================================*/

@keyframes starPulse{

0%{

transform:
translate(-50%,-50%)
scale(1);

}

50%{

transform:
translate(-50%,-50%)
scale(1.18);

}

100%{

transform:
translate(-50%,-50%)
scale(1);

}

}

@keyframes starFloat{

0%{

margin-top:0;

}

50%{

margin-top:-6px;

}

100%{

margin-top:0;

}

}


/*=====================================
    オーラ
=====================================*/

@keyframes aura{

0%{

transform:
translate(-50%,-50%)
scale(.8);

opacity:.35;

}

50%{

transform:
translate(-50%,-50%)
scale(1.05);

opacity:.9;

}

100%{

transform:
translate(-50%,-50%)
scale(.8);

opacity:.35;

}

}


/*=====================================
    光の柱
=====================================*/

@keyframes beam{

0%{

opacity:.25;

transform:
translateX(-50%)
scaleY(.6);

}

50%{

opacity:1;

transform:
translateX(-50%)
scaleY(1.2);

}

100%{

opacity:.25;

transform:
translateX(-50%)
scaleY(.6);

}

}
/*=============================
    光のリング
=============================*/

.ring{

    position:absolute;

    left:50%;
    top:42%;

    width:230px;
    height:230px;

    transform:translate(-50%,-50%);

    border-radius:50%;

    border:3px solid rgba(255,235,120,.7);

    box-shadow:

        0 0 25px gold,

        inset 0 0 18px white;

    animation:ring 2.2s infinite;

}


/*=============================
    キラキラ
=============================*/

.particle{

    position:absolute;

    width:8px;
    height:8px;

    border-radius:50%;

    background:white;

    box-shadow:

        0 0 12px gold,

        0 0 25px orange;

}

.p1{left:20px;top:40px;animation:fly1 2.2s infinite;}
.p2{right:30px;top:60px;animation:fly2 2.5s infinite;}
.p3{left:55px;bottom:30px;animation:fly3 2.8s infinite;}
.p4{right:40px;bottom:20px;animation:fly4 2.3s infinite;}
.p5{left:50%;top:-10px;animation:fly5 2.6s infinite;}
.p6{left:50%;bottom:-5px;animation:fly6 2.1s infinite;}
.p7{left:-5px;top:120px;animation:fly7 2.4s infinite;}
.p8{right:-5px;top:120px;animation:fly8 2.7s infinite;}


/*=============================
    光の輪
=============================*/

@keyframes ring{

0%{

transform:
translate(-50%,-50%)
scale(.5);

opacity:1;

}

100%{

transform:
translate(-50%,-50%)
scale(1.7);

opacity:0;

}

}


/*=============================
    パーティクル
=============================*/

@keyframes fly1{
0%{transform:translate(0,0) scale(.4);}
100%{transform:translate(-40px,-80px) scale(1.8);opacity:0;}
}

@keyframes fly2{
0%{transform:translate(0,0);}
100%{transform:translate(45px,-90px);opacity:0;}
}

@keyframes fly3{
0%{transform:translate(0,0);}
100%{transform:translate(-35px,70px);opacity:0;}
}

@keyframes fly4{
0%{transform:translate(0,0);}
100%{transform:translate(40px,80px);opacity:0;}
}

@keyframes fly5{
0%{transform:translate(-50%,0);}
100%{transform:translate(-50%,-120px);opacity:0;}
}

@keyframes fly6{
0%{transform:translate(-50%,0);}
100%{transform:translate(-50%,100px);opacity:0;}
}

@keyframes fly7{
0%{transform:translate(0,0);}
100%{transform:translate(-80px,-20px);opacity:0;}
}

@keyframes fly8{
0%{transform:translate(0,0);}
100%{transform:translate(80px,-20px);opacity:0;}
}
/*==================================
  最終仕上げ
==================================*/

/* トロフィーにマウスを乗せると発光 */
.trophy:hover{

    transform:
        scale(1.08);

    transition:.35s;

    filter:
        drop-shadow(0 0 18px gold)
        drop-shadow(0 0 40px orange)
        drop-shadow(0 0 90px gold);

}

/* 星 */

.star{

    transform-origin:center;

}

.trophy:hover .star{

    animation:
        starSpin .9s linear infinite,
        starPulse 1.2s ease-in-out infinite;

}

/* カップに流れる光 */

.cup{

    position:relative;

    overflow:hidden;

}

.cup::after{

    animation:
        shine 2.8s linear infinite;

}


/* フラッシュ */

.scene::before{

    content:"";

    position:absolute;

    inset:0;

    pointer-events:none;

    background:

        radial-gradient(
            circle,
            rgba(255,255,255,.7),
            transparent 60%
        );

    opacity:0;

    animation:
        flash 4s infinite;

}


/* 背景 */

.scene{

    background:

        radial-gradient(
            circle at center,
            #2a2100 0%,
            #181818 45%,
            #090909 100%
        );

}


/* 少し回転 */

@keyframes starSpin{

    from{

        transform:
            translate(-50%,-50%)
            rotate(0deg);

    }

    to{

        transform:
            translate(-50%,-50%)
            rotate(360deg);

    }

}


/* フラッシュ */

@keyframes flash{

    0%,80%,100%{

        opacity:0;

    }

    82%{

        opacity:.9;

    }

    85%{

        opacity:0;

    }

}


/* トロフィー全体のゆらぎ */

.trophy{

    animation:

        summon 1.6s cubic-bezier(.2,1.1,.3,1),

        float 3s ease-in-out infinite 1.6s,

        glow 2.5s ease-in-out infinite;

}


@keyframes glow{

    0%{

        filter:

            drop-shadow(0 0 8px rgba(255,215,0,.25));

    }

    50%{

        filter:

            drop-shadow(0 0 22px gold)
            drop-shadow(0 0 45px orange);

    }

    100%{

        filter:

            drop-shadow(0 0 8px rgba(255,215,0,.25));

    }

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

components.html(
    html,
    height=650,
    scrolling=False
)