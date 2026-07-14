import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="Trophy", layout="centered")

with open("trophy.png", "rb") as f:
    img = base64.b64encode(f.read()).decode()

html = f"""
<!DOCTYPE html>
<html>
<head>

<style>

html,body{{
margin:0;
background:white;
overflow:hidden;
}}

.scene{{
height:100vh;
display:flex;
justify-content:center;
align-items:center;
}}

.trophy{{
width:260px;

animation:
summon 1.2s ease-out,
float 2.8s ease-in-out infinite 1.2s,
glow 2s ease-in-out infinite;
}

.trophy img{{
width:100%;
display:block;
}}

@keyframes summon{{

0%{{
opacity:0;
transform:
translateY(180px)
scale(.2)
rotate(-40deg);
}}

60%{{
opacity:1;
transform:
translateY(-20px)
scale(1.15)
rotate(8deg);
}}

100%{{
transform:
translateY(0)
scale(1)
rotate(0deg);
}}

}}

@keyframes float{{

0%{{transform:translateY(0);}}

50%{{transform:translateY(-12px);}}

100%{{transform:translateY(0);}}

}}

@keyframes glow{{

0%{{
filter:
drop-shadow(0 0 10px gold);
}}

50%{{
filter:
drop-shadow(0 0 35px gold)
drop-shadow(0 0 70px orange);
}}

100%{{
filter:
drop-shadow(0 0 10px gold);
}}

}}

</style>

</head>

<body>

<div class="scene">

<div class="trophy">

<img src="data:image/png;base64,{img}">

</div>

</div>

</body>

</html>
"""

components.html(html, height=600)