import streamlit as st
import random

# ==================================================
# ページ設定
# ==================================================

st.set_page_config(
    page_title="SafeBox 防災コンシェルジュ",
    page_icon="🤖",
    layout="wide"
)

# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>
.block-container{
    padding-top:2rem;
}
.stButton>button{
    width:100%;
    height:55px;
    border-radius:12px;
    font-weight:bold;
    font-size:16px;
}
.stChatMessage{
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# セッション
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "category" not in st.session_state:
    st.session_state.category = None

if "welcome" not in st.session_state:
    st.session_state.welcome = False

# ==================================================
# 回答データ
# ==================================================

responses = {
    "地震": {
        "title": "🌍 地震",
        "conclusion": "まず机の下など安全な場所で身を守りましょう。",
        "reason": "揺れている最中は落下物や家具の転倒が最も危険です。",
        "actions": ["頭を守る", "揺れが収まるまで待つ", "火の元を確認する", "避難情報を確認する"],
        "family": ["家族の安否確認", "集合場所を確認する"],
        "items": ["懐中電灯", "水", "非常食", "モバイルバッテリー"],
        "tip": "揺れが収まってから落ち着いて行動しましょう。"
    },
    "備蓄": {
        "title": "📦 備蓄",
        "conclusion": "最低3日分、できれば7日分の備蓄を準備しましょう。",
        "reason": "災害時は物流が止まる可能性があります。",
        "actions": ["水を確認", "非常食を確認", "乾電池を確認", "薬を準備"],
        "family": ["乳幼児用品", "高齢者用品"],
        "items": ["飲料水", "非常食", "乾電池", "常備薬"],
        "tip": "普段から消費しながら備えるローリングストックがおすすめです。"
    },
    "避難": {
        "title": "🏫 避難",
        "conclusion": "避難所と避難経路を事前に確認しましょう。",
        "reason": "災害時は道路状況が変わる可能性があります。",
        "actions": ["避難所を確認", "避難経路を歩いてみる", "危険箇所を確認"],
        "family": ["集合場所を決める", "連絡方法を確認する"],
        "items": ["避難バッグ", "ライト", "飲料水"],
        "tip": "昼と夜の避難経路を確認しておくと安心です。"
    },
    "家族": {
        "title": "👨‍👩‍👧 家族",
        "conclusion": "家族との連絡方法を決めておきましょう。",
        "reason": "電話がつながらないことがあります。",
        "actions": ["171を確認", "集合場所を決める", "避難所を共有する"],
        "family": ["子どもにも避難方法を教える"],
        "items": ["連絡先一覧", "充電器"],
        "tip": "災害用伝言ダイヤル171を覚えておきましょう。"
    },
    "生活": {
        "title": "⚡ 停電・断水",
        "conclusion": "まず水と電源を確保しましょう。",
        "reason": "停電・断水は数日続く場合があります。",
        "actions": ["充電を節約する", "水を確保する", "冷蔵庫の開閉を減らす"],
        "family": ["高齢者や子どもを優先する"],
        "items": ["水", "乾電池", "ライト"],
        "tip": "保冷バッグがあると食品を長持ちさせられます。"
    },
    "メンタル": {
        "title": "🧠 メンタル",
        "conclusion": "まず深呼吸して落ち着きましょう。",
        "reason": "冷静な判断が安全につながります。",
        "actions": ["深呼吸する", "周囲の人と話す", "正しい情報を確認する"],
        "family": ["子どもの不安に寄り添う"],
        "items": ["飲み物", "毛布"],
        "tip": "一人で抱え込まず、周囲に相談しましょう。"
    }
}

# ==================================================
# チャット履歴表示
# ==================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==================================================
# 初回メッセージ
# ==================================================

if not st.session_state.welcome:
    st.session_state.messages.append({
        "role": "assistant",
        "content": """
## 👋 ようこそ！

私は **SafeBox 防災コンシェルジュ** です。
専門家ではありませんが、あなたの状況に合わせて  
できる限りの防災知識をお伝えします。  
一緒に安全を守る方法を考えていきましょう。

相談したいカテゴリを選んでください。
"""
    })
    st.session_state.welcome = True
    st.rerun()

# ==================================================
# カテゴリ選択
# ==================================================

if st.session_state.category is None:

    with st.chat_message("assistant"):
        st.write("📂 カテゴリを選択してください")

        col1, col2, col3 = st.columns(3)

        if col1.button("🌍 地震"):
            st.session_state.category = "地震"
            st.rerun()

        if col2.button("📦 備蓄"):
            st.session_state.category = "備蓄"
            st.rerun()

        if col3.button("🏫 避難"):
            st.session_state.category = "避難"
            st.rerun()

        col4, col5, col6 = st.columns(3)

        if col4.button("👨‍👩‍👧 家族"):
            st.session_state.category = "家族"
            st.rerun()

        if col5.button("⚡ 停電・断水"):
            st.session_state.category = "生活"
            st.rerun()

        if col6.button("🧠 メンタル"):
            st.session_state.category = "メンタル"
            st.rerun()

# ==================================================
# カテゴリが選ばれたら即回答（相談内容は固定）
# ==================================================

if st.session_state.category:

    data = responses[st.session_state.category]

    answer = f"""
## {data['title']}

### 相談内容  
**どうすればいい？**

### ① 結論  
{data['conclusion']}

### ② 理由  
{data['reason']}

### ③ 具体的な行動  
- {'\n- '.join(data['actions'])}

### ④ 家族への配慮  
- {'\n- '.join(data['family'])}

### ⑤ 備えておくもの  
- {'\n- '.join(data['items'])}

### ⑥ アドバイス  
{data['tip']}
"""

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.session_state.category = None
    st.rerun()

#=================================================
#履歴削除
#=================================================

if st.button("🗑️ チャット履歴を削除"):
    st.session_state.messages = []
    st.session_state.category = None
    st.session_state.welcome = False
    st.rerun()