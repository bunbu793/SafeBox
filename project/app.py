import streamlit as st
from supabase import create_client
import requests
import base64
from datetime import date, timedelta


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
# 小人 & バースト吹き出し CSS
# ==========================================

st.markdown("""
<style>

@keyframes kobito-alert {
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

.kobito-alert-box {
    position: fixed;
    top: 260px;
    right: -250px;
    z-index: 9999;

    display: flex;
    flex-direction: column;
    align-items: center;

    animation: kobito-alert 6s ease-in-out forwards;
}


/* ==========================================
   バースト吹き出し
   ========================================== */

.burst-balloon {
    --burst-color: #ff66aa;

    position: relative;

    background: white;

    padding: 25px;

    width: 230px;

    text-align: center;

    font-weight: 700;

    border-radius: 50%;

    border: 4px solid #333;

    box-shadow: 0 0 0 10px var(--burst-color);
}

.burst-balloon:before {

    content: "";

    position: absolute;

    top: -18px;
    left: -18px;
    right: -18px;
    bottom: -18px;

    background: var(--burst-color);

    clip-path: polygon(
        50% 0%,
        60% 15%,
        80% 10%,
        75% 30%,
        95% 35%,
        80% 50%,
        100% 60%,
        75% 70%,
        85% 90%,
        60% 85%,
        50% 100%,
        40% 85%,
        15% 90%,
        25% 70%,
        0% 60%,
        20% 50%,
        5% 35%,
        25% 30%,
        20% 10%,
        40% 15%
    );

    z-index: -1;
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
# 説明
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
# 小人画像取得
# ==========================================

def get_base64_image_from_url(url):

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    return base64.b64encode(
        response.content
    ).decode()


KOBITO_URL = (
    "https://raw.githubusercontent.com/"
    "bunbu793/SafeBox/"
    "main/project/assets/kobito1.png"
)


# ==========================================
# 小人画像を読み込む
# ==========================================

try:

    kobito_intro = get_base64_image_from_url(
        KOBITO_URL
    )

except Exception as e:

    kobito_intro = None

    st.warning(
        "小人の画像を読み込めませんでした。"
    )


# ==========================================
# 小人の初回表示
# ==========================================

if "kobito_shown" not in st.session_state:

    st.session_state["kobito_shown"] = False


if (
    not st.session_state.kobito_shown
    and kobito_intro
):

    st.markdown("""
    <style>

    @keyframes kobito-move {

        0% {
            right: -200px;
            opacity: 0;
        }

        20% {
            right: 80px;
            opacity: 1;
        }

        70% {
            right: 80px;
            opacity: 1;
        }

        100% {
            right: -200px;
            opacity: 0;
        }

    }

    .kobito-box {

        position: fixed;

        top: 300px;

        right: -200px;

        z-index: 9999;

        display: flex;

        flex-direction: column;

        align-items: center;

        animation: kobito-move 6s ease-in-out forwards;
    }

    .kobito-balloon {

        background: #fff;

        border: 2px solid #333;

        padding: 10px;

        border-radius: 10px;

        margin-bottom: 10px;
    }

    </style>
    """, unsafe_allow_html=True)


    st.markdown(f"""
    <div class="kobito-box">

        <div class="kobito-balloon">

            こんにちは！<br>
            ぼくが案内するよ！

        </div>

        <img
            src="data:image/png;base64,{kobito_intro}"
            width="150"
        >

    </div>
    """, unsafe_allow_html=True)


    st.session_state.kobito_shown = True


# ==========================================
# ログインコードの初期化
# ==========================================

if "family_codes" not in st.session_state:

    st.session_state["family_codes"] = []


# ==========================================
# ログイン画面
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
# ログイン・新規登録
# ==========================================

if st.button("決定"):

    if input_code.strip() == "":

        st.error(
            "ログインコードを入力してください"
        )

    elif input_password.strip() == "":

        st.error(
            "パスワードを入力してください"
        )

    else:

        input_code = input_code.strip()


        # ----------------------------------
        # Supabaseから家族コードを検索
        # ----------------------------------

        exists = (
            supabase
            .table("families")
            .select("*")
            .eq(
                "family_code",
                input_code
            )
            .execute()
        )


        # ==================================
        # 既存ユーザー
        # ==================================

        if exists.data:

            saved_password = (
                exists.data[0].get("password")
            )


            if saved_password == input_password:

                st.success(
                    "ログインに成功しました"
                )


                st.session_state[
                    "family_code"
                ] = input_code


                # ログイン後の画面をすぐ更新
                st.rerun()


            else:

                st.error(
                    "パスワードが違います"
                )


        # ==================================
        # 新規登録
        # ==================================

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

                st.success(
                    f"ログインコード「{input_code}」を登録しました"
                )


                st.session_state[
                    "family_code"
                ] = input_code


                # 登録後すぐ画面更新
                st.rerun()


# ==========================================
# 現在のログインコード表示
# ==========================================

if "family_code" in st.session_state:

    st.info(
        "現在のログインコード："
        f"{st.session_state['family_code']}"
    )


# ==========================================
# ログイン後
# ==========================================

if "family_code" in st.session_state:


    # ======================================
    # 防災グッズ取得
    # ======================================

    response = (
        supabase
        .table("emergency_items")
        .select("*")
        .eq(
            "family_code",
            st.session_state["family_code"]
        )
        .execute()
    )


    items = response.data or []


    # ======================================
    # 期限チェック
    # ======================================

    expired_items = []

    soon_expiry_items = []


    today = date.today()


    for item in items:

        try:

            expiry = date.fromisoformat(
                item["expiry_date"]
            )


            days_left = (
                expiry - today
            ).days


            # ------------------------------
            # 期限切れ
            # ------------------------------

            if days_left < 0:

                expired_items.append(
                    item["name"]
                )


            # ------------------------------
            # 7日以内
            # ------------------------------

            elif days_left <= 7:

                soon_expiry_items.append(
                    item["name"]
                )


        except Exception:

            # 日付がない・形式が違う場合
            pass


    # ======================================
    # 小人メッセージ決定
    # ======================================


    # --------------------------------------
    # 防災グッズがない
    # --------------------------------------

    if not items:

        kobito_message = """
        まだ防災グッズがないよ！<br>
        登録してみよう！
        """

        kobito_color = "#64b5f6"


    # --------------------------------------
    # 期限切れ
    # --------------------------------------

    elif expired_items:

        names = "、".join(
            expired_items
        )

        kobito_message = f"""
        大変だよ！<br>
        {names}<br>
        期限切れの商品があるよ！
        """

        kobito_color = "#ff66aa"


    # --------------------------------------
    # 7日以内
    # --------------------------------------

    elif soon_expiry_items:

        names = "、".join(
            soon_expiry_items
        )

        kobito_message = f"""
        もうすぐ期限だよ！<br>
        {names}<br>
        早めに確認してね！
        """

        kobito_color = "#ff9800"


    # --------------------------------------
    # 問題なし
    # --------------------------------------

    else:

        kobito_message = """
        安全だよ！<br>
        今のところ大丈夫！
        """

        kobito_color = "#43a047"


    # ======================================
    # 小人＋バースト吹き出し
    # ======================================

    if kobito_intro:

        st.markdown(
            f"""
            <div class="kobito-alert-box">

                <div
                    class="burst-balloon"
                    style="--burst-color:{kobito_color};"
                >

                    {kobito_message}

                </div>


                <img
                    src="data:image/png;base64,{kobito_intro}"
                    width="150"
                >

            </div>
            """,
            unsafe_allow_html=True
        )