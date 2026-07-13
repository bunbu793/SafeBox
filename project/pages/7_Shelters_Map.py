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

user_input = st.chat_input("例：何を買えばいい？ / 地震が怖い / 避難所はどこ？")

if user_input:

    # ユーザーの発言
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # カテゴリ
    category_text = "、".join(categories) if categories else "未選択"

    # --- 疑似AIロジック（相談内容で回答が変わる） ---
    text = user_input.lower()

    if "買" in text or "備蓄" in text or "必要" in text:
        main = "まずは水・食料・ライト・モバイルバッテリーの4つを優先しましょう。"
    elif "地震" in text:
        main = "まずは机の下など安全な場所で身を守ることが最優先です。"
    elif "避難所" in text or "どこ" in text:
        main = "自治体が指定する避難所を事前に確認し、最短ルートを把握しておきましょう。"
    elif "家族" in text or "連絡" in text:
        main = "家族とは集合場所と連絡手段を事前に決めておくことが重要です。"
    elif "怖" in text or "不安" in text:
        main = "不安を感じるのは自然なことです。まずは情報を整理し、できる準備から始めましょう。"
    else:
        main = "まずは状況を整理し、安全を確保することが大切です。"

    # --- 返答テンプレ ---
    answer = f"""
「{user_input}」という相談ですね。

① **結論**  
{main}

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

    # AIの回答
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
