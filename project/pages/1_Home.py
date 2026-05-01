import streamlit as st

st.title("SafeBox Manager - Home")

# ログインチェック
if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

st.success(f"ログイン中：{st.session_state['family_code']}")

st.subheader("メニュー")

# --- デザインCSS ---
st.markdown("""
<style>
.menu-btn {
    width: 100%;
    padding: 15px;
    border-radius: 10px;
    border: 2px solid #ddd;
    margin-bottom: 15px;
    background: #fafafa;
    font-size: 20px;
    text-align: left;
    transition: 0.2s;
}
.menu-btn:hover {
    background: #f0f0f0;
    border-color: #999;
}
</style>
""", unsafe_allow_html=True)

# --- ボタンでページ移動（これが一番確実に動く） ---
def menu_item(title, page_path):
    if st.button(title, key=page_path, use_container_width=True):
        st.switch_page(page_path)

menu_item("👨‍👩‍👧 家族構成登録・確認", "pages/2_family.py")
menu_item("📋 チェックリスト・アドバイス", "pages/3_Checklist_Advice.py")
menu_item("🔑 ログインコード管理", "pages/4_Family_Code.py")
menu_item("💬 チャット", "pages/5_Chat.py")
menu_item("🆘 安否確認", "pages/6_safety_Status.py")
menu_item("🗺️ 避難所マップ", "pages/7_Shelters_Map.py")
menu_item("❓ 防災クイズ", "pages/8_Quiz.py")

# ログアウト
if st.button("ログアウト"):
    st.session_state.clear()
    st.success("ログアウトしました")
