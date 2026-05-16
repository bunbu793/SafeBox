import streamlit as st
from supabase import create_client

# Supabase 接続
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)
st.title("SafeBox Manager - Settings")

st.title("SafeBoxManager - settings")

st.write("ここでは、家族コードやパスワードの変更が可能です。")

family_code = st.text_input("家族コード")
old_password = st.text_input("現在のパスワード", type="password")
new_password = st.text_input("新しいパスワード", type="password")

if st.button("パスワードを変更する"):
    if not family_code or not old_password or not new_password:
        st.warning("全ての項目を入力してください")
    else:
        response = supabase.table("family_profiles").select("*").eq("family_code", family_code).execute()
        if response.data:
            profile = response.data[0]
            if profile.get("password") == old_password:
                supabase.table("family_profiles").update({"password": new_password}).eq("family_code", family_code).execute()
                st.success("パスワードを変更しました！")
            else:
                st.error("現在のパスワードが違います")
        else:
            st.error("家族コードが見つかりません")