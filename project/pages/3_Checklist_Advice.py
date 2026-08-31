import streamlit as st
import json
from supabase import create_client

# =========================================================
# Supabase
# =========================================================

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

# =========================================================
# ページ設定
# =========================================================

st.set_page_config(
    page_title="SafeBox Manager - Checklist",
    page_icon="✅",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* 全体 */
    .main {
        padding-top: 20px;
    }

    /* タイトル */
    .page-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .page-description {
        color: #666;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* 家族人数 */
    .family-info {
        background: #f5f7fa;
        border: 1px solid #e1e5ea;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 20px;
    }

    /* 必要量カード */
    .required-card {
        background: white;
        border: 1px solid #e3e7eb;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }

    .required-name {
        font-size: 16px;
        font-weight: 600;
    }

    .required-value {
        font-size: 14px;
        color: #666;
        margin-top: 3px;
    }

    /* チェックカード */
    .check-card {
        background: white;
        border: 1px solid #e3e7eb;
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }

    /* 買い物リスト */
    .shopping-card {
        background: #fff8e8;
        border-left: 5px solid #f59e0b;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }

    /* 安全度 */
    .safety-box {
        padding: 18px;
        border-radius: 12px;
        color: white;
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 18px;
    }

    /* 達成率 */
    .rate-box {
        background: #f5f7fa;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        margin-bottom: 15px;
    }

    .rate-number {
        font-size: 34px;
        font-weight: 700;
    }

    .rate-label {
        color: #666;
        font-size: 14px;
    }

    /* 状態 */
    .status-ok {
        color: #2e7d32;
        font-weight: 600;
    }

    .status-ng {
        color: #d32f2f;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# タイトル
# =========================================================

st.markdown(
    '<div class="page-title">✅ 防災備品チェックリスト</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-description">'
    '必要な防災備品がそろっているか確認しましょう。'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# ログインチェック
# =========================================================

if "family_code" not in st.session_state:
    st.warning("初めにログインしてください。")
    st.stop()

family_code = st.session_state["family_code"]

st.success(f"ログイン中：{family_code}")

# =========================================================
# 家族データ取得
# =========================================================

try:

    response = (
        supabase
        .table("family_profiles")
        .select("*")
        .eq("family_code", family_code)
        .execute()
    )

    if response.data:
        family_data = response.data[0]
        family_count = family_data.get("members", 1)
    else:
        family_count = 1

except Exception:

    family_count = 1

# =========================================================
# 家族人数
# =========================================================

st.markdown(
    f"""
    <div class="family-info">
        <b>👨‍👩‍👧‍👦 家族人数</b><br>
        <span style="font-size:22px;font-weight:bold;">
            {family_count} 人
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 必要量
# =========================================================

items = {

    "飲料水": {
        "description": "1人1日3L × 3日分",
        "qty": 9,
        "unit": "L"
    },

    "非常食": {
        "description": "1人3日分",
        "qty": 3,
        "unit": "食"
    },

    "携帯トイレ": {
        "description": "1人3〜5回分 × 3日",
        "qty": 12,
        "unit": "個"
    },

    "モバイルバッテリー": {
        "description": "家族で最低1台",
        "qty": 1,
        "unit": "台"
    },

    "懐中電灯": {
        "description": "家族で最低1本",
        "qty": 1,
        "unit": "本"
    },

    "乾電池": {
        "description": "予備を含めて準備",
        "qty": 4,
        "unit": "本"
    },

    "救急セット": {
        "description": "家庭に1セット",
        "qty": 1,
        "unit": "セット"
    },

    "常備薬": {
        "description": "必要な薬を準備",
        "qty": 1,
        "unit": "種類"
    },

    "防寒具": {
        "description": "1人1枚",
        "qty": 1,
        "unit": "枚"
    }

}

required = {
    name: {
        "qty": data["qty"] * family_count,
        "unit": data["unit"],
        "description": data["description"]
    }
    for name, data in items.items()
}

# =========================================================
# 必要量表示
# =========================================================

st.subheader("📦 必要量の目安")

for name, data in required.items():

    st.markdown(
        f"""
        <div class="required-card">
            <div class="required-name">
                {name}
            </div>

            <div class="required-value">
                {data["description"]}
            </div>

            <div style="
                margin-top:7px;
                font-size:18px;
                font-weight:bold;
            ">
                必要量：{data["qty"]} {data["unit"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# チェック状態取得
# =========================================================

try:

    response = (
        supabase
        .table("checklist")
        .select("*")
        .eq("family_code", family_code)
        .execute()
    )

    if response.data:

        saved_checks = json.loads(
            response.data[0]["data"]
        )

    else:

        saved_checks = {}

except Exception:

    saved_checks = {}

# =========================================================
# チェックリスト
# =========================================================

st.divider()

st.subheader("✅ 備品チェック")

checked = {}

for name, data in required.items():

    default = saved_checks.get(name, False)

    st.markdown(
        f"""
        <div class="check-card">
            <b>{name}</b><br>
            <span style="color:#666;font-size:13px;">
                必要量：{data["qty"]} {data["unit"]}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    checked[name] = st.checkbox(
        "準備済み",
        value=default,
        key=f"check_{name}"
    )

# =========================================================
# 達成率計算
# =========================================================

total = len(checked)

done = sum(
    1
    for value in checked.values()
    if value
)

rate = int(
    (done / total) * 100
) if total > 0 else 0

# =========================================================
# 保存
# =========================================================

st.divider()

if st.button(
    "💾 チェック状態を保存",
    use_container_width=True
):

    try:

        supabase.table("checklist").upsert(
            {
                "family_code": family_code,
                "data": json.dumps(checked, ensure_ascii=False)
            }
        ).execute()

        st.success("チェック状態を保存しました！")

    except Exception as e:

        st.error(
            f"保存に失敗しました：{e}"
        )

# =========================================================
# 未チェック
# =========================================================

st.divider()

st.subheader("⚠️ 準備できていない備品")

not_completed = [
    name
    for name, done in checked.items()
    if not done
]

if not_completed:

    for name in not_completed:

        data = required[name]

        st.markdown(
            f"""
            <div class="shopping-card">
                <b>{name}</b><br>
                必要量：{data["qty"]} {data["unit"]}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.success(
        "すべての備品が準備済みです！"
    )

# =========================================================
# 買い物リスト
# =========================================================

st.divider()

st.subheader("🛒 買い物リスト")

shopping_list = []

for name, done in checked.items():

    if not done:

        data = required[name]

        shopping_list.append(
            f"{name}：{data['qty']} {data['unit']}"
        )

if shopping_list:

    for item in shopping_list:

        st.markdown(
            f"""
            <div class="shopping-card">
                🛒 {item}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.success(
        "買い物リストはありません。"
    )

# =========================================================
# 家族安全度
# =========================================================

st.divider()

st.subheader("🛡️ 家族の備え")

# =========================================================
# 安全状態
# =========================================================

def get_safety(rate):

    if rate >= 90:
        return (
            "非常に安全",
            "#43a047"
        )

    elif rate >= 70:
        return (
            "おおむね安全",
            "#8bc34a"
        )

    elif rate >= 50:
        return (
            "注意",
            "#fbc02d"
        )

    elif rate >= 30:
        return (
            "警戒",
            "#ff9800"
        )

    else:
        return (
            "危険",
            "#f44336"
        )

safety_text, safety_color = get_safety(rate)

st.markdown(
    f"""
    <div
        class="safety-box"
        style="background-color:{safety_color};"
    >
        {safety_text}
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 達成率
# =========================================================

st.markdown(
    f"""
    <div class="rate-box">

        <div class="rate-number">
            {rate}%
        </div>

        <div class="rate-label">
            防災備品の準備達成率
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# プログレスバー
st.progress(rate / 100)

st.write(
    f"**{done} / {total} 項目** 準備済み"
)

# =========================================================
# チェック状況
# =========================================================

st.subheader("📋 チェック状況")

for name, is_done in checked.items():

    if is_done:

        st.markdown(
            f"""
            <div class="required-card">
                <span class="status-ok">
                    ✓ {name}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="required-card">
                <span class="status-ng">
                    未準備　{name}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )