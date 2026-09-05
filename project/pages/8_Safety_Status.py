import streamlit as st
import json
from supabase import create_client, Client

from kobito_helper import KOBITO_IMAGES, inject_kobito_css, show_kobito_popup

# Supabase 初期化
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

inject_kobito_css()

st.title("SafeBox Manager - 安否確認")

# family_code の取得
family_code = st.session_state.get("family_code", None)

# ログインチェック
if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

st.info(f"ログイン中：{family_code}")

show_kobito_popup(
    KOBITO_IMAGES["safety"],
    "みんなの安否状況を確認しよう！",
    "kobito_safety_shown"
)

# 家族一覧取得
members = supabase.table("family_members").select("*").eq("family_code", family_code).execute()

# ★ 家族が登録されていない場合
if len(members.data) == 0:
    st.error("家族が登録されていません。\n最後のページ『設定』から家族を追加してください。")
    st.stop()

# 名前選択
st.subheader("あなたの名前を選択してください")
name = st.selectbox("名前", [m["name"] for m in members.data])

# 安否状況選択
st.subheader("あなたの安否状況を選択してください")

status_options = {
    "No damage": {"label": "🟩 被害なし", "emoji": "🟩"},
    "Damage": {"label": "🟥 被害あり", "emoji": "🟥"},
}

status_key = st.selectbox(
    "安否状況",
    list(status_options.keys()),
    format_func=lambda x: status_options[x]["label"]
)

# 保存ボタン
if st.button("安否状況を送信"):
    data = {"status": status_key}

    supabase.table("safety_status").upsert({
        "family_code": family_code,
        "name": name,
        "data": json.dumps(data)
    }).execute()

    st.success("安否状況を送信しました")

st.markdown("---")

# 全員の安否状況表示
st.subheader("家族の安否状況")

status_rows = supabase.table("safety_status").select("*").eq("family_code", family_code).execute()

for row in status_rows.data:
    name = row["name"]
    status = json.loads(row["data"]).get("status", None)

    # ★ 壊れたデータ（🟩 安全など）はスキップ
    if status not in status_options:
        st.warning(f"{name} の安否状況データが不足です (status={status})")
        continue

    icon = status_options[status]["emoji"]
    label = status_options[status]["label"].replace(icon, "")

    st.markdown(
        f"""
        <div style="
            padding: 14px;
            border-radius: 10px;
            background-color: #ffffff;
            margin-bottom: 12px;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.15);
        ">
            <div style="font-size: 22px; font-weight: bold;">{name}</div>
            <div style="font-size: 20px; margin-top: 6px;">{icon}{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )