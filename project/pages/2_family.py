import streamlit as st
from supabase import create_client

# =========================================================
# Supabase 接続
# =========================================================

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

# =========================================================
# ページ設定
# =========================================================

st.set_page_config(
    page_title="SafeBox Manager - Family",
    page_icon="👨‍👩‍👧‍👦",
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
# 編集モード
# =========================================================

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# =========================================================
# タイトル
# =========================================================

st.title("👨‍👩‍👧‍👦 家族構成")
st.caption("SafeBox Managerに登録する家族情報を管理します。")

st.success(f"ログイン中：{family_code}")

# =========================================================
# Supabaseから家族データ取得
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
    else:
        family_data = {
            "members": 1,
            "names": [],
            "notes": ""
        }

except Exception as e:

    st.error(f"家族情報の取得に失敗しました：{e}")

    family_data = {
        "members": 1,
        "names": [],
        "notes": ""
    }

# =========================================================
# 現在の状態
# =========================================================

st.subheader("🔐 状態")

if st.session_state.edit_mode:

    st.warning("編集モード：現在、家族情報を変更できます。")

    if st.button(
        "🔒 保存して閲覧モードに戻る",
        use_container_width=True
    ):
        st.session_state.edit_mode = False
        st.rerun()

else:

    st.info("閲覧モード：現在、家族情報は変更できません。")

    if st.button(
        "✏️ 家族情報を変更する",
        use_container_width=True
    ):
        st.session_state.edit_mode = True
        st.rerun()

disabled_flag = not st.session_state.edit_mode

# =========================================================
# 家族人数
# =========================================================

st.divider()

st.subheader("👨‍👩‍👧‍👦 家族人数")

members = st.number_input(
    "登録する家族人数",
    min_value=1,
    max_value=100,
    value=int(family_data.get("members", 1)),
    step=1,
    disabled=disabled_flag
)

st.info(f"現在の登録人数：**{members} 人**")

# =========================================================
# 名前
# =========================================================

st.divider()

st.subheader("📝 家族全員の名前")

existing_names = family_data.get("names", [])

# namesが文字列になっていた場合への対策
if not isinstance(existing_names, list):
    existing_names = []

name_inputs = []

for i in range(int(members)):

    default_name = (
        existing_names[i]
        if i < len(existing_names)
        else ""
    )

    with st.container(border=True):

        st.markdown(f"### {i + 1}人目")

        name_input = st.text_input(
            "名前",
            value=default_name,
            placeholder=f"{i + 1}人目の名前を入力",
            disabled=disabled_flag,
            key=f"family_name_{i}"
        )

        name_inputs.append(name_input)

# =========================================================
# 備考
# =========================================================

st.divider()

st.subheader("📝 備考")

notes = st.text_area(
    "家族についてのメモ",
    value=family_data.get("notes", ""),
    placeholder="例：避難時に必要なこと、連絡方法など",
    height=140,
    disabled=disabled_flag
)

# =========================================================
# 保存
# =========================================================

if st.session_state.edit_mode:

    st.divider()

    if st.button(
        "💾 家族構成を保存",
        use_container_width=True
    ):

        # 名前を整える
        cleaned_names = [
            name.strip()
            for name in name_inputs
        ]

        data = {
            "family_code": family_code,
            "members": int(members),
            "names": cleaned_names,
            "notes": notes.strip()
        }

        try:

            (
                supabase
                .table("family_profiles")
                .upsert(data)
                .execute()
            )

            # セッションにも保存
            st.session_state["family_data"] = data

            # 編集モード終了
            st.session_state.edit_mode = False

            st.success("家族構成を保存しました！")

            st.rerun()

        except Exception as e:

            st.error(
                f"保存に失敗しました：{e}"
            )

# =========================================================
# 閲覧用サマリー
# =========================================================

if not st.session_state.edit_mode:

    st.divider()

    st.subheader("📋 登録内容")

    # -----------------------------------------------------
    # 人数
    # -----------------------------------------------------

    st.metric(
        "家族人数",
        f"{family_data.get('members', 1)} 人"
    )

    # -----------------------------------------------------
    # 名前一覧
    # -----------------------------------------------------

    st.markdown("### 👨‍👩‍👧‍👦 家族一覧")

    saved_names = family_data.get("names", [])

    if saved_names:

        for i, name in enumerate(saved_names):

            if name.strip():

                with st.container(border=True):

                    st.write(
                        f"**{i + 1}人目**"
                    )

                    st.write(
                        f"### {name}"
                    )

    else:

        st.info(
            "まだ家族の名前が登録されていません。"
        )

    # -----------------------------------------------------
    # 備考
    # -----------------------------------------------------

    st.markdown("### 📝 備考")

    saved_notes = family_data.get("notes", "")

    if saved_notes.strip():

        st.info(saved_notes)

    else:

        st.caption(
            "備考は登録されていません。"
        )