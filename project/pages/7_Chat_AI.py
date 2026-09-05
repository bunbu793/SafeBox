import streamlit as st
import requests
from io import BytesIO
from PIL import Image

from kobito_helper import KOBITO_IMAGE_URL

# ==================================================
# ページ設定
# ==================================================

st.set_page_config(
    page_title="SafeBox 防災コンシェルジュ",
    page_icon="🧰",
    layout="wide"
)

# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>
.block-container{
    padding-top:2rem;
}
.stButton>button{
    width:100%;
    height:55px;
    border-radius:12px;
    font-weight:bold;
    font-size:16px;
}
.stChatMessage{
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 小人アイコン（アシスタントのアバターとして使用）
# ==================================================

@st.cache_data
def load_kobito_avatar():
    response = requests.get(KOBITO_IMAGE_URL)
    return Image.open(BytesIO(response.content))

kobito_avatar = load_kobito_avatar()

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
# チャット履歴表示
# ==================================================

for msg in st.session_state.messages:
    avatar = kobito_avatar if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ==================================================
# 初回メッセージ
# ==================================================

if not st.session_state.welcome:
    st.session_state.messages.append({
        "role": "assistant",
        "content": """## 👋 ようこそ！

私は **SafeBox 防災コンシェルジュ** です。
専門家ではありませんが、あなたの状況に合わせて
できる限りの防災知識をお伝えします。
一緒に安全を守る方法を考えていきましょう。

相談したいカテゴリを選んでください。
"""
    })
    st.session_state.welcome = True
    st.rerun()

# ==================================================
# カテゴリ選択
# ==================================================

if st.session_state.category is None:

    with st.chat_message("assistant", avatar=kobito_avatar):
        st.write("📂 カテゴリを選択してください")

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

    actions_text = "\n- ".join(data["actions"])

    answer = f"""## {data['title']}

### ① 結論
{data['conclusion']}

### ② 理由
{data['reason']}

### ③ 具体的な行動
- {actions_text}

### ④ アドバイス
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

    with st.chat_message("assistant", avatar=kobito_avatar):

        col1, col2 = st.columns(2)

        if col1.button("🔍 もっと詳しく"):

            data = responses[st.session_state.show_detail_button]
            detail = data["detail"]

            detail_actions_text = "\n- ".join(detail["actions"])

            detail_answer = f"""## {data['title']}（もっと詳しく）

### 追加の結論
{detail['conclusion']}

### 追加の行動
- {detail_actions_text}

### 追加のアドバイス
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

# ==================================================
# 履歴削除
# ==================================================

if st.button("🗑️ チャット履歴を削除"):
    st.session_state.messages = []
    st.session_state.category = None
    st.session_state.welcome = False
    st.session_state.show_detail_button = None
    st.rerun()