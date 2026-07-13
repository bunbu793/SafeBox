import streamlit as st
from ollama import Ollama

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