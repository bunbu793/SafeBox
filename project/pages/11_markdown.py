import streamlit as st

st.set_page_config(
    page_title="Golden Trophy",
    page_icon="🏆",
    layout="centered"
)

st.markdown("""
<style>

body{
    overflow:hidden;
}

.trophy-area{
    display:flex;
    justify-content:center;
    align-items:center;
    height:650px;
}

/* トロフィー全体 */
.trophy{
    position:relative;
    width:260px;
    height:420px;
    animation:
        summon 1.8s ease-out,
        float 4s ease-in-out infinite 2s;
}

/* カップ */
.cup{
    position:relative;
    width:170px;
    height:145px;
    margin:auto;
    border-radius:0 0 90px 90px;
    overflow:hidden;
    background:
        linear-gradient(
            90deg,
            #8d6400 0%,
            #c99b25 12%,
            #f6d46b 28%,
            #fff6cb 48%,
            #f6d46b 68%,
            #c99b25 86%,
            #8d6400 100%
        );
    box-shadow:
        inset 0 10px 12px rgba(255,255,255,.45),
        inset -10px -14px 20px rgba(0,0,0,.18),
        0 15px 30px rgba(0,0,0,.28);
    border-top:8px solid #fff3c2;
}

/* カップ光沢 */
.cup::before{
    content:"";
    position:absolute;
    top:12px;
    left:18px;
    width:45px;
    height:90px;
    background:rgba(255,255,255,.35);
    border-radius:50%;
    filter:blur(8px);
}

/* 横に流れる反射 */
.cup::after{
    content:"";
    position:absolute;
    top:-30px;
    left:-120px;
    width:70px;
    height:240px;
    background:
        linear-gradient(
            rgba(255,255,255,0),
            rgba(255,255,255,.7),
            rgba(255,255,255,0)
        );
    transform:rotate(20deg);
    animation:shine 4s linear infinite;
}

/* 取っ手 */
.handle-left,
.handle-right{
    position:absolute;
    top:20px;
    width:60px;
    height:60px;
    border-radius:50%;
    border:12px solid #d7ab32;
    background:none;
    box-shadow:inset 0 4px 5px rgba(255,255,255,.4);
}

.handle-left{ left:-42px; border-right:none; }
.handle-right{ right:-42px; border-left:none; }

/* 星（文字★） */
.star{
    position:absolute;
    top:22%;
    left:50%;
    transform:translate(-50%,-50%);
    font-size:64px;
    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #fff6b0 20%,
            #ffe36b 45%,
            #ffc800 70%,
            #b67d00 100%
        );
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    filter:
        drop-shadow(0 0 8px rgba(255,255,255,.9))
        drop-shadow(0 0 18px gold)
        drop-shadow(0 0 35px orange);
    animation:
        pulseStar 2s ease-in-out infinite,
        starFloat 3s ease-in-out infinite;
}

/* 柱 */
.stem{
    width:42px;
    height:68px;
    margin:auto;
}

/* 台座 */
.base-top{
    width:90px;
    height:34px;
    margin:auto;
    border-radius:8px 8px 0 0;
    background:linear-gradient(180deg,#b06b00,#6d3600);
    box-shadow:
        inset 0 3px 4px rgba(255,255,255,.25),
        0 6px 12px rgba(0,0,0,.35);
}

.base-bottom{
    width:160px;
    height:24px;
    margin:auto;
    border-radius:0 0 8px 8px;
    background:linear-gradient(180deg,#7d4200,#432000);
    box-shadow:
        inset 0 3px 3px rgba(255,255,255,.2),
        0 8px 18px rgba(0,0,0,.45);
}

/* 光のリング */
.glow-ring{
    position:absolute;
    width:230px;
    height:230px;
    left:50%;
    top:45%;
    transform:translate(-50%,-50%);
    border-radius:50%;
    border:3px solid rgba(255,235,120,.6);
    box-shadow:0 0 20px gold, inset 0 0 20px white;
    animation:ringPulse 2s infinite;
}

/* パーティクル */
.spark{
    position:absolute;
    width:8px;
    height:8px;
    border-radius:50%;
    background:white;
    box-shadow:0 0 12px gold, 0 0 25px orange;
}

.spark1{ left:25px; top:20px; animation:particle1 2.4s infinite; }
.spark2{ right:18px; top:55px; animation:particle2 2.7s infinite; }
.spark3{ left:60px; bottom:8px; animation:particle3 2.5s infinite; }
.spark4{ right:55px; bottom:25px; animation:particle4 2.2s infinite; }
.spark5{ left:50%; top:-10px; animation:particle5 2.8s infinite; }
.spark6{ left:48%; bottom:-8px; animation:particle6 2.3s infinite; }

/* トーテム召喚 */
@keyframes summon{
    0%{opacity:0;transform:translateY(180px) scale(.2) rotate(-80deg);filter:blur(12px);}
    35%{opacity:1;transform:translateY(-25px) scale(1.15) rotate(12deg);}
    65%{transform:translateY(8px) scale(.95) rotate(-5deg);}
    100%{opacity:1;transform:translateY(0) scale(1) rotate(0);filter:blur(0);}
}

/* 浮遊 */
@keyframes float{
    0%{transform:translateY(0);}
    50%{transform:translateY(-14px);}
    100%{transform:translateY(0);}
}

/* 星の脈動 */
@keyframes pulseStar{
    0%{transform:translate(-50%,-50%) scale(1);}
    50%{transform:translate(-50%,-50%) scale(1.18);}
    100%{transform:translate(-50%,-50%) scale(1);}
}

/* 星の浮遊 */
@keyframes starFloat{
    0%{margin-top:0;}
    50%{margin-top:-6px;}
    100%{margin-top:0;}
}

/* 光の輪 */
@keyframes ringPulse{
    0%{transform:translate(-50%,-50%) scale(.7);opacity:1;}
    100%{transform:translate(-50%,-50%) scale(1.4);opacity:0;}
}

/* 背景演出 */
.trophy-area{
    background:radial-gradient(circle, rgba(255,245,180,.18), transparent 70%);
}

</style>

<div class="trophy-area">
<div class="trophy">

<div class="cup">

<div class="glow-ring"></div>

<div class="spark spark1"></div>
<div class="spark spark2"></div>
<div class="spark spark3"></div>
<div class="spark spark4"></div>
<div class="spark spark5"></div>
<div class="spark spark6"></div>

<div class="handle-left"></div>
<div class="handle-right"></div>

<div class="star">★</div>

</div>

<div class="stem"></div>
<div class="base-top"></div>
<div class="base-bottom"></div>

</div>
</div>

""", unsafe_allow_html=True)
