import streamlit as st

st.set_page_config(
    page_title="AI 防災コンシェルジュ",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI 防災コンシェルジュ")
st.write("災害・家族・生活のことなど、なんでも相談できます。（※AI APIは使用していません）")

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

user_input = st.chat_input("例：地震が不安です / 家族と離れたらどうする？ / 避難所はどこ？")

if user_input:

    # ユーザーの発言
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # カテゴリ
    category_text = "、".join(categories) if categories else "未選択"

    # ユーザーの相談内容を引用してチャット感を出す
    intro = f"「{user_input}」という相談ですね。まずは状況を整理しましょう。"

    # APIなしの内部ロジックで回答生成
    answer = f"""
### 🧠 防災コンシェルジュ

{intro}

① **結論**  
まずは落ち着いて、あなた自身の安全を確保しましょう。

② **理由**  
災害時は焦りが危険につながるため、冷静な判断が重要です。

③ **具体的な行動**  
- 周囲の安全確認  
- 必要なら避難経路の確保  
- 家族や周囲の人と連絡  
- 最新の災害情報を確認  

④ **家族への配慮**  
- 安否確認  
- 集合場所の確認  
- 子どもや高齢者のサポート  

⑤ **備えておくもの**  
- 水・食料  
- モバイルバッテリー  
- 懐中電灯  
- 救急セット  
- 常備薬  

⑥ **安心できる一言**  
あなたの不安は自然なものです。一緒に安全を確保していきましょう。
"""

    # AIの回答を表示
    with st.chat_message("assistant"):
        st.markdown(answer)

    # 履歴に追加
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
