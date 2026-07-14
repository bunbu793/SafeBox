import streamlit as st

st.set_page_config(page_title="AI 防災コンシェルジュ", page_icon="🧠", layout="wide")

st.title("🧠 AI 防災コンシェルジュ")
st.write("災害・家族・生活のことなど、なんでも相談できます。（※AI APIは使用していません）")

# チャット履歴
if "messages" not in st.session_state:
    st.session_state.messages = []

# 選択されたカテゴリ
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# チャット履歴表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- カテゴリボタン（カテゴリ未選択のときだけ表示） ---
if st.session_state.selected_category is None:
    with st.chat_message("assistant"):
        st.write("どのカテゴリで相談しますか？")
        cols = st.columns(3)

        if cols[0].button("食料・水（備蓄）"):
            st.session_state.selected_category = "備蓄"

        if cols[1].button("避難所・避難経路"):
            st.session_state.selected_category = "避難"

        if cols[2].button("家族との連絡・安否確認"):
            st.session_state.selected_category = "家族"

        cols2 = st.columns(3)

        if cols2[0].button("災害時の行動（地震）"):
            st.session_state.selected_category = "地震"

        if cols2[1].button("メンタルケア（不安・怖い）"):
            st.session_state.selected_category = "メンタル"

        if cols2[2].button("生活の困りごと（停電・断水）"):
            st.session_state.selected_category = "生活"

# --- カテゴリが選ばれたらチャット履歴に追加 ---
if st.session_state.selected_category:
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"カテゴリ：{st.session_state.selected_category} が選ばれました。\n相談内容を入力してください。"
    })

# --- ユーザー入力 ---
user_input = st.chat_input("相談内容を入力")

if user_input:

    # ユーザーの発言
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    category = st.session_state.selected_category or "その他"
    text = user_input.lower()

    # --- ①結論 ---
    if category == "備蓄":
        conclusion = "まずは水・食料・ライト・モバイルバッテリーを優先して揃えましょう。"
    elif category == "地震":
        conclusion = "まずは机の下など安全な場所で身を守ることが最優先です。"
    elif category == "避難":
        conclusion = "最寄りの避難所を事前に確認し、ルートを把握しておきましょう。"
    elif category == "家族":
        conclusion = "家族とは集合場所と連絡手段を事前に決めておくことが重要です。"
    elif category == "メンタル":
        conclusion = "まずは深呼吸し、落ち着いて状況を整理しましょう。"
    elif category == "生活":
        conclusion = "停電や断水時は、まず安全と最低限の生活確保を優先しましょう。"
    else:
        conclusion = "まずは落ち着いて状況を整理し、安全を確保しましょう。"

    # --- ②〜⑥（簡略版） ---
    answer = f"""
「{user_input}」という相談ですね。

① **結論**  
{conclusion}

② **理由**  
災害時は焦りが危険につながるため、冷静な判断が重要です。

③ **具体的な行動**  
- 周囲の安全確認  
- 必要なら避難経路の確保  
- 家族や周囲の人と連絡  
- 最新の災害情報を確認  

④ **家族への配慮**  
- 家族と連絡を取り合う  
- 集合場所を確認する  

⑤ **備えておくもの**  
- 水・食料  
- モバイルバッテリー  
- 懐中電灯  

⑥ **安心できる一言**  
できることから一つずつ進めれば、必ず安全に近づきます。
"""

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    # 🔥 質問後カテゴリをリセット（ここが重要）
    st.session_state.selected_category = None
