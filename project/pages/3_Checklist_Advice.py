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
# ログインチェック
# =========================================================

if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

family_code = st.session_state["family_code"]

# =========================================================
# タイトル
# =========================================================

st.title("✅ 防災備品チェックリスト")
st.caption("必要な防災備品がそろっているか確認しましょう。")

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

st.info(f"👨‍👩‍👧‍👦 登録されている家族人数：**{family_count} 人**")

# =========================================================
# 必要な防災備品
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
# 必要量の目安
# =========================================================

st.divider()
st.subheader("📦 必要量の目安")

for name, data in required.items():

    with st.container(border=True):

        st.markdown(f"### {name}")

        st.caption(data["description"])

        st.write(
            f"必要量：**{data['qty']} {data['unit']}**"
        )

# =========================================================
# Supabaseからチェック状態を取得
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

        try:
            saved_checks = json.loads(
                response.data[0]["data"]
            )
        except Exception:
            saved_checks = {}

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

    with st.container(border=True):

        st.markdown(f"### {name}")

        st.write(
            f"必要量：**{data['qty']} {data['unit']}**"
        )

        checked[name] = st.checkbox(
            "準備済み",
            value=saved_checks.get(name, False),
            key=f"check_{name}"
        )

# =========================================================
# 達成率
# =========================================================

total = len(checked)

done = sum(
    1 for value in checked.values()
    if value
)

rate = int(
    done / total * 100
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

        supabase.table("checklist").upsert({
            "family_code": family_code,
            "data": json.dumps(
                checked,
                ensure_ascii=False
            )
        }).execute()

        st.success("チェック状態を保存しました！")

    except Exception as e:

        st.error(
            f"保存に失敗しました：{e}"
        )

# =========================================================
# 未チェックの備品
# =========================================================

st.divider()
st.subheader("⚠️ 準備できていない備品")

not_completed = [
    name
    for name, done_value in checked.items()
    if not done_value
]

if not_completed:

    for name in not_completed:

        data = required[name]

        with st.container(border=True):

            st.warning(
                f"{name}　｜　"
                f"必要量：{data['qty']} {data['unit']}"
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

for name, done_value in checked.items():

    if not done_value:

        data = required[name]

        shopping_list.append(
            f"{name}：{data['qty']} {data['unit']}"
        )

if shopping_list:

    for item in shopping_list:
        st.warning(f"🛒 {item}")

else:

    st.success(
        "買い物をする必要はありません！"
    )

# =========================================================
# 家族の備え
# =========================================================

st.divider()
st.subheader("🛡️ 家族の備え")

# =========================================================
# 安全状態
# =========================================================

def get_safety(rate):

    if rate >= 90:
        return "非常に安全"

    elif rate >= 70:
        return "おおむね安全"

    elif rate >= 50:
        return "注意"

    elif rate >= 30:
        return "警戒"

    else:
        return "危険"


safety_text = get_safety(rate)

# 状態によって標準UIを変更
if safety_text == "非常に安全":

    st.success(
        f"🟢 {safety_text}"
    )

elif safety_text == "おおむね安全":

    st.success(
        f"🟢 {safety_text}"
    )

elif safety_text == "注意":

    st.warning(
        f"🟡 {safety_text}"
    )

elif safety_text == "警戒":

    st.warning(
        f"🟠 {safety_text}"
    )

else:

    st.error(
        f"🔴 {safety_text}"
    )

# =========================================================
# 達成率
# =========================================================

st.metric(
    "防災備品の準備達成率",
    f"{rate}%"
)

st.progress(
    rate / 100
)

st.write(
    f"**{done} / {total} 項目** 準備済み"
)

# =========================================================
# チェック状況
# =========================================================

st.subheader("📋 チェック状況")

for name, is_done in checked.items():

    data = required[name]

    col1, col2 = st.columns([4, 1])

    with col1:

        st.write(
            f"**{name}**"
        )

    with col2:

        if is_done:
            st.success("完了")
        else:
            st.error("未準備")