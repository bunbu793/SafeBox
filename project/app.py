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