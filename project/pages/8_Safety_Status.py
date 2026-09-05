import streamlit as st
import json
from supabase import create_client, Client

from kobito_helper import KOBITO_IMAGES, apply_page_theme, show_kobito_popup

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

family_code = st.session_state.get("family_code", None)

if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

apply_page_theme(
    "safety",
    "🛡️ 安否確認",
    f"ログイン中：{family_code}"
)

show_kobito_popup(
    KOBITO_IMAGES["safety"],
    "みんなの安否状況を確認しよう！",
    "kobito_safety_shown"
)

members = supabase.table("family_members").select("*").eq("family_code", family_code).execute()

if len(members.data) == 0:
    st.error("家族が登録されていません。\n最後のページ『設定』から家族を追加してください。")
    st.stop()

st.subheader("あなたの名前を選択してください")
name = st.selectbox("名前", [m["name"] for m in members.data])

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

if st.button("安否状況を送信"):
    data = {"status": status_key}

    supabase.table("safety_status").upsert({
        "family_code": family_code,
        "name": name,
        "data": json.dumps(data)
    }).execute()

    st.success("安否状況を送信しました")

st.markdown("---")

st.subheader("家族の安否状況")

status_rows = supabase.table("safety_status").select("*").eq("family_code", family_code).execute()

for row in status_rows.data:
    name = row["name"]
    status = json.loads(row["data"]).get("status", None)

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
