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
menu_item("🔑 家族コード", "pages/4_Family_Code.py")
menu_item("🛒 お店を探す", "pages/5_Shopping_Guide.py")
menu_item("📅 賞味・使用期限管理", "pages/6_Expiration_Date.py")
menu_item("🤖 AI相談", "pages/7_Chat_AI.py")
menu_item("🛡️ 安全確認", "pages/8_Safety_Status.py")
menu_item("❓ 防災クイズ", "pages/9_Quiz.py")
menu_item("📖 防災パンフレット", "pages/10_Disaster_Preparedness_Brochure.py")
menu_item("⚙️ 設定", "pages/11_settings.py")