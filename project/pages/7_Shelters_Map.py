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
# デザイン
# ==================================================

st.markdown("""
<style>

.main{
    background-color:#f7f9fc;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:55px;
    font-weight:bold;
    font-size:16px;
}

.stChatMessage{
    border-radius:18px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# タイトル
# ==================================================

st.title("🤖 SafeBox 防災コンシェルジュ")
st.write("災害時の行動や備えについて相談できます。")

# ==================================================
# セッション
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "category" not in st.session_state:
    st.session_state.category = None

# ==================================================
# 防災豆知識
# ==================================================

tips = [
    "💡 水は1人1日3Lを目安に備蓄しましょう。",
    "💡 家具固定で地震の被害を減らせます。",
    "💡 非常食は賞味期限を確認しましょう。",
    "💡 モバイルバッテリーは定期的に充電しましょう。",
    "💡 家族で集合場所を決めておきましょう。"
]

# ==================================================
# 回答データ
# ==================================================

responses = {

"地震":{

"title":"🌍 地震",

"conclusion":"まず机の下など安全な場所で身を守ってください。",

"reason":"落下物や家具の転倒が大きな危険になります。",

"actions":[
"頭を守る",
"揺れが収まるまで待つ",
"火の元を確認する",
"避難情報を見る"
],

"family":[
"家族の安否確認",
"集合場所へ向かう"
],

"items":[
"水",
"非常食",
"ライト",
"モバイルバッテリー"
],

"tip":"家具固定器具を付けると被害を減らせます。"

},

"備蓄":{

"title":"📦 備蓄",

"conclusion":"最低3日、できれば7日分準備しましょう。",

"reason":"物流が止まる可能性があります。",

"actions":[
"水を確認",
"非常食を確認",
"乾電池を交換",
"薬を準備"
],

"family":[
"乳幼児や高齢者用品も準備"
],

"items":[
"水",
"非常食",
"乾電池",
"薬",
"ラジオ"
],

"tip":"ローリングストックがおすすめです。"

},

"避難":{

"title":"🏫 避難",

"conclusion":"避難所を事前に確認しておきましょう。",

"reason":"災害時は道路状況が変わります。",

"actions":[
"避難所を確認",
"避難経路を歩いてみる",
"危険箇所を確認"
],

"family":[
"集合場所を決める"
],

"items":[
"避難バッグ",
"飲料水",
"ライト"
],

"tip":"昼と夜の避難経路を確認しましょう。"

},

"家族":{

"title":"👨‍👩‍👧 家族",

"conclusion":"連絡方法を事前に決めましょう。",

"reason":"電話がつながりにくくなることがあります。",

"actions":[
"171を確認",
"集合場所を決める",
"避難所を共有"
],

"family":[
"子どもにも避難方法を教える"
],

"items":[
"連絡先一覧",
"充電器"
],

"tip":"災害用伝言ダイヤル171を覚えておきましょう。"

},

"生活":{

"title":"⚡ 停電・断水",

"conclusion":"まず水と電源を確保しましょう。",

"reason":"停電・断水は数日続くことがあります。",

"actions":[
"充電を節約",
"飲料水を確保",
"冷蔵庫を開けすぎない"
],

"family":[
"高齢者を優先"
],

"items":[
"水",
"ライト",
"乾電池"
],

"tip":"保冷バッグがあると便利です。"

},

"メンタル":{

"title":"🧠 メンタル",

"conclusion":"まず深呼吸して落ち着きましょう。",

"reason":"焦ると判断ミスにつながります。",

"actions":[
"深呼吸",
"周囲と話す",
"正しい情報を見る"
],

"family":[
"子どもの不安に寄り添う"
],

"items":[
"飲み物",
"毛布"
],

"tip":"一人で抱え込まないことが大切です。"

}

}

# ==================================================
# チャット履歴表示
# ==================================================

for message in st.session_state.messages:

    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

    elif message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])


# ==================================================
# カテゴリ選択
# ==================================================

if st.session_state.category is None:

    with st.chat_message("assistant"):

        st.markdown("### 📂 相談したいカテゴリを選んでください")

        row1 = st.columns(3)

        if row1[0].button("🌍 地震", use_container_width=True):
            st.session_state.category = "地震"

            st.session_state.messages.append({
                "role":"assistant",
                "content":"🌍 **地震** が選択されました。\n\n相談内容を入力してください。"
            })

            st.rerun()

        if row1[1].button("📦 備蓄", use_container_width=True):
            st.session_state.category = "備蓄"

            st.session_state.messages.append({
                "role":"assistant",
                "content":"📦 **備蓄** が選択されました。\n\n相談内容を入力してください。"
            })

            st.rerun()

        if row1[2].button("🏫 避難", use_container_width=True):
            st.session_state.category = "避難"

            st.session_state.messages.append({
                "role":"assistant",
                "content":"🏫 **避難** が選択されました。\n\n相談内容を入力してください。"
            })

            st.rerun()

        row2 = st.columns(3)

        if row2[0].button("👨‍👩‍👧 家族", use_container_width=True):
            st.session_state.category = "家族"

            st.session_state.messages.append({
                "role":"assistant",
                "content":"👨‍👩‍👧 **家族** が選択されました。\n\n相談内容を入力してください。"
            })

            st.rerun()

        if row2[1].button("⚡ 停電・断水", use_container_width=True):
            st.session_state.category = "生活"

            st.session_state.messages.append({
                "role":"assistant",
                "content":"⚡ **停電・断水** が選択されました。\n\n相談内容を入力してください。"
            })

            st.rerun()

        if row2[2].button("🧠 メンタル", use_container_width=True):
            st.session_state.category = "メンタル"

            st.session_state.messages.append({
                "role":"assistant",
                "content":"🧠 **メンタル** が選択されました。\n\n相談内容を入力してください。"
            })

            st.rerun()


# ==================================================
# チャット入力
# ==================================================

user_input = st.chat_input("相談内容を入力してください")

# ==================================================
# 回答処理
# ==================================================

if user_input:

    # ユーザーのメッセージを保存
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # カテゴリ取得
    category = st.session_state.category

    if category is None:
        category = "地震"

    data = responses[category]

    # 箇条書きをMarkdownに変換
    actions = "\n".join(
        [f"- {text}" for text in data["actions"]]
    )

    family = "\n".join(
        [f"- {text}" for text in data["family"]]
    )

    items = "\n".join(
        [f"- {text}" for text in data["items"]]
    )

    # AI回答
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

### 💬 あなたの相談内容

> {user_input}

落ち着いて、一つずつ対応していけば大丈夫です。
"""

    # AIメッセージ保存
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # カテゴリをリセット
    st.session_state.category = None

    st.rerun()

# ==================================================
# サイドバー
# ==================================================

with st.sidebar:

    st.title("🛡 SafeBox")

    st.success("防災コンシェルジュ")

    st.divider()

    # 相談件数
    user_count = len(
        [m for m in st.session_state.messages if m["role"] == "user"]
    )

    st.metric(
        label="相談件数",
        value=user_count
    )

    st.divider()

    # カテゴリ表示
    if st.session_state.category is None:
        st.info("📂 カテゴリ：未選択")
    else:
        st.success(f"📂 {st.session_state.category}")

    st.divider()

    # 防災豆知識
    st.subheader("💡 今日の防災豆知識")

    if "today_tip" not in st.session_state:
        st.session_state.today_tip = random.choice(tips)

    st.info(st.session_state.today_tip)

    if st.button("🔄 豆知識を更新", use_container_width=True):
        st.session_state.today_tip = random.choice(tips)
        st.rerun()

    st.divider()

    st.subheader("📋 メニュー")

    st.write("🌍 地震")
    st.write("📦 備蓄")
    st.write("🏫 避難")
    st.write("👨‍👩‍👧 家族")
    st.write("⚡ 停電・断水")
    st.write("🧠 メンタル")

    st.divider()

    # 履歴削除
    if st.button("🗑 チャット履歴を削除", use_container_width=True):

        st.session_state.messages = []
        st.session_state.category = None

        if "today_tip" in st.session_state:
            del st.session_state.today_tip

        st.rerun()

# ==================================================
# フッター
# ==================================================

st.divider()

st.caption("🛡 SafeBox Disaster Concierge")

st.caption("災害時の判断をサポートする防災コンシェルジュ")

# ==================================================
# サイドバー
# ==================================================

with st.sidebar:

    st.title("🛡 SafeBox")

    st.success("防災コンシェルジュ")

    st.divider()

    # 相談件数
    user_count = len(
        [m for m in st.session_state.messages if m["role"] == "user"]
    )

    st.metric(
        label="相談件数",
        value=user_count
    )

    st.divider()

    # カテゴリ表示
    if st.session_state.category is None:
        st.info("📂 カテゴリ：未選択")
    else:
        st.success(f"📂 {st.session_state.category}")

    st.divider()

    # 防災豆知識
    st.subheader("💡 今日の防災豆知識")

    if "today_tip" not in st.session_state:
        st.session_state.today_tip = random.choice(tips)

    st.info(st.session_state.today_tip)

    if st.button("🔄 豆知識を更新", use_container_width=True):
        st.session_state.today_tip = random.choice(tips)
        st.rerun()

    st.divider()

    st.subheader("📋 メニュー")

    st.write("🌍 地震")
    st.write("📦 備蓄")
    st.write("🏫 避難")
    st.write("👨‍👩‍👧 家族")
    st.write("⚡ 停電・断水")
    st.write("🧠 メンタル")

    st.divider()

    # 履歴削除
    if st.button("🗑 チャット履歴を削除", use_container_width=True):

        st.session_state.messages = []
        st.session_state.category = None

        if "today_tip" in st.session_state:
            del st.session_state.today_tip

        st.rerun()

# ==================================================
# フッター
# ==================================================

st.divider()

st.caption("🛡 SafeBox Disaster Concierge")

st.caption("災害時の判断をサポートする防災コンシェルジュ")
# ==================================================
# 初回メッセージ
# ==================================================

if "welcome" not in st.session_state:

    st.session_state.messages.append({
        "role": "assistant",
        "content": """
# 🤖 SafeBoxへようこそ！

こんにちは！

私は **SafeBox 防災コンシェルジュ** です。

次のような相談ができます。

- 🌍 地震
- 📦 備蓄
- 🏫 避難
- 👨‍👩‍👧 家族
- ⚡ 停電・断水
- 🧠 メンタルケア

カテゴリを選択して相談してください。
"""
    })

    st.session_state.welcome = True


# ==================================================
# 相談終了メッセージ
# ==================================================

if len(st.session_state.messages) > 8:

    st.success("🎉 今日も防災について学習できました！")


# ==================================================
# SafeBox情報
# ==================================================

with st.expander("ℹ SafeBoxについて"):

    st.markdown("""
### 🛡 SafeBox

SafeBoxは、

災害時に必要な情報を
すぐ確認できる防災支援アプリです。

#### 主な機能

- 🤖 防災コンシェルジュ
- 🗺 避難所検索
- 📦 備蓄チェック
- 🚨 緊急連絡先
- 👨‍👩‍👧 家族情報管理
- 📱 スマホ対応

今後さらに機能追加予定です。
""")


# ==================================================
# フッター
# ==================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🛡 SafeBox")

with col2:
    st.caption("Version 2.0")

with col3:
    st.caption("Made with Streamlit")


st.markdown(
"""
<center>

### 🤖 SafeBox 防災コンシェルジュ

災害時も、いつもの安心を。

</center>
""",
unsafe_allow_html=True
)