import streamlit as st
from supabase import create_client

# Supabase 接続
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("SafeBox Manager - Family code")

# ログインチェック
if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

family_code = st.session_state["family_code"]

# 家族データ取得
response = supabase.table("family_profiles").select("*").eq("family_code", family_code).execute()
family_data = response.data[0] if response.data else {}

st.info(f"ログイン中：{family_code}")

# 編集モード管理
if "memo_edit" not in st.session_state:
    st.session_state.memo_edit = False

memo = family_data.get("memo")or ""

# 編集モード切り替え
if st.session_state.memo_edit:
    st.subheader("✏️ 編集モード")
    new_memo = st.text_area("共有メモ", value=memo, height=300)

    if st.button("💾 保存してロックする"):
        supabase.table("family_profiles").update({"memo": new_memo}).eq("family_code", family_code).execute()
        st.session_state.memo_edit = False
        st.success("メモを保存しました！")

else:
    st.subheader("📝 家族共有メモ（閲覧モード）")
    st.markdown("""
        <div style="background:#fafafa;padding:15px;border-radius:10px;border:1px solid #ddd;">
        {}
        </div>
        """.format(memo.replace("\n", "<br>")), unsafe_allow_html=True)

    if st.button("✏️ 編集する"):
        st.session_state.memo_edit = True
