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
    st.error(f"データの取得に失敗しました：{e}")
    items = []


# -------------------------
# 期限判定
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
# 件数集計
# -------------------------

expired_count = 0
warning_count = 0
safe_count = 0

for item in items:

    expiry = date.fromisoformat(item["expiry_date"])

    icon, status, days_left = get_status(expiry)

    if status == "期限切れ":
        expired_count += 1

    elif status == "期限間近":
        warning_count += 1

    else:
        safe_count += 1


# -------------------------
# サマリー
# -------------------------

st.markdown("### 📊 期限状況")

col1, col2, col3 = st.columns(3)

with col1:
    st.error(f"🔴 期限切れ\n\n**{expired_count} 件**")

with col2:
    st.warning(f"🟡 期限間近\n\n**{warning_count} 件**")

with col3:
    st.success(f"🟢 安全\n\n**{safe_count} 件**")


# -------------------------
# フィルター
# -------------------------

st.markdown("### 🔎 絞り込み")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    filter_status = st.selectbox(
        "状態",
        [
            "すべて",
            "🔴 期限切れ",
            "🟡 期限間近",
            "🟢 安全"
        ]
    )

with filter_col2:
    search_name = st.text_input(
        "商品名検索",
        placeholder="例：水、アルファ米"
    )


# -------------------------
# 商品一覧
# -------------------------

if not items:

    st.info("まだ防災グッズが登録されていません。")

else:

    shown_count = 0

    for item in items:

        expiry = date.fromisoformat(item["expiry_date"])

        icon, status, days_left = get_status(expiry)

        # -------------------------
        # フィルター判定
        # -------------------------

        if filter_status != "すべて":
            if not filter_status.startswith(icon):
                continue

        if search_name.strip():
            if search_name.lower() not in item["name"].lower():
                continue

        shown_count += 1

        # -------------------------
        # カード
        # -------------------------

        with st.container(border=True):

            # 上段
            top_col1, top_col2 = st.columns([4, 1])

            with top_col1:
                st.markdown(
                    f"## {icon} {item['name']}"
                )

            with top_col2:

                if status == "期限切れ":
                    st.error("期限切れ")

                elif status == "期限間近":
                    st.warning("期限間近")

                else:
                    st.success("安全")

            # 区切り
            st.divider()

            # 情報
            info_col1, info_col2 = st.columns(2)

            with info_col1:

                st.markdown(
                    f"**📅 {item['expiry_type']}**"
                )

                st.write(
                    item["expiry_date"]
                )

                if days_left < 0:

                    st.error(
                        f"⚠️ {abs(days_left)} 日超過"
                    )

                elif days_left == 0:

                    st.warning(
                        "⚠️ 今日が期限です"
                    )

                else:

                    st.write(
                        f"残り **{days_left} 日**"
                    )

            with info_col2:

                st.markdown("**📦 基本情報**")

                st.write(
                    f"カテゴリ：{item['category']}"
                )

                st.write(
                    f"数量：{item['quantity']}"
                )

                if item["location"]:
                    st.write(
                        f"📍 保管場所：{item['location']}"
                    )
                else:
                    st.write(
                        "📍 保管場所：未登録"
                    )

            # メモ
            if item["memo"]:

                st.markdown("**📝 メモ**")

                st.info(
                    item["memo"]
                )

            # 削除
            delete_col1, delete_col2 = st.columns([5, 1])

            with delete_col2:

                if st.button(
                    "🗑️ 削除",
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

                        st.success("削除しました")
                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"削除に失敗しました：{e}"
                        )

    # 検索結果が0件
    if shown_count == 0:

        st.info(
            "条件に一致する防災グッズがありません。"
        )