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
response = supabase.table("family_profiles").select("*").eq(
    "family_code", st.session_state["family_code"]
).execute()

if response.data:
    family_data = response.data[0]
    family_count = family_data.get("members", 1)
else:
    family_count = 1

st.info(f"登録されている家族人数: **{family_count} 人**")

# 必要量の説明
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
# チェック状態の永続化（Supabase）
# -------------------------

response = supabase.table("checklist").select("*").eq(
    "family_code", st.session_state["family_code"]
).execute()

if response.data:
    saved_checks = json.loads(response.data[0]["data"])
else:
    saved_checks = {}

# -------------------------
# チェックリスト表示
# -------------------------

st.subheader("チェックリスト")

checked = {}
for name in required.keys():
    default = saved_checks.get(name, False)
    checked[name] = st.checkbox(f"{name}：{required[name]}", value=default)

# -------------------------
# 保存ボタン
# -------------------------

if st.button("チェック状態を保存"):
    supabase.table("checklist").upsert({
        "family_code": st.session_state["family_code"],
        "data": json.dumps(checked)
    }).execute()
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
# 買い物リストの作成
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

# -------------------------
# 家族安全度チェッカー（追加部分）
# -------------------------

st.subheader("家族安全度チェッカー")

total = len(checked)
done = sum(1 for v in checked.values() if v)
rate = int((done / total) * 100)

def get_rank(rate):
    if rate >= 90:
        return "A", "非常に安全", "#4CAF50"   # 緑
    elif rate >= 70:
        return "B", "まあ安心", "#8BC34A"   # 黄緑
    elif rate >= 50:
        return "C", "改善必要", "#FFC107"   # 黄色
    elif rate >= 30:
        return "D", "危険", "#FF9800"       # オレンジ
    else:
        return "E", "非常に危険", "#F44336" # 赤

rank_letter, rank_text, color = get_rank(rate)

# 色付きボックス
st.markdown(
    f"""
    <div style="
        background-color:{color};
        padding: 15px;
        border-radius: 10px;
        color: white;
        font-size: 22px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    ">
        安全度ランク：{rank_letter}（{rank_text}）
    </div>
    """,
    unsafe_allow_html=True
)

st.metric("達成率", f"{rate}%")

st.write("### チェック状況")
for name, done in checked.items():
    st.write(f"- {name}: {'✔️' if done else '❌'}")
