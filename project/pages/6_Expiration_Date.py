import streamlit as st
from supabase import create_client
from datetime import date

# =========================================================
# Supabase接続
# =========================================================

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =========================================================
# ページ設定
# =========================================================

st.set_page_config(
    page_title="防災グッズ管理",
    page_icon="🧰",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 20px;
    }

    .page-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .page-description {
        color: #666;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* 状態ラベル */
    .status-label {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 7px;
        color: white;
        font-size: 15px;
        font-weight: 700;
        margin: 8px 0 10px 0;
    }

    /* 状態を大きく表示するバー */
    .status-box {
        width: 100%;
        padding: 12px;
        border-radius: 9px;
        color: white;
        text-align: center;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 18px;
        box-sizing: border-box;
    }

    .item-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 3px;
    }

    .info-title {
        font-size: 14px;
        color: #666;
        margin-bottom: 2px;
    }

    .info-value {
        font-size: 17px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .memo-box {
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 12px;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# タイトル
# =========================================================

st.markdown(
    '<div class="page-title">🧰 防災グッズ管理</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-description">'
    '非常食・保存水・乾電池・防災用品などの期限をまとめて管理できます。'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# ログイン確認
# =========================================================

if "family_code" not in st.session_state:
    st.warning("先にメインページでログインしてください。")
    st.stop()

family_code = st.session_state["family_code"]

# =========================================================
# 状態判定
# =========================================================

def get_status(expiry_date):
    """
    期限までの日数によって
    安全 / 注意 / 警戒 / 危険
    を判定する
    """

    today = date.today()
    days_left = (expiry_date - today).days

    # 期限切れ
    if days_left < 0:
        return {
            "status": "危険",
            "color": "#f44336",
            "days": days_left
        }

    # 30日以内
    elif days_left <= 30:
        return {
            "status": "警戒",
            "color": "#ff9800",
            "days": days_left
        }

    # 90日以内
    elif days_left <= 90:
        return {
            "status": "注意",
            "color": "#fbc02d",
            "days": days_left
        }

    # 91日以上
    else:
        return {
            "status": "安全",
            "color": "#43a047",
            "days": days_left
        }


# =========================================================
# 防災グッズ登録
# =========================================================

st.subheader("➕ 防災グッズを登録")

with st.form("add_item_form"):

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
        "登録する",
        use_container_width=True
    )

# =========================================================
# 登録処理
# =========================================================

if submitted:

    if name.strip() == "":
        st.error("商品名を入力してください。")

    else:

        data = {
            "family_code": family_code,
            "name": name.strip(),
            "category": category,
            "expiry_type": expiry_type,
            "expiry_date": expiry_date.isoformat(),
            "quantity": int(quantity),
            "location": location.strip(),
            "memo": memo.strip()
        }

        try:

            response = (
                supabase
                .table("emergency_items")
                .insert(data)
                .execute()
            )

            if response.data:
                st.success(f"「{name}」を登録しました！")
                st.rerun()

            else:
                st.error("登録できませんでした。")

        except Exception as e:

            st.error(
                f"登録に失敗しました：{e}"
            )


# =========================================================
# データ取得
# =========================================================

try:

    response = (
        supabase
        .table("emergency_items")
        .select("*")
        .eq("family_code", family_code)
        .order("expiry_date")
        .execute()
    )

    items = response.data or []

except Exception as e:

    st.error(
        f"データの取得に失敗しました：{e}"
    )

    items = []


# =========================================================
# 件数集計
# =========================================================

danger_count = 0
warning_count = 0
caution_count = 0
safe_count = 0

for item in items:

    try:

        expiry = date.fromisoformat(
            item["expiry_date"]
        )

        result = get_status(expiry)

        if result["status"] == "危険":
            danger_count += 1

        elif result["status"] == "警戒":
            warning_count += 1

        elif result["status"] == "注意":
            caution_count += 1

        else:
            safe_count += 1

    except Exception:
        pass


# =========================================================
# 期限状況
# =========================================================

st.divider()

st.subheader("📊 期限状況")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "危険",
        f"{danger_count} 件"
    )

with col2:
    st.metric(
        "警戒",
        f"{warning_count} 件"
    )

with col3:
    st.metric(
        "注意",
        f"{caution_count} 件"
    )

with col4:
    st.metric(
        "安全",
        f"{safe_count} 件"
    )


# =========================================================
# 検索・フィルター
# =========================================================

st.subheader("🔎 防災グッズを探す")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    filter_status = st.selectbox(
        "状態",
        [
            "すべて",
            "危険",
            "警戒",
            "注意",
            "安全"
        ]
    )

with filter_col2:

    search_name = st.text_input(
        "商品名検索",
        placeholder="例：水"
    )


# =========================================================
# 商品一覧
# =========================================================

st.subheader("📦 登録済み防災グッズ")

if not items:

    st.info(
        "まだ防災グッズが登録されていません。"
    )

else:

    shown_count = 0

    for item in items:

        try:

            expiry = date.fromisoformat(
                item["expiry_date"]
            )

        except Exception:
            continue

        result = get_status(expiry)

        status = result["status"]
        color = result["color"]
        days_left = result["days"]

        # -------------------------------------------------
        # フィルター
        # -------------------------------------------------

        if filter_status != "すべて":

            if status != filter_status:
                continue

        if search_name.strip():

            if search_name.lower() not in item["name"].lower():
                continue

        shown_count += 1

        # -------------------------------------------------
        # 商品カード
        # -------------------------------------------------

        with st.container(border=True):

            # 商品名
            st.markdown(
                f'<div class="item-title">{item["name"]}</div>',
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # 左上の小さいラベル
            # -------------------------------------------------

            label_text = f"{item['expiry_type']}"

            if days_left < 0:
                label_text += "切れ"
            else:
                label_text += " " + item["expiry_date"]

            st.markdown(
                f"""
                <div
                    class="status-label"
                    style="background-color:{color};"
                >
                    {label_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # 大きな状態バー
            # -------------------------------------------------

            st.markdown(
                f"""
                <div
                    class="status-box"
                    style="background-color:{color};"
                >
                    {status}
                </div>
                """,
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # 情報
            # -------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    '<div class="info-title">期限の種類</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="info-value">'
                    f'{item["expiry_type"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="info-title">期限</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="info-value">'
                    f'{item["expiry_date"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                # 残り日数
                if days_left < 0:

                    st.error(
                        f"{abs(days_left)} 日前に期限切れです"
                    )

                elif days_left == 0:

                    st.warning(
                        "今日が期限です"
                    )

                else:

                    st.write(
                        f"あと **{days_left} 日**"
                    )

            with col2:

                st.markdown(
                    '<div class="info-title">カテゴリ</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="info-value">'
                    f'{item["category"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="info-title">数量</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="info-value">'
                    f'{item["quantity"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="info-title">保管場所</div>',
                    unsafe_allow_html=True
                )

                st.write(
                    item["location"] or "未登録"
                )

            # -------------------------------------------------
            # メモ
            # -------------------------------------------------

            if item["memo"]:

                st.markdown(
                    f"""
                    <div class="memo-box">
                        <b>📝 メモ</b><br>
                        {item["memo"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # -------------------------------------------------
            # 削除
            # -------------------------------------------------

            delete_col1, delete_col2 = st.columns([4, 1])

            with delete_col2:

                if st.button(
                    "削除",
                    key=f"delete_{item['id']}",
                    use_container_width=True
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

    # -------------------------------------------------
    # 検索結果なし
    # -------------------------------------------------

    if shown_count == 0:

        st.info(
            "条件に一致する防災グッズがありません。"
        )