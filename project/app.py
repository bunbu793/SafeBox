import streamlit as st
from supabase import create_client
import requests
import base64
from datetime import date

# =========================================================
# ページ設定
# =========================================================

st.set_page_config(
    page_title="SafeBox Manager",
    page_icon="🧰",
    layout="centered"
)

# =========================================================
# Supabase 接続
# =========================================================

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =========================================================
# タイトル
# =========================================================

st.markdown(
    """
    <h1 translate="no">SafeBox Manager</h1>
    <h2>防災サポートアプリ</h2>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 説明
# =========================================================

st.write(
    """
    ようこそ、SafeBox Manager へ。

    このアプリでは、

    - 備品管理
    - 賞味期限・消費期限チェック
    - 災害情報
    - 避難所マップ
    - 家族連絡カード

    など、災害時に役立つ機能をまとめて利用できます。
    """
)

# =========================================================
# 小人表示フラグ
# =========================================================

if "kobito_shown" not in st.session_state:
    st.session_state["kobito_shown"] = False

# =========================================================
# 小人画像取得
# =========================================================

def get_base64_image_from_url(url):

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    return base64.b64encode(
        response.content
    ).decode()


# =========================================================
# 小人コメントを決定
# =========================================================

def get_kobito_message():

    # まだログインしていない
    if "family_code" not in st.session_state:

        return (
            "こんにちは！<br>"
            "ぼくが案内するよ！"
        )

    family_code = st.session_state["family_code"]

    try:

        # ---------------------------------------------
        # Supabaseから期限データ取得
        # ---------------------------------------------

        response = (
            supabase
            .table("emergency_items")
            .select(
                "name, expiry_type, expiry_date"
            )
            .eq(
                "family_code",
                family_code
            )
            .execute()
        )

        items = response.data or []

        today = date.today()

        expired_items = []
        warning_items = []

        # ---------------------------------------------
        # 期限判定
        # ---------------------------------------------

        for item in items:

            try:

                expiry = date.fromisoformat(
                    item["expiry_date"]
                )

            except Exception:

                continue

            days_left = (
                expiry - today
            ).days

            # 期限切れ
            if days_left < 0:

                expired_items.append(item)

            # 30日以内
            elif days_left <= 30:

                warning_items.append(item)

        # ---------------------------------------------
        # コメント
        # ---------------------------------------------

        if expired_items:

            return (
                "たいへん！<br>"
                f"期限切れが {len(expired_items)} 件あるよ！<br>"
                "確認して交換してね！"
            )

        elif warning_items:

            return (
                "そろそろ確認してね！<br>"
                f"期限が近いものが {len(warning_items)} 件あるよ！"
            )

        else:

            return (
                "ばっちり！<br>"
                "防災グッズは安全な状態だよ！"
            )

    except Exception:

        # Supabaseの読み込みに失敗した場合
        return (
            "こんにちは！<br>"
            "ぼくが案内するよ！"
        )


# =========================================================
# 小人を1回表示
# =========================================================

if not st.session_state["kobito_shown"]:

    try:

        # ---------------------------------------------
        # 小人画像
        # ---------------------------------------------

        kobito_image = get_base64_image_from_url(
            "https://raw.githubusercontent.com/"
            "bunbu793/SafeBox/main/project/assets/kobito1.png"
        )

        # ---------------------------------------------
        # コメント
        # ---------------------------------------------

        kobito_message = get_kobito_message()

        # ---------------------------------------------
        # CSS
        # ---------------------------------------------

        st.markdown(
            """
            <style>

            @keyframes kobito-move {

                0% {
                    right: -220px;
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
                    right: -220px;
                    opacity: 0;
                }
            }

            .kobito-box {

                position: fixed;

                top: 300px;

                right: -220px;

                z-index: 9999;

                display: flex;

                flex-direction: column;

                align-items: center;

                animation:
                    kobito-move
                    6s
                    ease-in-out
                    forwards;
            }

            .kobito-balloon {

                background: white;

                border: 2px solid #333;

                padding: 10px 15px;

                border-radius: 10px;

                margin-bottom: 10px;

                font-size: 16px;

                font-weight: 600;

                line-height: 1.5;

                text-align: center;

                box-shadow:
                    0 3px 10px rgba(0,0,0,0.15);

                white-space: nowrap;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        # ---------------------------------------------
        # 小人表示
        # ---------------------------------------------

        st.markdown(
            f"""
            <div class="kobito-box">

                <div class="kobito-balloon">
                    {kobito_message}
                </div>

                <img
                    src="data:image/png;base64,{kobito_image}"
                    width="150"
                >

            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------------------------------------
        # 一度だけ表示
        # ---------------------------------------------

        st.session_state["kobito_shown"] = True

    except Exception:

        # 画像取得などに失敗してもアプリは動かす
        st.session_state["kobito_shown"] = True


# =========================================================
# ログインコード
# =========================================================

if "family_codes" not in st.session_state:
    st.session_state["family_codes"] = []

st.subheader("ログインコードを入力してください")

input_code = st.text_input(
    "ログインコード"
)

input_password = st.text_input(
    "パスワード",
    type="password"
)

# =========================================================
# ログイン・新規登録
# =========================================================

if st.button("決定"):

    # ---------------------------------------------
    # 入力チェック
    # ---------------------------------------------

    if input_code.strip() == "":

        st.error(
            "ログインコードを入力してください"
        )

    elif input_password.strip() == "":

        st.error(
            "パスワードを入力してください"
        )

    else:

        try:

            # -----------------------------------------
            # 既存の家族コードを確認
            # -----------------------------------------

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

            # =========================================
            # 既存ユーザー
            # =========================================

            if exists.data:

                saved_password = (
                    exists.data[0].get("password")
                )

                if saved_password == input_password:

                    # ログイン成功
                    st.session_state["family_code"] = input_code

                    # ログイン後に小人をもう一度表示
                    st.session_state["kobito_shown"] = False

                    st.success(
                        "ログインに成功しました"
                    )

                    # 画面を再読み込み
                    st.rerun()

                else:

                    st.error(
                        "パスワードが違います"
                    )

            # =========================================
            # 新規登録
            # =========================================

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

                if response.data:

                    st.session_state["family_code"] = input_code

                    # 新規登録後も小人を表示
                    st.session_state["kobito_shown"] = False

                    st.success(
                        f"ログインコード「{input_code}」を登録しました"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Supabaseへの保存に失敗しました"
                    )

        except Exception as e:

            st.error(
                f"ログイン処理に失敗しました：{e}"
            )


# =========================================================
# 現在のログインコード
# =========================================================

if "family_code" in st.session_state:

    st.info(
        f"現在のログインコード："
        f"{st.session_state['family_code']}"
    )