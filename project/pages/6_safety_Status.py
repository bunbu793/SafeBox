import streamlit as st
import json
from supabase import create_client

st.title("SafeBox Manager - 安否確認")

# Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ログインチェック
if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

family_code = st.session_state["family_code"]
st.success(f"ログイン中：{family_code}")

# 家族一覧を取得
members = supabase.table("family_members").select("*").eq("family_code", family_code).execute()

if not members.data:
    st.error("家族の名前が登録されていません。設定ページで追加してください。")
    st.stop()

member_names = [m["name"] for m in members.data]

# 名前選択
st.subheader("あなたの名前を選択してください")
name = st.selectbox("名前", member_names)

# 絵文字付きステータス
status_options = {
    "safe": {"label": "🟢 安全", "emoji": "🟢"},
    "danger": {"label": "🔴 危険", "emoji": "🔴"},
    "need_help": {"label": "🟡 要支援", "emoji": "🟡"}
}

st.subheader("あなたの安否状況を選択してください")

selected_label = st.radio(
    "安否状況",
    [v["label"] for v in status_options.values()]
)

# 選択されたキーを取得
selected_key = None
for key, v in status_options.items():
    if v["label"] == selected_label:
        selected_key = key
        break

# 保存
if st.button("安否状況を送信"):
    data = {
        "name": name,
        "status": status_options[selected_key]["label"],
        "emoji": status_options[selected_key]["emoji"]
    }

    supabase.table("safety_status").upsert({
        "family_code": family_code,
        "name": name,
        "data": json.dumps(data)
    }).execute()

    st.success(f"{data['emoji']} {name}：{data['status']} を送信しました")

# 家族の状況一覧
st.subheader("家族の安否状況一覧")

response = supabase.table("safety_status").select("*").eq("family_code", family_code).execute()

if response.data:
    for row in response.data:
        d = json.loads(row["data"])

        # カードデザイン
        st.markdown(
            f"""
            <div style="
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 12px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
            ">
                <h3 style="margin: 0;">{d['emoji']} {d['name']}</h3>
                <p style="margin: 5px 0 0; font-size: 18px;">{d['status']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("まだ安否状況が登録されていません")
