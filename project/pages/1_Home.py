import streamlit as st

from kobito_helper import KOBITO_IMAGES, apply_page_theme, show_kobito_popup

# ログインチェック
if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

apply_page_theme(
    "home",
    "🏠 SafeBox Manager",
    f"ログイン中：{st.session_state['family_code']}"
)

show_kobito_popup(
    KOBITO_IMAGES["home"],
    "メニューから使いたい機能を選んでね！",
    "kobito_home_shown"
)

st.subheader("メニュー")

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