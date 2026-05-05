import streamlit as st
from supabase import create_client

# Supabase 接続
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("SafeBox Manager - Family composition")

# -------------------------
# ログインチェック
# -------------------------
if "family_code" not in st.session_state:
    st.warning("初めにログインをしてください")
    st.stop()

family_code = st.session_state["family_code"]
st.success(f"ログイン中: {family_code}")

# -------------------------
# 編集モード管理
# -------------------------
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# -------------------------
# Supabase から家族データ読み込み
# -------------------------
response = supabase.table("family_profiles").select("*").eq("family_code", family_code).execute()

if response.data:
    family_data = response.data[0]
else:
    family_data = {"members": 1, "names": [], "notes": ""}

# -------------------------
# 編集モード切り替えボタン

st.subheader("家族構成")

if st.session_state.edit_mode:
    st.info("編集モードです")
    if st.button("保存してロックする"):
        st.session_state.edit_mode = False
else:
    st.info("閲覧モード（変更できません）")
    if st.button("変更する"):
        st.session_state.edit_mode = True

disabled_flag = not st.session_state.edit_mode

# -------------------------
# 家族人数入力
# -------------------------
members = st.number_input(
    "家族人数",
    min_value=1,
    max_value=100,
    value=family_data.get("members", 1),
    disabled=disabled_flag
)

# 名前入力欄

st.subheader("家族全員の名前")

name_inputs = []
existing_names = family_data.get("names", [])

for i in range(members):
    default_name = existing_names[i] if i < len(existing_names) else ""
    name_input = st.text_input(
        f"{i+1}人目の名前",
        value=default_name,
        disabled=disabled_flag
    )
    name_inputs.append(name_input)

# 備考欄

notes = st.text_area(
    "備考",
    value=family_data.get("notes", ""),
    disabled=disabled_flag
)

# 保存処理
if st.session_state.edit_mode:
    if st.button("保存"):
        data = {
            "family_code": family_code,
            "members": members,
            "names": name_inputs,
            "notes": notes
        }

        supabase.table("family_profiles").upsert(data).execute()
        st.session_state["family_data"] = data

        st.success("家族構成を保存しました！")
