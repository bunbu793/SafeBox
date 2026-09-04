import streamlit as st
from supabase import create_client
import requests
import base64
import json
import os

st.set_page_config(
    page_title="SafeBox Manager",
    page_icon="🧰",
    layout="centered"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

#タイトル
st.markdown("""
<h1 translate="no">SafeBox Manager</h1>
<h2>防災サポートアプリ</h2>
""", unsafe_allow_html=True)

#説明文
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

#小人を表示
# フラグがなければ初期化
if "kobito_shown" not in st.session_state:
    st.session_state["kobito_shown"] = False

# 小人を一度だけ表示
if not st.session_state.kobito_shown:

    def get_base64_image_from_url(url):
        response = requests.get(url)
        return base64.b64encode(response.content).decode()

    kobito_intro = get_base64_image_from_url(
            "https://raw.githubusercontent.com/bunbu793/SafeBox/main/project/assets/kobito1.png"
            )

    # CSS（アニメーション）
    st.markdown("""
    <style>
    @keyframes kobito-move {
        0%   { right: -200px; opacity: 0; }
        20%  { right: 80px; opacity: 1; }
        70%  { right: 80px; opacity: 1; }
        100% { right: -200px; opacity: 0; }
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
        background:#fff;
        border:2px solid #333;
        padding:10px;
        border-radius:10px;
        margin-bottom:10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 小人表示
    st.markdown(f"""
    <div class="kobito-box">
        <div class="kobito-balloon">
            こんにちは！<br>ぼくが案内するよ！
        </div>
        <img src="data:image/png;base64,{kobito_intro}" width="150">
    </div>
    """, unsafe_allow_html=True)

    # フラグを立てる（次回以降は表示しない）
    st.session_state.kobito_shown = True

#ログインコードの初期化＋新規作成＋読み込み
if "family_codes" not in st.session_state:
    st.session_state["family_codes"] = []

st.subheader("ログインコードを入力してください")

input_code = st.text_input("ログインコード")
input_password = st.text_input("パスワード" ,type = "password")

if st.button("決定"):
    if input_code.strip() == "":
        st.error("ログインコードを入力してください")
    elif input_password.strip() == "":
        st.error("パスワードを入力してください")
    else:
        exists = supabase.table("families").select("*").eq("family_code", input_code).execute()

        if exists.data:
            # 既存 → パスワードチェック
            saved_password = exists.data[0].get("password")

            if saved_password == input_password:
                st.success("ログインに成功しました")
                st.session_state["family_code"] = input_code
            else:
                st.error("パスワードが違います")
        else:
            # 新規登録（コード＋パスワードを保存）
            data = {
                "family_code": input_code,
                "password": input_password
            }
            response = supabase.table("families").insert(data).execute()

            if response.data is None:
                st.error("Supabase への保存に失敗しました")
            else:
                st.success(f"ログインコード「{input_code}」を登録しました")
                st.session_state["family_code"] = input_code

# 現在のログインコード表示
if "family_code" in st.session_state:
    st.info(f"現在のログインコード：{st.session_state['family_code']}")

# =========================================================
# 期限状況による小人コメント
# =========================================================

from datetime import date

if "family_code" in st.session_state:

    family_code = st.session_state["family_code"]

    try:
        # 防災グッズの期限データを取得
        response = (
            supabase
            .table("emergency_items")
            .select("name, expiry_type, expiry_date")
            .eq("family_code", family_code)
            .execute()
        )

        items = response.data or []

        # 状態ごとの件数
        expired_items = []
        warning_items = []
        safe_items = []

        today = date.today()

        for item in items:

            try:
                expiry = date.fromisoformat(
                    item["expiry_date"]
                )

            except Exception:
                continue

            days_left = (expiry - today).days

            if days_left < 0:
                expired_items.append(item)

            elif days_left <= 30:
                warning_items.append(item)

            else:
                safe_items.append(item)

        # -------------------------------------------------
        # 小人のコメントを決定
        # -------------------------------------------------

        if expired_items:

            kobito_message = (
                "たいへん！\n\n"
                f"期限が切れているものが "
                f"{len(expired_items)}件 あるよ。\n"
                "期限管理ページで確認してね！"
            )

            comment_type = "danger"

        elif warning_items:

            kobito_message = (
                "そろそろ確認してね！\n\n"
                f"期限が近いものが "
                f"{len(warning_items)}件 あるよ。\n"
                "早めに交換しておくと安心だよ！"
            )

            comment_type = "warning"

        else:

            kobito_message = (
                "ばっちり！\n\n"
                "今のところ期限に問題はないよ。\n"
                "この状態をキープしよう！"
            )

            comment_type = "safe"

        # -------------------------------------------------
        # 小人表示
        # -------------------------------------------------

        st.divider()
        st.subheader("🧙 小人からのお知らせ")

        col1, col2 = st.columns(
            [1, 2],
            vertical_alignment="center"
        )

        with col1:

            try:
                st.image(
                    "project/assets/kobito_transparent.png",
                    width=160
                )

            except Exception:
                st.write("🧙")

        with col2:

            if comment_type == "danger":

                st.error(kobito_message)

            elif comment_type == "warning":

                st.warning(kobito_message)

            else:

                st.success(kobito_message)

    except Exception as e:

        st.warning(
            "期限情報を確認できませんでした。"
        )
