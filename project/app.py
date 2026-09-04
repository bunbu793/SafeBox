import streamlit as st
from supabase import create_client
from datetime import date
import json
import os

from kobito_helper import (
    KOBITO_IMAGE_URL,
    inject_kobito_css,
    show_kobito_popup
)

st.set_page_config(
    page_title="SafeBox Manager",
    page_icon="🧰",
    layout="centered"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# 小人 & バースト吹き出し CSS
inject_kobito_css()

st.markdown("""
<style>

@keyframes kobito-alert {
    0%   { right: -250px; opacity: 0; }
    20%  { right: 40px; opacity: 1; }
    80%  { right: 40px; opacity: 1; }
    100% { right: -250px; opacity: 0; }
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

/* バースト吹き出し */
.burst-balloon {
    --burst-color: #ff66aa; /* ←色変更できる */
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
        50% 0%, 60% 15%, 80% 10%, 75% 30%,
        95% 35%, 80% 50%, 100% 60%, 75% 70%,
        85% 90%, 60% 85%, 50% 100%, 40% 85%,
        15% 90%, 25% 70%, 0% 60%, 20% 50%,
        5% 35%, 25% 30%, 20% 10%, 40% 15%
    );
    z-index: -1;
}

</style>
""", unsafe_allow_html=True)

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

# ページ読み込み時の「こんにちは」（1回だけ）
show_kobito_popup(
    KOBITO_IMAGE_URL,
    "こんにちは！<br>ぼくが案内するよ！",
    "kobito_shown"
)

# =========================================================
# 家族の防災グッズ状態を確認する関数
# =========================================================

def get_family_status(family_code):
    """家族の防災グッズの状態を確認して、danger/warning/safe/empty/unknownを判定する"""

    try:
        response = (
            supabase
            .table("emergency_items")
            .select("expiry_date")
            .eq("family_code", family_code)
            .execute()
        )
        items = response.data or []
    except Exception:
        return "unknown"

    if not items:
        return "empty"

    today = date.today()
    has_danger = False
    has_warning = False

    for item in items:
        try:
            expiry = date.fromisoformat(item["expiry_date"])
            days_left = (expiry - today).days

            if days_left < 0:
                has_danger = True
            elif days_left <= 30:
                has_warning = True
        except Exception:
            continue

    if has_danger:
        return "danger"
    elif has_warning:
        return "warning"
    else:
        return "safe"


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

                # 在庫状態に応じて「おかえりなさい」メッセージを変える
                status = get_family_status(input_code)

                if status == "danger":
                    welcome_message = "おかえりなさい！<br>大変です、期限切れのものがあります！"
                elif status == "warning":
                    welcome_message = "おかえりなさい！<br>もうすぐ期限のものがあります、注意して！"
                elif status == "safe":
                    welcome_message = "おかえりなさい！<br>今は安心だね！"
                else:
                    welcome_message = "おかえりなさい！<br>まずは防災グッズを登録してみよう！"

                show_kobito_popup(
                    KOBITO_IMAGE_URL,
                    welcome_message,
                    "kobito_welcome_shown"
                )
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

                # 新規登録時の「ようこそ」
                show_kobito_popup(
                    KOBITO_IMAGE_URL,
                    "ようこそ！<br>登録ありがとう！",
                    "kobito_register_shown"
                )

# 現在のログインコード表示
if "family_code" in st.session_state:
    st.info(f"現在のログインコード：{st.session_state['family_code']}")