import streamlit as st
import json
import os
from supabase import create_client

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("SafeBox Manager - Checklist")

# ログインチェック
if "family_code" not in st.session_state:
    st.warning("初めにログインしてください")
    st.stop()

st.success(f"ログイン中：{st.session_state['family_code']}")

# Supabase から家族データを読み込む
response = supabase.table("family_profiles").select("*").eq("family_code", st.session_state["family_code"]).execute()

if response.data:
    family_data = response.data[0]
    family_count = family_data.get("members", 1)
else:
    family_count = 1


st.info(f"登録されている家族人数: **{family_count} 人**")

# 必要量の説明（元のまま）
items = {
    "飲料水（1人1日3L × 3日分）": {"qty": 9, "unit": "L"},
    "非常食（1人3日分）": {"qty": 3, "unit": "食"},
    "携帯トイレ（1人3〜5回分 × 3日）": {"qty": 12, "unit": "個"},
    "モバイルバッテリー": {"qty": 1, "unit": "台"},
    "懐中電灯": {"qty": 1, "unit": "本"},
    "乾電池": {"qty": 4, "unit": "本"},
    "救急セット": {"qty": 1, "unit": "セット"},
    "常備薬": {"qty": 1, "unit": "種類"},
    "防寒具": {"qty": 1, "unit": "枚"},
}

# 必要量の計算
required = {
    name: f"{data['qty'] * family_count} {data['unit']}"
    for name, data in items.items()
}

st.subheader("必要量の目安")
for name, value in required.items():
    st.write(f"- **{name}**：必要量 → **{value}**")

# -------------------------
# チェック状態の永続化（JSON）
# -------------------------

CHECK_PATH = "data/checklist.json"

# JSONがなければ作成
if not os.path.exists(CHECK_PATH):
    with open(CHECK_PATH, "w") as f:
        json.dump({}, f)

# JSON読み込み
with open(CHECK_PATH, "r") as f:
    saved_checks = json.load(f)

# -------------------------
# チェックリスト表示
# -------------------------

st.subheader("チェックリスト")

checked = {}
for name in required.keys():
    # 保存されている状態を反映
    default = saved_checks.get(name, False)
    checked[name] = st.checkbox(f"{name}：{required[name]}", value=default)

# -------------------------
# 保存ボタン
# -------------------------

if st.button("チェック状態を保存"):
    with open(CHECK_PATH, "w") as f:
        json.dump(checked, f, indent=2)
    st.success("チェック状態を保存しました")

# -------------------------
# 未チェックの表示
# -------------------------

st.subheader("チェックされていない備品")

not_completed = [name for name, done in checked.items() if not done]

if not_completed:
    st.warning("まだチェックされていない備品:")
    for item in not_completed:
        st.write(f"- {item}")
else:
    st.success("すべての備品がチェック済みとなっています")

#--------------------
#買い物リストの作成
#--------------------

st.subheader("買い物リスト")

shopping_list = []

for name, done in checked.items():
    if not done:
        shopping_list.append(f"{name}:{required[name]}")

if shopping_list:
    st.error("買い物リスト")
    for item in shopping_list:
        st.write(f"- {item}")

else:
    st.success("買い物をする必要はありません")