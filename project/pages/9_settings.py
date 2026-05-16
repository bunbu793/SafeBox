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

st.write("ここでは、家族コードやパスワードの変更が可能です。")

def generate_reset_token():
    return secrets.token_urlsafe(32)

def save_reset_token(email, token):
    supabase.table("profiles").update({
        "reset_token": token
    }).eq("email", email).execute()

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

email = st.text_input("登録メールアドレス")

if st.button("再発行メールを送る"):

    token = generate_reset_token()
    reset_link = "https://your-app-url/reset?token=dummy"
    save_reset_token(email, token)

    success = send_reset_email(email, reset_link)

    if success:
        st.success("再発行メールを送信しました")
    else:
        st.error("メール送信に失敗しました")