import streamlit as st
from supabase import create_client
from datetime import date

# -------------------------
# Supabase
# -------------------------

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# -------------------------
# ページ設定
# -------------------------

st.set_page_config(
    page_title="防災グッズ管理",
    page_icon="🧰",
    layout="centered"
)

st.title("🧰 防災グッズ管理")
st.write("非常食・保存水・防災用品などの期限をまとめて管理できます。")

# -------------------------
# ログイン確認
# -------------------------

if "family_code" not in st.session_state:
    st.warning("先にメインページでログインしてください。")
    st.stop()

family_code = st.session_state["family_code"]

# -------------------------
# 期限の状態を判定
# -------------------------

def get_status(expiry_date):
    today = date.today()
    days_left = (expiry_date - today).days

    if days_left < 0:
        return "🔴", "期限切れ", days_left

    elif days_left <= 30:
        return "🟡", "期限間近", days_left

    else:
        return "🟢", "安全", days_left


# -------------------------
# 新規登録
# -------------------------

st.subheader("➕ 防災グッズを登録")

with st.form("add_item"):

    name = st.text_input(
        "商品名",
        placeholder="例：保存水、アルファ米、乾電池"
    )

    category = st.selectbox(
        "カテゴリ",
        [
            "非常食",
            "飲料水",
            "電池",
            "医療・救急",
            "衛生用品",
            "照明・通信",
            "防災用品",
            "その他"
        ]
    )

    expiry_type = st.selectbox(
        "期限の種類",
        [
            "賞味期限",
            "使用期限",
            "使用推奨期限",
            "点検日"
        ]
    )

    expiry_date = st.date_input(
        "期限・点検日",
        value=date.today()
    )

    quantity = st.number_input(
        "数量",
        min_value=1,
        value=1,
        step=1
    )

    location = st.text_input(
        "保管場所",
        placeholder="例：玄関の棚、押し入れ"
    )

    memo = st.text_area(
        "メモ",
        placeholder="例：家族4人分"
    )

    submitted = st.form_submit_button(
        "登録する"
    )

    if submitted:

        if name.strip() == "":
            st.error("商品名を入力してください。")

        else:

            data = {
                "family_code": family_code,
                "name": name,
                "category": category,
                "expiry_type": expiry_type,
                "expiry_date": expiry_date.isoformat(),
                "quantity": quantity,
                "location": location,
                "memo": memo
            }

            try:

                supabase.table(
                    "emergency_items"
                ).insert(data).execute()

                st.success(
                    f"「{name}」を登録しました！"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"登録に失敗しました：{e}"
                )


# -------------------------
# 登録済みデータ取得
# -------------------------

st.divider()

st.subheader("📦 登録済み防災グッズ")

try:

    response = (
        supabase
        .table("emergency_items")
        .select("*")
        .eq("family_code", family_code)
        .order("expiry_date")
        .execute()
    )

    items = response.data

except Exception as e:

    st.error(
        f"データの取得に失敗しました：{e}"
    )

    items = []


# -------------------------
# 件数集計
# -------------------------

expired_count = 0
warning_count = 0
safe_count = 0

for item in items:

    expiry = date.fromisoformat(
        item["expiry_date"]
    )

    icon, status, days_left = get_status(expiry)

    if status == "期限切れ":
        expired_count += 1

    elif status == "期限間近":
        warning_count += 1

    else:
        safe_count += 1


# -------------------------
# 状態サマリー
# -------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🔴 期限切れ",
        expired_count
    )

with col2:
    st.metric(
        "🟡 期限間近",
        warning_count
    )

with col3:
    st.metric(
        "🟢 安全",
        safe_count
    )


# -------------------------
# 一覧表示
# -------------------------

if not items:

    st.info(
        "まだ防災グッズが登録されていません。"
    )

else:

    for item in items:

        expiry = date.fromisoformat(
            item["expiry_date"]
        )

        icon, status, days_left = get_status(
            expiry
        )

        # -------------------------
        # 色
        # -------------------------

        if status == "期限切れ":

            box_color = "#ffebee"
            border_color = "#e53935"

        elif status == "期限間近":

            box_color = "#fff8e1"
            border_color = "#f9a825"

        else:

            box_color = "#e8f5e9"
            border_color = "#43a047"


        # -------------------------
        # カード
        # -------------------------

        st.markdown(
            f"""
            <div style="
                background-color:{box_color};
                border-left:8px solid {border_color};
                padding:15px;
                margin-bottom:15px;
                border-radius:10px;
            ">

                <h3 style="margin-top:0;">
                    {icon} {item["name"]}
                </h3>

                <p>
                    <b>状態：</b>{status}
                </p>

                <p>
                    <b>{item["expiry_type"]}：</b>
                    {item["expiry_date"]}
                </p>

                <p>
                    <b>残り：</b>
                    {
                        "期限切れ"
                        if days_left < 0
                        else f"あと {days_left} 日"
                    }
                </p>

                <p>
                    <b>カテゴリ：</b>
                    {item["category"]}
                </p>

                <p>
                    <b>数量：</b>
                    {item["quantity"]}
                </p>

                <p>
                    <b>保管場所：</b>
                    {item["location"] or "未登録"}
                </p>

                <p>
                    <b>メモ：</b>
                    {item["memo"] or "なし"}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------
        # 削除
        # -------------------------

        if st.button(
            f"🗑️ {item['name']}を削除",
            key=f"delete_{item['id']}"
        ):

            try:

                (
                    supabase
                    .table("emergency_items")
                    .delete()
                    .eq("id", item["id"])
                    .eq("family_code", family_code)
                    .execute()
                )

                st.success("削除しました。")
                st.rerun()

            except Exception as e:

                st.error(
                    f"削除に失敗しました：{e}"
                )