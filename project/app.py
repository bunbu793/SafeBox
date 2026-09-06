import streamlit as st
from supabase import create_client
from datetime import date
import json
import os

from kobito_helper import (
    KOBITO_IMAGES,
    apply_page_theme,
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

apply_page_theme(
    "login",
    "🧰 SafeBox Manager",
    "防災サポートアプリへようこそ"
)

#説明文
st.write("""
このアプリでは、

- 備品管理  
- 賞味期限チェック  
- 災害情報  
- 避難所マップ  
- 家族連絡カード  

など、災害時に役立つ機能をまとめて利用できます。
""")

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
# 小人メッセージを決定して、最後に1回だけ表示する
# =========================================================

if "family_code" in st.session_state:

    # ログイン済み（再訪問時も含めて毎回、在庫状況に応じたメッセージ）
    status = get_family_status(st.session_state["family_code"])

    if status == "danger":
        kobito_message = "おかえりなさい！<br>大変です、防災グッズに期限切れのものがあります！"
    elif status == "warning":
        kobito_message = "おかえりなさい！<br>防災グッズにもうすぐ期限のものがあります、注意して！"
    elif status == "safe":
        kobito_message = "おかえりなさい！<br>防災グッズは今は安心だね！"
    else:
        kobito_message = "おかえりなさい！<br>まずは防災グッズを登録してみよう！"

else:

    # 未ログイン（毎回「こんにちは」）
    kobito_message = "こんにちは！<br>ぼくが案内するよ！"

show_kobito_popup(
    KOBITO_IMAGES["login"],
    kobito_message,
    "kobito_login"
)