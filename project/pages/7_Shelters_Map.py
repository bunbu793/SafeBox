import streamlit as st

# =====================================================
# ページ設定
# =====================================================

st.set_page_config(
    page_title="SafeBox 防災コンシェルジュ",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SafeBox 防災コンシェルジュ")
st.caption("災害・備蓄・避難などをサポートします（AI APIは使用していません）")

# =====================================================
# セッション管理
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# =====================================================
# 回答データ
# =====================================================

responses = {

    "地震": {
        "title":"🌍 地震",

        "conclusion":"まずは机の下など安全な場所で身を守りましょう。",

        "reason":"地震では家具の転倒や落下物が大きな危険になります。",

        "actions":[
            "頭を守る",
            "揺れが収まるまで動かない",
            "火の元を確認する",
            "避難情報を確認する"
        ],

        "family":[
            "家族の安否確認",
            "集合場所を確認"
        ],

        "items":[
            "水",
            "非常食",
            "懐中電灯",
            "モバイルバッテリー"
        ],

        "tip":"家具固定器具を付けると被害を減らせます。"
    },

    "備蓄":{

        "title":"📦 備蓄",

        "conclusion":"最低3日分、できれば7日分の備蓄を用意しましょう。",

        "reason":"災害直後は物流が止まる場合があります。",

        "actions":[
            "水を人数分準備",
            "非常食を確認",
            "乾電池を交換",
            "薬を準備"
        ],

        "family":[
            "赤ちゃんや高齢者の用品も準備"
        ],

        "items":[
            "飲料水",
            "非常食",
            "乾電池",
            "救急セット",
            "ラジオ"
        ],

        "tip":"普段から使いながら備蓄するローリングストックがおすすめです。"
    },

    "避難":{

        "title":"🏫 避難",

        "conclusion":"最寄りの指定避難所を事前に確認しておきましょう。",

        "reason":"災害時は道路状況が変わることがあります。",

        "actions":[
            "避難所を確認",
            "避難経路を歩いて確認",
            "危険箇所を把握"
        ],

        "family":[
            "家族で集合場所を決める"
        ],

        "items":[
            "避難バッグ",
            "飲料水",
            "ライト"
        ],

        "tip":"昼と夜の両方で避難経路を確認しておきましょう。"
    },

    "家族":{

        "title":"👨‍👩‍👧 家族",

        "conclusion":"連絡方法と集合場所を事前に決めておきましょう。",

        "reason":"電話がつながりにくくなる場合があります。",

        "actions":[
            "171を確認",
            "集合場所を決める",
            "避難所を共有する"
        ],

        "family":[
            "子どもにも避難方法を教える"
        ],

        "items":[
            "連絡先一覧",
            "モバイルバッテリー"
        ],

        "tip":"災害用伝言ダイヤル171の使い方を確認しておきましょう。"
    },

    "生活":{

        "title":"⚡ 停電・断水",

        "conclusion":"まず生活に必要な水と電源を確保しましょう。",

        "reason":"停電や断水は数日続く場合があります。",

        "actions":[
            "充電を節約",
            "飲料水を確保",
            "冷蔵庫の開閉を減らす"
        ],

        "family":[
            "高齢者や乳幼児を優先"
        ],

        "items":[
            "水",
            "ライト",
            "電池",
            "モバイルバッテリー"
        ],

        "tip":"保冷バッグがあると食品が長持ちします。"
    },

    "メンタル":{

        "title":"🧠 メンタルケア",

        "conclusion":"まず深呼吸をして落ち着きましょう。",

        "reason":"焦ると判断ミスにつながります。",

        "actions":[
            "深呼吸",
            "周囲と話す",
            "正しい情報を見る"
        ],

        "family":[
            "子どもや高齢者の不安に寄り添う"
        ],

        "items":[
            "飲み物",
            "毛布"
        ],

        "tip":"一人で抱え込まず、周囲に相談しましょう。"
    }
}

# =====================================================
# 防災豆知識
# =====================================================

tips = [
    "💡 水は1人1日3Lが目安です。",
    "💡 非常食は賞味期限を定期的に確認しましょう。",
    "💡 家具固定で地震被害を減らせます。",
    "💡 モバイルバッテリーは常に充電しておきましょう。",
    "💡 家族で避難場所を共有しておきましょう。"
]

# =====================================================
# チャット履歴表示
# =====================================================

for msg in st.session_state.messages:

    avatar = "🤖" if msg["role"] == "assistant" else "🧑"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# =====================================================
# カテゴリ選択
# =====================================================

if st.session_state.selected_category is None:

    with st.chat_message("assistant", avatar="🤖"):

        st.markdown("## 📂 相談カテゴリを選んでください")

        row1 = st.columns(3)

        if row1[0].button("📦 備蓄", use_container_width=True):
            st.session_state.selected_category = "備蓄"
            st.session_state.messages.append({
                "role": "assistant",
                "content": "📦 **備蓄** が選択されました。\n\n相談内容を入力してください。"
            })
            st.rerun()

        if row1[1].button("🌍 地震", use_container_width=True):
            st.session_state.selected_category = "地震"
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🌍 **地震** が選択されました。\n\n相談内容を入力してください。"
            })
            st.rerun()

        if row1[2].button("🏫 避難", use_container_width=True):
            st.session_state.selected_category = "避難"
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🏫 **避難** が選択されました。\n\n相談内容を入力してください。"
            })
            st.rerun()

        row2 = st.columns(3)

        if row2[0].button("👨‍👩‍👧 家族", use_container_width=True):
            st.session_state.selected_category = "家族"
            st.session_state.messages.append({
                "role": "assistant",
                "content": "👨‍👩‍👧 **家族** が選択されました。\n\n相談内容を入力してください。"
            })
            st.rerun()

        if row2[1].button("⚡ 停電・断水", use_container_width=True):
            st.session_state.selected_category = "生活"
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚡ **停電・断水** が選択されました。\n\n相談内容を入力してください。"
            })
            st.rerun()

        if row2[2].button("🧠 メンタル", use_container_width=True):
            st.session_state.selected_category = "メンタル"
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🧠 **メンタル** が選択されました。\n\n相談内容を入力してください。"
            })
            st.rerun()

# =====================================================
# 入力欄
# =====================================================

user_input = st.chat_input("相談内容を入力してください")

# =====================================================
# 回答処理
# =====================================================

if user_input:

    # ユーザーの発言を保存
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 選択されたカテゴリ
    category = st.session_state.selected_category

    # カテゴリ未選択の場合
    if category is None:
        category = "地震"

    data = responses[category]

    # 箇条書きを生成
    actions = "\n".join([f"- {a}" for a in data["actions"]])
    family = "\n".join([f"- {a}" for a in data["family"]])
    items = "\n".join([f"- {a}" for a in data["items"]])

    answer = f"""
## {data["title"]}

### 📌 結論

{data["conclusion"]}

---

### 📖 理由

{data["reason"]}

---

### ✅ 具体的な行動

{actions}

---

### 👨‍👩‍👧 家族への配慮

{family}

---

### 🎒 備えておくもの

{items}

---

### 💡 ワンポイント

{data["tip"]}

---

**あなたの相談内容**

> {user_input}

落ち着いて行動すれば、安全に近づくことができます。
"""

    # AIの回答を保存
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # カテゴリをリセット
    st.session_state.selected_category = None

    st.rerun()

# =====================================================
# サイドバー
# =====================================================

with st.sidebar:

    st.header("🛡 SafeBox")

    st.success("防災コンシェルジュ")

    st.divider()

    st.subheader("📊 利用状況")

    user_count = len(
        [m for m in st.session_state.messages if m["role"] == "user"]
    )

    st.metric(
        label="相談件数",
        value=user_count
    )

    st.divider()

    st.subheader("💡 今日の防災豆知識")

    import random

    st.info(random.choice(tips))

    st.divider()

    if st.button("🗑 チャット履歴を削除", use_container_width=True):

        st.session_state.messages = []

        st.session_state.selected_category = None

        st.rerun()


# =====================================================
# フッター
# =====================================================

st.divider()

st.caption(
    "© SafeBox Disaster Concierge"
)

# =====================================================
# デザイン
# =====================================================

st.markdown(
    """
<style>

.stChatMessage{
    border-radius:18px;
    padding:15px;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:55px;
    font-size:17px;
    font-weight:bold;
}

div[data-testid="stMetric"]{
    border-radius:12px;
    padding:10px;
}

</style>
""",
    unsafe_allow_html=True
)