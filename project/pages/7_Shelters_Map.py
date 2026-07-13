import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="AI 防災コンシェルジュ",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI 防災コンシェルジュ")
st.write("災害・家族・生活のことなど、なんでもAIに相談できます。")

# チャット履歴
if "messages" not in st.session_state:
    st.session_state.messages = []

# 表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.subheader("相談カテゴリ（複数選択OK）")

categories = st.multiselect(
    "カテゴリ",
    [
        "避難場所",
        "災害時の行動",
        "家族の安全",
        "持ち物・備蓄",
        "メンタルケア",
        "食料・水",
        "生活の不安",
        "その他"
    ]
)

user_input = st.chat_input("相談内容を入力してください")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    category_text = "、".join(categories) if categories else "未選択"

    system_prompt = f"""
あなたは防災コンシェルジュです。

相談カテゴリ
{category_text}

回答は次の順番でしてください。

①結論
②理由
③具体的な行動
④家族への配慮
⑤備えておくもの
⑥安心できる一言

正確で分かりやすく回答してください。
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for msg in st.session_state.messages:
        messages.append(msg)

    with st.chat_message("assistant"):

        with st.spinner("考えています..."):

            response = client.chat.completions.create(
                model="gpt-5",
                messages=messages
            )

            answer = response.choices[0].message.content

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )