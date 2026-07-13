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

user_input = st.chat_input("相談内容を入力してください")

if user_input:

    # ユーザーの発言
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # カテゴリ
    category_text = "、".join(categories) if categories else "未選択"

    # APIなしの内部ロジックで回答生成
    answer = f"""
### 🧠 防災コンシェルジュの回答

**相談カテゴリ:** {category_text}

① **結論**  
あなたの状況では、まず落ち着いて安全を確保することが最優先です。

② **理由**  
災害時は判断力が低下しやすく、誤った行動が危険につながるためです。

③ **具体的な行動**  
- 周囲の安全確認  
- 必要なら避難経路の確保  
- 家族や周囲の人と連絡を取る  
- 最新の災害情報を確認する  

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
あなたは今できる最善の行動をしようとしています。それだけで十分立派です。
"""

    # AIの回答を表示
    with st.chat_message("assistant"):
        st.markdown(answer)

    # 履歴に追加
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
