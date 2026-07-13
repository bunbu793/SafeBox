import streamlit as st
import ollama

# 初回だけ履歴を作成
if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.chat_input("相談内容を入力してください")

if user_input:

    st.session_state["messages"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    response = ollama.chat(
        model="gemma3",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    answer = response["message"]["content"]

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state["messages"].append(
        {"role": "assistant", "content": answer}
    )