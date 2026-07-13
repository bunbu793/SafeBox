import streamlit as st

st.title("🧠 AI 防災コンシェルジュ")
st.write("災害・家族・生活のことなど、なんでも AI に相談できます。")

# チャット履歴
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 過去のメッセージを表示
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ユーザー入力
user_input = st.chat_input("相談内容を入力してください（例：地震が起きたらどうすればいい？）")

if user_input:
    # ユーザーのメッセージを追加
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # AI の返答を生成
    with st.chat_message("assistant"):
        response = f"""
あなたは防災コンシェルジュです。
以下の相談に対して、わかりやすく丁寧に回答してください。

相談内容：
{user_input}

回答は以下の構成でお願いします：

1. 結論（まず何をすべきか）
2. 理由（なぜその行動が必要か）
3. 具体的な行動ステップ
4. 家族がいる場合の注意点
5. 持ち物・準備
6. 心のケア・安心のための一言
"""
        st.write(response)

    # AI の返答を履歴に追加
    st.session_state["messages"].append({"role": "assistant", "content": response})
