import streamlit as st
import random

st.set_page_config(page_title="防災クイズ", page_icon="📝")

# -------------------------
# セッション初期化
# -------------------------
if "rank" not in st.session_state:
    st.session_state.rank = 1
if "points" not in st.session_state:
    st.session_state.points = 0
if "mode" not in st.session_state:
    st.session_state.mode = None
if "practice_questions" not in st.session_state:
    st.session_state.practice_questions = []
if "test_questions" not in st.session_state:
    st.session_state.test_questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "result_marks" not in st.session_state:
    st.session_state.result_marks = {}
if "test_passed" not in st.session_state:
    st.session_state.test_passed = False

# -------------------------
# 問題数ロジック
# -------------------------
def get_practice_count(rank):
    if rank >= 20:
        return 100
    return 10 + (rank - 1) * 5

def get_test_count():
    return 10

# -------------------------
# 問題データ（Lv1〜Lv5）
# -------------------------
def get_lv1_questions():
    return [
        {"q": "地震が起きたとき、まず最初にすべき行動は？",
         "choices": ["頭を守る", "外に走って出る", "スマホを見る", "窓を開ける"],
         "answer": "頭を守る"},
        {"q": "避難所で最も大切なことは？",
         "choices": ["静かにする", "情報を共有する", "荷物を広げる", "好きな場所を占領する"],
         "answer": "情報を共有する"},
        {"q": "災害時に役立つのはどれ？",
         "choices": ["懐中電灯", "ゲーム機", "大きなスピーカー", "観葉植物"],
         "answer": "懐中電灯"},
        {"q": "非常食として正しいものは？",
         "choices": ["缶詰", "生肉", "アイスクリーム", "ケーキ"],
         "answer": "缶詰"},
        {"q": "災害時に水が止まった場合、まず使うべき水は？",
         "choices": ["ペットボトルの水", "トイレの水", "お風呂の残り湯", "川の水"],
         "answer": "お風呂の残り湯"},
        {"q": "避難するときに必要なものは？",
         "choices": ["スマホ", "貴重品", "水", "全部必要"],
         "answer": "全部必要"},
        {"q": "災害用伝言ダイヤルの番号は？",
         "choices": ["171", "911", "119", "777"],
         "answer": "171"},
        {"q": "地震の揺れが収まった後にすべきことは？",
         "choices": ["火の確認", "すぐ寝る", "SNSに投稿", "走り回る"],
         "answer": "火の確認"},
        {"q": "避難所でのトラブルを防ぐために大切なことは？",
         "choices": ["譲り合い", "大声で話す", "荷物を広げる", "他人を無視する"],
         "answer": "譲り合い"},
        {"q": "災害時に一番大切なのは？",
         "choices": ["命を守ること", "荷物を守ること", "家を守ること", "SNSで情報発信"],
         "answer": "命を守ること"},
    ]

def get_lv2_questions():
    return [
        {"q": "地震の揺れが強いとき、家の中で最も危険なのは？",
         "choices": ["窓際", "机の下", "布団の中", "玄関"],
         "answer": "窓際"},
        {"q": "耐震家具の固定に使うべきものは？",
         "choices": ["L字金具", "ガムテープ", "ひも", "接着剤"],
         "answer": "L字金具"},
        {"q": "地震が起きたとき、エレベーターに乗っていたら？",
         "choices": ["最寄り階で降りる", "そのまま上に行く", "非常ボタンを押す", "ジャンプする"],
         "answer": "最寄り階で降りる"},
        {"q": "地震の揺れで火災が起きやすい場所は？",
         "choices": ["キッチン", "玄関", "寝室", "トイレ"],
         "answer": "キッチン"},
        {"q": "地震後にガスの安全確認をする方法は？",
         "choices": ["元栓を閉める", "匂いを嗅ぐ", "火をつける", "ガス管を叩く"],
         "answer": "元栓を閉める"},
    ]

def get_lv3_questions():
    return [
        {"q": "避難指示が出たときにまず確認すべきことは？",
         "choices": ["避難経路", "天気", "SNSの反応", "テレビ番組表"],
         "answer": "避難経路"},
        {"q": "避難するときに靴として適切なのは？",
         "choices": ["運動靴", "サンダル", "ハイヒール", "裸足"],
         "answer": "運動靴"},
        {"q": "避難所に向かうとき、持ち出し品として優先度が高いものは？",
         "choices": ["水・食料・貴重品", "ゲーム機", "観葉植物", "大きな家具"],
         "answer": "水・食料・貴重品"},
    ]

def get_lv4_questions():
    return [
        {"q": "家庭の備蓄で最低限必要な水の量は？（1人1日あたり）",
         "choices": ["3リットル", "500ミリリットル", "10リットル", "1リットル"],
         "answer": "3リットル"},
        {"q": "非常食として適切なものは？",
         "choices": ["長期保存できる食品", "生もの", "冷凍食品のみ", "調理が複雑な料理"],
         "answer": "長期保存できる食品"},
    ]

def get_lv5_questions():
    return [
        {"q": "災害時に家族と連絡を取る方法として事前に決めておくべきなのは？",
         "choices": ["連絡手段と集合場所", "その場のノリ", "SNSだけ", "電話だけ"],
         "answer": "連絡手段と集合場所"},
        {"q": "災害時に子どもに教えておくべきことは？",
         "choices": ["避難場所と連絡先", "ゲームのスコア", "テレビ番組表", "好きな食べ物"],
         "answer": "避難場所と連絡先"},
    ]

def get_legend_questions():
    return get_lv1_questions() + get_lv2_questions() + get_lv3_questions() + get_lv4_questions() + get_lv5_questions()

# -------------------------
# レベルに応じた問題セット
# -------------------------
def get_questions_for_rank(rank):
    if rank == 1:
        return get_lv1_questions()
    elif rank == 2:
        return get_lv2_questions()
    elif rank == 3:
        return get_lv3_questions()
    elif rank == 4:
        return get_lv4_questions()
    elif rank == 5:
        return get_lv5_questions()
    else:
        return get_legend_questions()

# -------------------------
# UI
# -------------------------
st.title("📝 防災クイズ")

st.info(f"現在のランク：Lv.{st.session_state.rank}")
st.success(f"累計ポイント：{st.session_state.points} pt")

st.divider()

# -------------------------
# 練習問題開始
# -------------------------
if st.button("🎯 練習問題を始める"):
    st.session_state.mode = "practice"
    st.session_state.answers = {}
    st.session_state.result_marks = {}

    all_qs = get_questions_for_rank(st.session_state.rank)
    n = get_practice_count(st.session_state.rank)

    st.session_state.practice_questions = random.sample(all_qs, min(n, len(all_qs)))

# -------------------------
# テスト開始
# -------------------------
if st.button("🔥 テストを受ける（9問正解で合格）"):
    st.session_state.mode = "test"
    st.session_state.answers = {}
    st.session_state.result_marks = {}

    all_qs = get_questions_for_rank(st.session_state.rank)
    st.session_state.test_questions = random.sample(all_qs, get_test_count())

# -------------------------
# ○ × を重ねて表示する CSS
# -------------------------
st.markdown("""
<style>
.correct-mark {
    color: green;
    font-size: 40px;
    font-weight: bold;
}
.wrong-mark {
    color: red;
    font-size: 40px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 練習問題表示
# -------------------------
if st.session_state.mode == "practice":
    qs = st.session_state.practice_questions
    st.subheader(f"🎯 練習問題（{len(qs)}問）")

    for idx, q in enumerate(qs):
        st.write(f"### {q['q']}")

        # ○ × を重ねて表示
        if idx in st.session_state.result_marks:
            mark = st.session_state.result_marks[idx]
            if mark == "correct":
                st.markdown("<div class='correct-mark'>○</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='wrong-mark'>×</div>", unsafe_allow_html=True)

        st.session_state.answers[idx] = st.radio(
            "回答を選択してください",
            q["choices"],
            key=f"practice_{idx}"
        )

    if st.button("結果を発表する"):
        correct = 0
        for idx, q in enumerate(qs):
            ans = st.session_state.answers.get(idx)
            if ans == q["answer"]:
                correct += 1
                st.session_state.result_marks[idx] = "correct"
            else:
                st.session_state.result_marks[idx] = "wrong"

        st.write(f"### 結果：{correct} / {len(qs)}")

        # ポイント加算（練習問題のみ）
        st.session_state.points += correct

        st.success(f"🎉 +{correct} pt 獲得！")

# -------------------------
# テスト表示
# -------------------------
if st.session_state.mode == "test":
    qs = st.session_state.test_questions
    st.subheader("🔥 テスト（10問）")

    for idx, q in enumerate(qs):
        st.write(f"### {q['q']}")

        # ○ × を重ねて表示
        if idx in st.session_state.result_marks:
            mark = st.session_state.result_marks[idx]
            if mark == "correct":
                st.markdown("<div class='correct-mark'>○</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='wrong-mark'>×</div>", unsafe_allow_html=True)

        st.session_state.answers[idx] = st.radio(
            "回答を選択してください",
            q["choices"],
            key=f"test_{idx}"
        )

    if st.button("テスト結果を発表する"):
        correct = 0
        for idx, q in enumerate(qs):
            ans = st.session_state.answers.get(idx)
            if ans == q["answer"]:
                correct += 1
                st.session_state.result_marks[idx] = "correct"
            else:
                st.session_state.result_marks[idx] = "wrong"

        st.write(f"### 結果：{correct} / {len(qs)}")

        if correct >= 9:
            st.success("🎉 合格！次のランクへ進めます")
            st.session_state.test_passed = True
            st.session_state.test_correct = correct
        else:
            st.error("不合格… また挑戦しよう！")
            st.session_state.test_passed = False

    if st.session_state.test_passed:
        if st.button("次のランクへ進む"):
            st.session_state.rank += 1

            if st.session_state.test_correct == 9:
                st.session_state.points += 900
            else:
                st.session_state.points += 1200

            st.success("ランクアップしました！")
            st.session_state.mode = None
