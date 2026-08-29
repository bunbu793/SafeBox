import streamlit as st
from supabase import create_client
import datetime

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("防災グッズの賞味期限管理")

# ログインチェック
if "family_code" not in st.session_state:
    st.warning("ログインしてください")
    st.stop()

family_code = st.session_state["family_code"]

# -------------------------
# 新規登録フォーム
# -------------------------

st.subheader("新しい期限を登録")

item_name = st.text_input("アイテム名（例：非常食、乾電池、飲料水など）")
expiration = st.date_input("賞味期限 / 使用期限")
memo = st.text_area("メモ（任意）")

if st.button("登録"):
    if item_name.strip() == "":
        st.error("アイテム名を入力してください")
        st.stop()
    exp_date = expiration.strftime("%Y-%m-%d")

    memo_value = memo.strip()
    if memo_value == "":
        memo_value = None

    data = {
        "family_code": family_code,
        "item_name": item_name,
        "expiration": exp_date,
        "memo": memo if memo.strip() != "" else None
    }

    st.write("送信データ:" , data)

    supabase.table("item_expiration").insert(data).execute()
    st.success(f"{item_name} の期限を登録しました")
# -------------------------
# 登録済みアイテム一覧
# -------------------------

st.subheader("登録済みアイテム一覧")

response = supabase.table("item_expiration").select("*").eq(
    "family_code", family_code
).order("expiration", desc=False).execute()

today = datetime.date.today()

if response.data:
    for item in response.data:
        exp = datetime.date.fromisoformat(item["expiration"])
        remaining = (exp - today).days

        # 状態判定
        if remaining < 0:
            status = f"⚠️ 期限切れ（{abs(remaining)}日前）"
            color = "red"
        elif remaining <= 30:
            status = f"⚠️ 期限が近い（あと{remaining}日）"
            color = "orange"
        else:
            status = f"残り {remaining}日"
            color = "green"

        st.markdown(f"""
### {item['item_name']}
- **期限**：{item['expiration']}
- **状態**：<span style="color:{color}; font-weight:bold;">{status}</span>
- **メモ**：{item['memo']}
""", unsafe_allow_html=True)

else:
    st.info("まだ登録されていません")
