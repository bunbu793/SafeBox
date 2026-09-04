import streamlit as st
from supabase import create_client
import requests
import base64

# ==========================================
# ページ設定
# ==========================================

st.set_page_config(
    page_title="SafeBox Manager",
    page_icon="🧰",
    layout="centered"
)

# ==========================================
# Supabase
# ==========================================

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ==========================================
# 小人画像
# ==========================================

def get_base64_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode()


KOBITO_URL = (
    "https://raw.githubusercontent.com/bunbu793/"
    "SafeBox/main/project/assets/kobito1.png"
)

try:
    kobito_intro = get_base64_image_from_url(KOBITO_URL)
except Exception:
    kobito_intro = None


# ==========================================
# セッション状態
# ==========================================

if "kobito_shown" not in st.session_state:
    st.session_state["kobito_shown"] = False

if "welcome_back" not in st.session_state:
    st.session_state["welcome_back"] = False

if "family_code" not in st.session_state:
    st.session_state["family_code"] = None


# ==========================================
# 小人CSS
# ==========================================

st.markdown("""
<style>

/* ==========================================
   こんにちは小人
   ========================================== */

@keyframes kobito-move {

    0% {
        right: -250px;
        opacity: 0;
    }

    20% {
        right: 40px;
        opacity: 1;
    }

    80% {
        right: 40px;
        opacity: 1;
    }

    100% {
        right: -250px;
        opacity: 0;
    }
}

.kobito-box {

    position: fixed;

    top: 300px;
    right: -250px;

    z-index: 9999;

    display: flex;
    flex-direction: column;
    align-items: center;

    animation: kobito-move 6s ease-in-out forwards;
}


/* ==========================================
   おかえり小人
   ========================================== */

@keyframes kobito-welcome {

    0% {
        right: -250px;
        opacity: 0;
    }

    20% {
        right: 40px;
        opacity: 1;
    }

    80% {
        right: 40px;
        opacity: 1;
    }

    100% {
        right: -250px;
        opacity: 0;
    }
}

.kobito-welcome-box {

    position: fixed;

    top: 300px;
    right: -250px;

    z-index: 9999;

    display: flex;
    flex-direction: column;
    align-items: center;

    animation: kobito-welcome 6s ease-in-out forwards;
}


/* ==========================================
   小人の吹き出し
   ========================================== */

.kobito-balloon,
.kobito-welcome-balloon {

    background: white;

    border: 2px solid #333;

    padding: 10px 18px;

    border-radius: 10px;

    margin-bottom: 10px;

    font-weight: bold;

    text-align: center;

    white-space: nowrap;
}


/* ==========================================
   小人画像
   ========================================== */

.kobito-box img,
.kobito-welcome-box img {

    display: block;

    width: 150px;

    height: auto;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# タイトル
# ==========================================

st.markdown("""
<h1 translate="no">SafeBox Manager</h1>

<h2>防災サポートアプリ</h2>
""", unsafe_allow_html=True)


# ==========================================
# 説明文
# ==========================================

st.write("""
ようこそ、SafeBox Manager へ。

このアプリでは、

- 備品管理
- 賞味期限チェック
- 災害情報
- 避難所マップ
- 家族連絡カード

など、災害時に役立つ機能をまとめて利用できます。
""")


# ==========================================
# こんにちは小人
# ==========================================

if not st.session_state["kobito_shown"]:

    if kobito_intro:

        st.markdown(
            f"""
            <div class="kobito-box">

                <div class="kobito-balloon">
                    こんにちは！<br>
                    ぼくが案内するよ！
                </div>

                <img
                    src="data:image/png;base64,{kobito_intro}"
                    alt="小人"
                >

            </div>
            """,
            unsafe_allow_html=True
        )

    st.session_state["kobito_shown"] = True


# ==========================================
# ログイン
# ==========================================

st.subheader("ログインコードを入力してください")

input_code = st.text_input(
    "ログインコード"
)

input_password = st.text_input(
    "パスワード",
    type="password"
)


# ==========================================
# 決定
# ==========================================

if st.button("決定"):

    # --------------------------------------
    # 入力チェック
    # --------------------------------------

    if input_code.strip() == "":

        st.error("ログインコードを入力してください")

    elif input_password.strip() == "":

        st.error("パスワードを入力してください")

    else:

        # --------------------------------------
        # Supabaseから家族コードを検索
        # --------------------------------------

        exists = (
            supabase
            .table("families")
            .select("*")
            .eq("family_code", input_code)
            .execute()
        )

        # ======================================
        # 既存の家族コード
        # ======================================

        if exists.data:

            saved_password = exists.data[0].get("password")

            # ----------------------------------
            # パスワード正解
            # ----------------------------------

            if saved_password == input_password:

                st.session_state["family_code"] = input_code

                # おかえり小人を表示
                st.session_state["welcome_back"] = True

                st.success("ログインに成功しました")

                # 画面を再読み込み
                st.rerun()

            # ----------------------------------
            # パスワード不正解
            # ----------------------------------

            else:

                st.error("パスワードが違います")


        # ======================================
        # 新規登録
        # ======================================

        else:

            data = {
                "family_code": input_code,
                "password": input_password
            }

            response = (
                supabase
                .table("families")
                .insert(data)
                .execute()
            )

            if response.data is None:

                st.error(
                    "Supabase への保存に失敗しました"
                )

            else:

                st.session_state["family_code"] = input_code

                # 新規登録でもおかえりを表示
                st.session_state["welcome_back"] = True

                st.success(
                    f"ログインコード「{input_code}」を登録しました"
                )

                # 画面を再読み込み
                st.rerun()


# ==========================================
# おかえり小人
# ==========================================

if st.session_state["welcome_back"]:

    if kobito_intro:

        st.markdown(
            f"""
            <div class="kobito-welcome-box">

                <div class="kobito-welcome-balloon">
                    おかえり！<br>
                    今日もよろしくね！
                </div>

                <img
                    src="data:image/png;base64,{kobito_intro}"
                    alt="小人"
                >

            </div>
            """,
            unsafe_allow_html=True
        )

    # 一度だけ表示
    st.session_state["welcome_back"] = False


# ==========================================
# 現在のログインコード
# ==========================================

if st.session_state.get("family_code"):

    st.info(
        f"現在のログインコード："
        f"{st.session_state['family_code']}"
    )