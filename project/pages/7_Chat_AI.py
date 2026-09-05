import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kobito_helper import KOBITO_IMAGES, get_base64_image_from_url

# ==================================================
# ページ設定
# ==================================================

st.set_page_config(
    page_title="SafeBox 防災コンシェルジュ",
    page_icon="🧰",
    layout="wide"
)

# ==================================================
# 小人画像（base64化してHTMLに直接埋め込む）
# ==================================================

kobito_b64 = get_base64_image_from_url(KOBITO_IMAGES["chat"])

# ==================================================
# CSS（全体デザイン刷新）
# ==================================================

st.markdown(f"""
<style>

.stApp {{
    background: linear-gradient(180deg, #fff8f0 0%, #fef1f1 100%);
}}

.block-container{{
    padding-top:1.5rem;
    max-width: 900px;
}}

/* ヘッダーバナー */
.chat-header {{
    background: linear-gradient(135deg, #ff9a76, #ff6f91);
    border-radius: 20px;
    padding: 22px 28px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 6px 16px rgba(255,111,145,0.3);
}}
.chat-header h1 {{
    margin: 0;
    font-size: 26px;
}}
.chat-header p {{
    margin: 6px 0 0 0;
    opacity: 0.9;
    font-size: 14px;
}}

/* カテゴリボタン（大きめカード風） */
.stButton>button{{
    width:100%;
    height:64px;
    border-radius:16px;
    font-weight:700;
    font-size:16px;
    border: none;
    background: white;
    color: #444;
    box-shadow: 0 3px 8px rgba(0,0,0,0.08);
    transition: 0.15s;
}}
.stButton>button:hover{{
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.12);
    background: #fff0eb;
}}

/* 吹き出しチャット行 */
.chat-row {{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 22px;
}}
.chat-row.user {{
    flex-direction: row-reverse;
}}

.chat-avatar {{
    width: 90px;
    height: 90px;
    object-fit: contain;
    flex-shrink: 0;
    filter: drop-shadow(0 3px 6px rgba(0,0,0,0.15));
}}

.chat-bubble {{
    position: relative;
    background: white;
    border-radius: 20px;
    padding: 18px 22px;
    max-width: 75%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    font-size: 15.5px;
    line-height: 1.7;
}}

.chat-bubble.assistant::before {{
    content: "";
    position: absolute;
    left: -10px;
    top: 24px;
    border-width: 10px 12px 10px 0;
    border-style: solid;
    border-color: transparent white transparent transparent;
}}

.chat-bubble.user {{
    background: #ff6f91;
    color: white;
}}
.chat-bubble.user::before {{
    content: "";
    position: absolute;
    right: -10px;
    top: 24px;
    border-width: 10px 0 10px 12px;
    border-style: solid;
    border-color: transparent transparent transparent #ff6f91;
}}

.chat-bubble h2 {{
    font-size: 19px;
    margin-top: 0;
}}
.chat-bubble h3 {{
    font-size: 15.5px;
    color: #ff6f91;
    margin-bottom: 4px;
}}

/* 詳細・戻るボタンを横並びのピル型に */
.detail-btn-row .stButton>button {{
    height: 48px;
    border-radius: 24px;
    font-size: 14px;
}}

</style>
""", unsafe_allow_html=True)

def render_message(role, content):
    if role == "assistant":
        st.markdown(f"""
        <div class="chat-row assistant">
            <img class="chat-avatar" src="data:image/png;base64,{kobito_b64}">
            <div class="chat-bubble assistant">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-row user">
            <div class="chat-bubble user">{content}</div>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# セッション
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "category" not in st.session_state:
    st.session_state.category = None

if "welcome" not in st.session_state:
    st.session_state.welcome = False

if "show_detail_button" not in st.session_state:
    st.session_state.show_detail_button = None  # 「もっと詳しく」を出すカテゴリ名を保持

# ==================================================
# 回答データ（カテゴリ名・内容は自由に書き換えてください）
# ==================================================

responses = {
    "地震": {
        "title": "🌍 地震が起きたら",
        "conclusion": "まず机の下など、頭と体を守れる場所へ移動しましょう。",
        "reason": "揺れている間は、家具の転倒や物の落下が一番の危険です。",
        "actions": ["頭を守る姿勢を取る", "揺れが収まるまで動かない", "火の元・ガスを確認する", "スマホで避難情報を確認する"],
        "tip": "揺れが収まってから、慌てず落ち着いて行動しましょう。",
        "detail": {
            "conclusion": "揺れの最中はまず身の安全、揺れが収まった後は二次災害への備えが重要です。",
            "actions": [
                "揺れが収まったら、ドアや窓を開けて避難経路を確保する",
                "ガラスの破片などに注意し、スリッパや靴を履く",
                "家族の安否をまず声で確認する",
                "余震に備えて、しばらくは大きな家具から離れて過ごす",
                "自治体や気象庁の情報をチェックし、避難が必要か判断する"
            ],
            "tip": "同じ地域でも被害状況は家庭ごとに違います。慌てず一つずつ確認していきましょう。"
        }
    },
    "備蓄": {
        "title": "📦 備蓄の準備",
        "conclusion": "最低3日分、できれば1週間分の水・食料を備えておきましょう。",
        "reason": "災害時は物流が止まり、お店で買えなくなることがあります。",
        "actions": ["飲料水(1人1日3L目安)を確認する", "非常食を確認する", "乾電池・モバイルバッテリーを準備する", "常備薬を確認する"],
        "tip": "普段の食品を少し多めに買っておき、使ったら買い足す「ローリングストック」がおすすめです。",
        "detail": {
            "conclusion": "備蓄は「量」だけでなく「家族構成に合わせた中身」も大切です。",
            "actions": [
                "乳幼児がいる場合はミルク・おむつも備える",
                "高齢者がいる場合は普段飲んでいる薬を多めに確保する",
                "ペットがいる場合はペットフードや水も忘れずに",
                "カセットコンロなど、電気なしで調理できる道具も用意する",
                "半年に一度、賞味期限や使用期限をチェックする習慣をつける"
            ],
            "tip": "SafeBox Managerの「防災グッズ管理」ページで期限を一括管理できます。"
        }
    },
    "避難": {
        "title": "🏫 避難するときは",
        "conclusion": "避難所の場所と、そこまでの安全な道を事前に確認しておきましょう。",
        "reason": "災害時は道路の状況が変わり、いつもの道が使えないことがあります。",
        "actions": ["最寄りの避難所を確認する", "実際に歩いて避難経路を確認する", "経路上の危険箇所(ブロック塀・崖など)を確認する"],
        "tip": "昼と夜、両方の時間帯で経路を確認しておくとより安心です。",
        "detail": {
            "conclusion": "避難は「早めの判断」と「複数の避難ルートの把握」が鍵になります。",
            "actions": [
                "自治体が指定するハザードマップを確認する",
                "第一避難場所と第二避難場所の両方を決めておく",
                "車での避難が難しい場合を想定し、徒歩ルートも確認する",
                "避難時に持ち出す荷物(避難バッグ)をすぐ取れる場所に置いておく",
                "近所で助け合える人がいないか、日頃から把握しておく"
            ],
            "tip": "「早すぎるかも」と思うタイミングでの避難が、結果的に一番安全です。"
        }
    },
    "家族": {
        "title": "👨‍👩‍👧 家族との連絡",
        "conclusion": "災害時の連絡方法と集合場所を、家族であらかじめ決めておきましょう。",
        "reason": "災害直後は電話がつながりにくくなることが多いです。",
        "actions": ["災害用伝言ダイヤル「171」の使い方を確認する", "家族の集合場所を決めておく", "避難所の情報を家族で共有しておく"],
        "tip": "171は体験利用できる日があるので、家族で一度練習しておくと安心です。",
        "detail": {
            "conclusion": "連絡手段は一つに絞らず、複数用意しておくと安心です。",
            "actions": [
                "電話以外に、SNSやメッセージアプリでの連絡方法も決めておく",
                "遠方の親戚を「安否確認の中継役」に決めておく(被災地同士は連絡が取りにくいため)",
                "子どもにも、家族の集合場所と連絡方法を教えておく",
                "職場や学校からの帰宅が難しい場合の対応も話し合っておく"
            ],
            "tip": "「もしバラバラの場所にいたら、どうする？」を一度家族で話しておきましょう。"
        }
    },
    "生活": {
        "title": "⚡ 停電・断水になったら",
        "conclusion": "まずスマホの充電と、飲み水の確保を優先しましょう。",
        "reason": "停電や断水は、数時間〜数日続くことがあります。",
        "actions": ["モバイルバッテリーで充電を確保する", "お風呂の水を貯めるなど生活用水を確保する", "冷蔵庫の開閉をできるだけ減らす"],
        "tip": "保冷剤や保冷バッグがあると、冷蔵庫の中身を長持ちさせられます。",
        "detail": {
            "conclusion": "停電・断水時は「情報」「衛生」「食品管理」の3点を意識しましょう。",
            "actions": [
                "携帯ラジオなど、電池で使える情報収集手段を用意する",
                "簡易トイレや携帯トイレを備えておく",
                "常温保存できる食品を優先して消費する",
                "カセットコンロがあれば温かい食事を用意できる",
                "断水が長引く場合は給水車の情報を自治体サイトで確認する"
            ],
            "tip": "普段から「電気・水がなくても1日過ごせるか」を意識してみると備えが見えてきます。"
        }
    },
    "メンタル": {
        "title": "🧠 不安なときは",
        "conclusion": "まず深呼吸をして、今できることから一つずつ落ち着いて行いましょう。",
        "reason": "災害時の不安や緊張は自然な反応です。焦らないことが大切です。",
        "actions": ["ゆっくり深呼吸をする", "信頼できる人と話す", "正確な情報源(自治体・気象庁など)を確認する"],
        "tip": "一人で抱え込まず、周りの人に気持ちを話すことも大切なケアです。",
        "detail": {
            "conclusion": "不安は「情報不足」や「孤立感」から強くなりやすいので、それぞれに対処しましょう。",
            "actions": [
                "デマや不確かな情報に振り回されないよう、公式情報源を確認する",
                "子どもや高齢者には、年齢に合わせた分かりやすい言葉で状況を伝える",
                "眠れない・食欲がないなど体調の変化がないか家族で気にかけ合う",
                "少しでも安心できる時間(好きな飲み物を飲むなど)を作る",
                "長引く不安がある場合は、無理せず専門の相談窓口に頼る"
            ],
            "tip": "「不安を感じるのは当然のこと」と受け止めるだけでも、少し楽になります。"
        }
    }
}

# ==================================================
# ヘッダー
# ==================================================

st.markdown("""
<div class="chat-header">
    <h1>🏠 SafeBox 防災コンシェルジュ</h1>
    <p>気になることを選んで、防災の知恵を聞いてみよう</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# チャット履歴表示
# ==================================================

for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"])

# ==================================================
# 初回メッセージ
# ==================================================

if not st.session_state.welcome:
    st.session_state.messages.append({
        "role": "assistant",
        "content": """<h2>👋 ようこそ！</h2>
私は <b>SafeBox 防災コンシェルジュ</b> です。<br>
専門家ではありませんが、あなたの状況に合わせて
できる限りの防災知識をお伝えします。<br>
一緒に安全を守る方法を考えていきましょう。<br><br>
相談したいカテゴリを選んでください。"""
    })
    st.session_state.welcome = True
    st.rerun()

# ==================================================
# カテゴリ選択
# ==================================================

if st.session_state.category is None:

    render_message("assistant", "📂 カテゴリを選択してください")

    col1, col2, col3 = st.columns(3)

    if col1.button("🌍 地震"):
        st.session_state.category = "地震"
        st.rerun()

    if col2.button("📦 備蓄"):
        st.session_state.category = "備蓄"
        st.rerun()

    if col3.button("🏫 避難"):
        st.session_state.category = "避難"
        st.rerun()

    col4, col5, col6 = st.columns(3)

    if col4.button("👨‍👩‍👧 家族"):
        st.session_state.category = "家族"
        st.rerun()

    if col5.button("⚡ 停電・断水"):
        st.session_state.category = "生活"
        st.rerun()

    if col6.button("🧠 メンタル"):
        st.session_state.category = "メンタル"
        st.rerun()

# ==================================================
# カテゴリが選ばれたら回答（基本情報）
# ==================================================

if st.session_state.category:

    data = responses[st.session_state.category]

    actions_html = "".join([f"・{a}<br>" for a in data["actions"]])

    answer = f"""<h2>{data['title']}</h2>
<h3>① 結論</h3>
{data['conclusion']}
<h3>② 理由</h3>
{data['reason']}
<h3>③ 具体的な行動</h3>
{actions_html}
<h3>④ アドバイス</h3>
{data['tip']}
"""

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # 「もっと詳しく」ボタンを出すためにカテゴリを記憶しておく
    st.session_state.show_detail_button = st.session_state.category
    st.session_state.category = None
    st.rerun()

# ==================================================
# 「もっと詳しく」ボタン & カテゴリに戻るボタン
# ==================================================

if st.session_state.show_detail_button:

    st.markdown('<div class="detail-btn-row">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    if col1.button("🔍 もっと詳しく"):

        data = responses[st.session_state.show_detail_button]
        detail = data["detail"]

        detail_actions_html = "".join([f"・{a}<br>" for a in detail["actions"]])

        detail_answer = f"""<h2>{data['title']}（もっと詳しく）</h2>
<h3>追加の結論</h3>
{detail['conclusion']}
<h3>追加の行動</h3>
{detail_actions_html}
<h3>追加のアドバイス</h3>
{detail['tip']}
"""

        st.session_state.messages.append({
            "role": "assistant",
            "content": detail_answer
        })

        st.session_state.show_detail_button = None
        st.rerun()

    if col2.button("📂 カテゴリに戻る"):
        st.session_state.show_detail_button = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# 履歴削除
# ==================================================

if st.button("🗑️ チャット履歴を削除"):
    st.session_state.messages = []
    st.session_state.category = None
    st.session_state.welcome = False
    st.session_state.show_detail_button = None
    st.rerun()
