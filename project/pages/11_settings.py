import streamlit as st
from supabase import create_client

from kobito_helper import KOBITO_IMAGES, apply_page_theme, show_kobito_popup

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

family_code = st.session_state["family_code"]

apply_page_theme(
    "settings",
    "⚙️ 設定",
    f"ログイン中：{family_code}"
)

show_kobito_popup(
    KOBITO_IMAGES["settings"],
    "家族の追加や削除はここでできるよ！",
    "kobito_settings_shown"
)

st.subheader("家族の名前を追加")

new_name = st.text_input("追加する家族の名前（例:太郎、花子）")

color = st.selectbox("カラータグを選択", ["blue", "green", "red", "yellow", "pink", "purple"])

if st.button("家族を追加"):
    if new_name.strip() == "":
        st.error("名前を入力してください")
    else:
        supabase.table("family_members").insert({
            "family_code": family_code,
            "name": new_name,
            "color": color
        }).execute()

        st.success(f"家族に「{new_name}」を追加しました（色: {color}）")

st.subheader("登録済みの家族")

members = supabase.table("family_members").select("*").eq("family_code", family_code).execute()

st.markdown("""
<style>
.red-trash-btn {
    background-color: #ff4d4d !important;
    color: white !important;
    border: none !important;
    padding: 6px 10px !important;
    border-radius: 6px !important;
    cursor: pointer !important;
    font-size: 18px !important;
    box-shadow: 0px 2px 3px rgba(0,0,0,0.3) !important;
}
.red-trash-btn:hover {
    background-color: #ff1a1a !important;
}
</style>
""", unsafe_allow_html=True)

if members.data:
    for m in members.data:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center;">
                    <div style="
                        width:14px; height:14px;
                        background:{m.get('color', 'blue')};
                        border-radius:50%;
                        margin-right:8px;
                    "></div>
                    <span>- {m['name']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            btn = st.button("🗑️", key=f"delete_{m['id']}")

            st.markdown(
                f"""
                <script>
                const btns = window.parent.document.querySelectorAll('button[data-testid="baseButton-delete_{m["id"]}"]');
                btns.forEach(btn => btn.classList.add('red-trash-btn'));
                </script>
                """,
                unsafe_allow_html=True
            )

            if btn:
                supabase.table("family_members").delete().eq("id", m["id"]).execute()
                st.success(f"{m['name']} を削除しました")
                st.rerun()
else:
    st.info("まだ家族が登録されていません")
