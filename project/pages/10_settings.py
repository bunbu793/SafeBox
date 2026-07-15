import streamlit as st
from supabase import create_client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import secrets

# Supabase 接続
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("SafeBox Manager - Settings")

st.write("ここでは、家族コードやパスワードの変更、家族の名前登録が可能です。")

# ---------------------------
# パスワード再発行（user_id 方式）
# ---------------------------

def generate_reset_token():
    return secrets.token_urlsafe(32)

def save_reset_token(user_id, token):
    supabase.table("profiles").update({
        "reset_token": token
    }).eq("user_id", user_id).execute()

def send_reset_email(to_email, reset_link):
    message = Mail(
        from_email=st.secrets["FROM_EMAIL"],
        to_emails=to_email,
        subject="【SafeBox Manager】パスワード再設定リンク",
        html_content=f"""
        <p>パスワード再設定をご希望ですか？</p>
        <p>以下のリンクから新しいパスワードを設定できます：</p>
        <a href="{reset_link}">{reset_link}</a>
        <p>このメールに心当たりがない場合は無視してください。</p>
        """
    )

    try:
        sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
        sg.send(message)
        return True
    except Exception as e:
        print(e)
        return False

st.subheader("パスワード再発行")

user_id_input = st.text_input("個人コード（user_id）を入力してください")

if st.button("再発行メールを送る"):
    if user_id_input.strip() == "":
        st.error("個人コードを入力してください")
    else:
        token = generate_reset_token()

        # 本来は token を含む URL を作る
        reset_link = f"https://your-app-url/reset?token={token}"

        # Supabase に保存
        save_reset_token(user_id_input, token)

        # メール送信（メールアドレスは user_id と同じにしている場合のみ）
        success = send_reset_email(user_id_input, reset_link)

        if success:
            st.success("再発行メールを送信しました")
        else:
            st.error("メール送信に失敗しました")

# ---------------------------
# 家族の名前登録
# ---------------------------

st.subheader("家族の名前を追加")

if "family_code" not in st.session_state:
    st.warning("ログインしてください")
    st.stop()

family_code = st.session_state["family_code"]

new_name = st.text_input("追加する家族の名前（例：侃、母、父、兄、姉）")

if st.button("家族を追加"):
    if new_name.strip() == "":
        st.error("名前を入力してください")
    else:
        supabase.table("family_members").insert({
            "family_code": family_code,
            "name": new_name
        }).execute()

        st.success(f"家族に「{new_name}」を追加しました")

# 家族一覧表示 & 削除機能
st.subheader("登録済みの家族")

members = supabase.table("family_members").select("*").eq("family_code", family_code).execute()

# CSS（赤い2Dゴミ箱ボタン）
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
            st.write(f"- {m['name']}")

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
