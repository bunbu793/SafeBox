import streamlit as st

# トロフィーCSS
st.markdown("""
<style>
.trophy {
    width: 120px;
    height: 160px;
    margin: auto;
    position: relative;

    animation: zoomIn 0.8s ease-out forwards,
               explode 0.8s ease-out 0.8s forwards,
               rise 1.2s ease-out 1.6s forwards,
               shine 2s ease-in-out infinite 2.8s;
}

.trophy .cup {
    width: 100px;
    height: 70px;
    background: gold;
    border-radius: 50px 50px 20px 20px;
    margin: auto;
    position: relative;
    box-shadow: 0 0 20px rgba(255,215,0,0.7);
}

.trophy .handle-left,
.trophy .handle-right {
    width: 30px;
    height: 50px;
    border: 8px solid gold;
    border-radius: 50%;
    position: absolute;
    top: 10px;
}

.trophy .handle-left { left: -25px; }
.trophy .handle-right { right: -25px; }

.trophy .base {
    width: 80px;
    height: 40px;
    background: #8b5a2b;
    margin: auto;
    border-radius: 5px;
    margin-top: 10px;
}

@keyframes zoomIn {
    0% { transform: scale(0.1) translateY(-200px); opacity: 0; }
    60% { transform: scale(1.3) translateY(20px); opacity: 1; }
    100% { transform: scale(1) translateY(0px); opacity: 1; }
}

@keyframes explode {
    0% { filter: drop-shadow(0px 0px 0px gold); }
    50% { filter: drop-shadow(0px 0px 40px gold); }
    100% { filter: drop-shadow(0px 0px 10px gold); }
}

@keyframes rise {
    0% { transform: translateY(0px); }
    100% { transform: translateY(-20px); }
}

@keyframes shine {
    0% { filter: drop-shadow(0px 0px 5px gold); }
    50% { filter: drop-shadow(0px 0px 25px gold); }
    100% { filter: drop-shadow(0px 0px 5px gold); }
}
</style>
""", unsafe_allow_html=True)

# レイアウト（左：問題、右：トロフィー）
left, right = st.columns([2, 1])

with left:
    st.write("### 非常食として正しいものは？")
    answer = st.radio("選んでください", ["缶詰", "生肉", "アイスクリーム", "ケーキ"])
    st.button("回答する")

with right:
    st.markdown("""
    <div class="trophy">
        <div class="cup"></div>
        <div class="handle-left"></div>
        <div class="handle-right"></div>
        <div class="base"></div>
    </div>
    """, unsafe_allow_html=True)
