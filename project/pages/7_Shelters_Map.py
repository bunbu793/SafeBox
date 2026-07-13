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
        "食料・水（備蓄）",
        "避難所・避難経路",
        "家族との連絡・安否確認",
        "災害時の行動（地震・台風・火災）",
        "持ち物（防災バッグ）",
        "メンタルケア（不安・怖い）",
        "生活の困りごと（停電・断水）",
        "その他"
    ]
)

user_input = st.chat_input("例：何を買えばいい？ / 地震が怖い / 避難所はどこ？")

if user_input:

    # ユーザーの発言
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    text = user_input.lower()

    # --- ① 結論（相談内容で変化） ---
    if "買" in text or "備蓄" in text:
        conclusion = "まずは水・食料・ライト・モバイルバッテリーを優先して揃えましょう。"
    elif "地震" in text:
        conclusion = "まずは机の下など安全な場所で身を守ることが最優先です。"
    elif "避難所" in text or "避難" in text:
        conclusion = "最寄りの避難所を事前に確認し、ルートを把握しておきましょう。"
    elif "家族" in text:
        conclusion = "家族とは集合場所と連絡手段を事前に決めておくことが重要です。"
    else:
        conclusion = "まずは落ち着いて状況を整理し、安全を確保しましょう。"

    # --- ② 理由（相談内容で変化） ---
    if "怖" in text or "不安" in text:
        reason = "不安を感じると判断力が低下するため、まずは心を落ち着けることが大切です。"
    elif "買" in text or "備蓄" in text:
        reason = "災害時は物流が止まりやすく、必要な物資が手に入りにくくなるためです。"
    else:
        reason = "災害時は焦りが危険につながるため、冷静な判断が重要です。"

    # --- ③ 具体的な行動（カテゴリで変化） ---
    if "避難所・避難経路" in categories:
        actions = """
- 最寄りの避難所を確認  
- 避難ルートを2つ以上確保  
- 夜間でも通れる道を確認  
"""
    elif "食料・水（備蓄）" in categories or "買" in text:
        actions = """
- 水・食料を3日分確保  
- モバイルバッテリーを充電  
- 懐中電灯の電池確認  
"""
    elif "災害時の行動（地震・台風・火災）" in categories:
        actions = """
- 周囲の安全確認  
- 家具の転倒防止  
- 最新の災害情報を確認  
"""
    else:
        actions = """
- 周囲の安全確認  
- 必要なら避難経路の確保  
- 家族や周囲の人と連絡  
- 最新の災害情報を確認  
"""

    # --- ④ 家族への配慮（カテゴリで変化） ---
    if "家族との連絡・安否確認" in categories or "家族" in text:
        family = """
- 家族の安否確認  
- 集合場所の共有  
- 子どもや高齢者のサポート  
"""
    else:
        family = """
- 家族と連絡を取り合う  
- 集合場所を確認する  
"""

    # --- ⑤ 備えておくもの（カテゴリで変化） ---
    if "食料・水（備蓄）" in categories or "買" in text:
        items = """
- 水・食料  
- モバイルバッテリー  
- 懐中電灯  
- 救急セット  
- 常備薬  
"""
    elif "持ち物（防災バッグ）" in categories:
        items = """
- 非常食  
- 飲料水  
- ライト  
- 電池  
- モバイルバッテリー  
- 救急セット  
"""
    else:
        items = """
- 水・食料  
- 懐中電灯  
- 電池  
- モバイルバッテリー  
"""

    # --- ⑥ 安心できる一言（相談内容で変化） ---
    if "怖" in text or "不安" in text or "メンタルケア（不安・怖い）" in categories:
        comfort = "あなたの不安は自然なものです。ゆっくり準備していけば大丈夫です。"
    else:
        comfort = "できることから一つずつ進めれば、必ず安全に近づきます。"

    # --- まとめ（カテゴリは表示しない） ---
    answer = f"""
「{user_input}」という相談ですね。

① **結論**  
{conclusion}

② **理由**  
{reason}

③ **具体的な行動**  
{actions}

④ **家族への配慮**  
{family}

⑤ **備えておくもの**  
{items}

⑥ **安心できる一言**  
{comfort}
"""

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
